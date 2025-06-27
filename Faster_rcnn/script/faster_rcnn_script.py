import os
from codecarbon import EmissionsTracker
from torchinfo import summary
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
from torchmetrics.detection.mean_ap import MeanAveragePrecision
from torchvision.ops import nms

# Analizza le classi nel dataset pth
def analyze_dataset_classes(pth_file, dataset_name="Dataset"):
    data = torch.load(pth_file)
    all_labels = set()
    class_counts = {}
    for k, v in data.items():
        if 'labels' in v and isinstance(v['labels'], torch.Tensor):
            labels = v['labels'].tolist()
            all_labels.update(labels)
            for label in labels:
                class_counts[label] = class_counts.get(label, 0) + 1
    print(f"\nAnalisi {dataset_name}:")
    print(f"Classi trovate: {sorted(all_labels)}")
    print("Distribuzione classi:")
    for class_id in sorted(class_counts.keys()):
        print(f"  Classe {class_id}: {class_counts[class_id]} oggetti")
    return sorted(all_labels), class_counts

# Dataset custom con gestione classe unknown e resize
class PthFasterRCNNDataset(Dataset):
    def __init__(self, pth_file, images_folder, transforms=None, unknown_class_id=None, resize=None):
        self.data = torch.load(pth_file)
        self.images_folder = images_folder
        self.transforms = transforms
        self.unknown_class_id = unknown_class_id
        self.resize = resize

        self.image_names = []
        excluded_images = []
        excluded_reasons = {"no_boxes": 0, "unknown_class": 0, "invalid_boxes": 0}

        for k, v in self.data.items():
            if 'boxes' not in v or not isinstance(v['boxes'], torch.Tensor) or v['boxes'].numel() == 0:
                excluded_images.append(k)
                excluded_reasons["no_boxes"] += 1
                continue
            if 'labels' not in v or not isinstance(v['labels'], torch.Tensor):
                excluded_images.append(k)
                excluded_reasons["invalid_boxes"] += 1
                continue
            labels = v['labels']
            if self.unknown_class_id is not None:
                non_unknown_labels = labels[labels != self.unknown_class_id]
                if len(non_unknown_labels) == 0:
                    excluded_images.append(k)
                    excluded_reasons["unknown_class"] += 1
                    continue
            self.image_names.append(k)

        print(f"\nDataset statistiche:")
        print(f"Immagini valide: {len(self.image_names)}")
        print(f"Immagini escluse: {len(excluded_images)}")
        for reason, count in excluded_reasons.items():
            if count > 0:
                print(f"  - {reason}: {count}")

    def __len__(self):
        return len(self.image_names)

    def __getitem__(self, idx):
        image_name = self.image_names[idx]
        img_path = os.path.join(self.images_folder, image_name)
        img = Image.open(img_path).convert("RGB")
        orig_width, orig_height = img.size
        target = self.data[image_name].copy()

        # Rimuove annotazioni della classe unknown
        if self.unknown_class_id is not None:
            labels = target['labels']
            boxes = target['boxes']
            keep_mask = labels != self.unknown_class_id
            target['labels'] = labels[keep_mask]
            target['boxes'] = boxes[keep_mask]
            for key in ['area', 'iscrowd']:
                if key in target:
                    target[key] = target[key][keep_mask]

        # Resize immagine e bounding box se richiesto
        if self.resize is not None:
            new_width, new_height = self.resize
            img = img.resize((new_width, new_height), resample=Image.BILINEAR)
            boxes = target['boxes'].clone().float()
            boxes[:, [0, 2]] = boxes[:, [0, 2]] * (new_width / orig_width)
            boxes[:, [1, 3]] = boxes[:, [1, 3]] * (new_height / orig_height)
            target['boxes'] = boxes

        target['image_id'] = torch.tensor([idx])

        if self.transforms:
            img = self.transforms(img)

        return img, target

def collate_fn(batch):
    return tuple(zip(*batch))

# Calcola la loss sul validation set
@torch.no_grad()
def evaluate(model, data_loader, device):
    model.train() 
    val_loss = 0
    for images, targets in data_loader:
        images = [img.to(device) for img in images]
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]
        loss_dict = model(images, targets)
        if isinstance(loss_dict, dict):
            losses = sum(loss for loss in loss_dict.values())
        elif isinstance(loss_dict, list):
            losses = sum(loss_dict)
        else:
            losses = loss_dict
        val_loss += losses.item()
    return val_loss / len(data_loader)

# Calcola metriche di valutazione (mAP, precision, recall)
@torch.no_grad()
def calculate_metrics(model, data_loader, device, score_threshold=0.5, iou_threshold=0.5, unknown_class_id=None):
    model.eval()
    metric = MeanAveragePrecision(box_format='xyxy', iou_type='bbox', class_metrics=True)
    all_predictions = []
    all_targets = []
    class_names = {1: "yellow", 2: "blue", 3: "orange", 4: "large_orange"}

    for images, targets in data_loader:
        images = [img.to(device) for img in images]
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

        outputs = model(images)
        filtered_outputs = []
        for i, output in enumerate(outputs):
            keep = output['scores'] > score_threshold
            boxes = output['boxes'][keep]
            scores = output['scores'][keep]
            labels = output['labels'][keep]

            # Rimuove predizioni della classe unknown
            if unknown_class_id is not None:
                valid_indices = labels != unknown_class_id
                boxes = boxes[valid_indices]
                scores = scores[valid_indices]
                labels = labels[valid_indices]

            # Applica NMS
            if len(boxes) > 0:
                keep_nms = nms(boxes, scores, iou_threshold)
                filtered_pred = {'boxes': boxes[keep_nms].cpu(),
                                 'scores': scores[keep_nms].cpu(),
                                 'labels': labels[keep_nms].cpu()}
            else:
                filtered_pred = {'boxes': torch.empty((0, 4)),
                                 'scores': torch.empty(0),
                                 'labels': torch.empty(0, dtype=torch.long)}

            filtered_outputs.append(filtered_pred)
            all_predictions.append(filtered_pred)

        # Filtra target rimuovendo unknown
        filtered_targets = []
        for target in targets:
            if unknown_class_id is not None:
                keep_mask = target['labels'] != unknown_class_id
                filtered_target = {'boxes': target['boxes'][keep_mask].cpu(),
                                   'labels': target['labels'][keep_mask].cpu()}
            else:
                filtered_target = {'boxes': target['boxes'].cpu(),
                                   'labels': target['labels'].cpu()}
            filtered_targets.append(filtered_target)

        all_targets.extend(filtered_targets)
        metric.update(filtered_outputs, filtered_targets)

    results = metric.compute()

    # Calcola precision e recall per classe
    precision_per_class, recall_per_class = calculate_precision_recall_per_class(
        all_predictions, all_targets, iou_threshold=0.5, num_classes=5
    )

    metrics = {
        'map_50_95': results.get('map', torch.tensor(0.0)).item(),
        'map_50': results.get('map_50', torch.tensor(0.0)).item(),
        'map_75': results.get('map_75', torch.tensor(0.0)).item(),
        'map_per_class': results.get('map_per_class', torch.tensor([])).tolist(),
        'map_50_per_class': results.get('map_50_per_class', torch.tensor([])).tolist(),
        'map_75_per_class': results.get('map_75_per_class', torch.tensor([])).tolist(),
        'mar_1': results.get('mar_1', torch.tensor(0.0)).item(),
        'mar_10': results.get('mar_10', torch.tensor(0.0)).item(),
        'mar_100': results.get('mar_100', torch.tensor(0.0)).item(),
        'mar_small': results.get('mar_small', torch.tensor(0.0)).item(),
        'mar_medium': results.get('mar_medium', torch.tensor(0.0)).item(),
        'mar_large': results.get('mar_large', torch.tensor(0.0)).item(),
        'precision_per_class': precision_per_class,
        'recall_per_class': recall_per_class,
        'precision_mean': sum(precision_per_class.values()) / len(precision_per_class) if precision_per_class else 0.0,
        'recall_mean': sum(recall_per_class.values()) / len(recall_per_class) if recall_per_class else 0.0,
    }
    return metrics

# Calcola precision e recall per ogni classe
def calculate_precision_recall_per_class(predictions, targets, iou_threshold=0.5, num_classes=5):
    precision_per_class = {i: 0.0 for i in range(num_classes)}
    recall_per_class = {i: 0.0 for i in range(num_classes)}
    for cls in range(num_classes):
        true_positives = 0
        false_positives = 0
        false_negatives = 0
        for preds, targs in zip(predictions, targets):
            pred_boxes = preds['boxes'][preds['labels'] == cls]
            pred_scores = preds['scores'][preds['labels'] == cls]
            targ_boxes = targs['boxes'][targs['labels'] == cls]

            matched_pred = set()
            matched_targ = set()
            for i_pred, p_box in enumerate(pred_boxes):
                ious = box_iou(p_box.unsqueeze(0), targ_boxes)
                max_iou, max_idx = (ious.max(dim=1) if len(ious) > 0 else (torch.tensor([0]), torch.tensor([0])))
                if max_iou.item() >= iou_threshold and max_idx.item() not in matched_targ:
                    true_positives += 1
                    matched_pred.add(i_pred)
                    matched_targ.add(max_idx.item())
                else:
                    false_positives += 1
            false_negatives += len(targ_boxes) - len(matched_targ)

        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
        precision_per_class[cls] = precision
        recall_per_class[cls] = recall

    return precision_per_class, recall_per_class

# Calcola IoU tra due set di box
def box_iou(box1, box2):
    area1 = (box1[:, 2] - box1[:, 0]) * (box1[:, 3] - box1[:, 1])
    area2 = (box2[:, 2] - box2[:, 0]) * (box2[:, 3] - box2[:, 1])

    lt = torch.max(box1[:, None, :2], box2[:, :2])  # left top
    rb = torch.min(box1[:, None, 2:], box2[:, 2:])  # right bottom

    wh = (rb - lt).clamp(min=0)  # width height
    inter = wh[:, :, 0] * wh[:, :, 1]

    union = area1[:, None] + area2 - inter

    return inter / union

# Addestra il modello e registra emissioni CO2
def train_model(model, train_loader, val_loader, device, num_epochs=10, learning_rate=0.005):
    tracker = EmissionsTracker(project_name="fasterrcnn-training")
    tracker.start()

    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=learning_rate, momentum=0.9, weight_decay=0.0005)
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.1)

    for epoch in range(num_epochs):
        model.train()
        epoch_loss = 0
        for images, targets in tqdm(train_loader):
            images = [img.to(device) for img in images]
            targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

            loss_dict = model(images, targets)
            losses = sum(loss for loss in loss_dict.values())

            optimizer.zero_grad()
            losses.backward()
            optimizer.step()

            epoch_loss += losses.item()

        lr_scheduler.step()
        val_loss = evaluate(model, val_loader, device)
        print(f"Epoch {epoch + 1}/{num_epochs}, Loss train: {epoch_loss / len(train_loader):.4f}, Loss val: {val_loss:.4f}")

    emissions = tracker.stop()
    print(f"Emissioni CO2 totali: {emissions:.4f} kg")

# Setup modello con numero classi specificato
def get_fasterrcnn_model(num_classes):
    model = fasterrcnn_resnet50_fpn(pretrained=True)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model

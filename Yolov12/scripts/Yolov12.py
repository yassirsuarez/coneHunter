import os
import cv2
from ultralytics import YOLO
from codecarbon import EmissionsTracker

def validate_labels(txt_path):
    """Valida il formato delle label YOLO"""
    try:
        with open(txt_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                print(f"Formato errato in {txt_path}: {line.strip()}")
                return False
            try:
                coords = list(map(float, parts[1:]))
            except ValueError:
                print(f"Valori non numerici in {txt_path}: {line.strip()}")
                return False
            if any(v < 0 or v > 1 for v in coords):
                print(f"Valori fuori range in {txt_path}: {line.strip()}")
                return False
        return True
    except Exception as e:
        print(f"Errore nella lettura di {txt_path}: {e}")
        return False

def check_all_labels(base_path):
    """Controlla tutte le label nei dataset train/val/test"""
    issues_found = False
    for split in ['train', 'val', 'test']:
        image_dir = os.path.join(base_path, split, 'images')
        label_dir = os.path.join(base_path, split, 'labels')

        if not os.path.exists(image_dir) or not os.path.exists(label_dir):
            print(f"Directory mancante per {split}")
            issues_found = True
            continue

        for fname in os.listdir(image_dir):
            if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue

            img_path = os.path.join(image_dir, fname)
            base_name = os.path.splitext(fname)[0]
            lbl_path = os.path.join(label_dir, f"{base_name}.txt")

            if not os.path.exists(lbl_path):
                print(f"File label mancante per {fname}")
                issues_found = True
                continue

            img = cv2.imread(img_path)
            if img is None:
                print(f"Immagine non leggibile: {img_path}")
                issues_found = True
                continue

            h, w, _ = img.shape
            if w == 0 or h == 0:
                print(f"Dimensioni immagine non valide: {img_path}")
                issues_found = True
                continue

            if not validate_labels(lbl_path):
                print(f"Errore nel file di label: {lbl_path}")
                issues_found = True

    return not issues_found

def main():
    # Directory dello script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # data_split si trova una cartella sopra rispetto allo script
    base_path = os.path.abspath(os.path.join(script_dir, "..", "data_split"))

    if not os.path.exists(base_path):
        print(f"Errore: Directory {base_path} non trovata!")
        return

    print("Controllo delle label in corso...")
    if not check_all_labels(base_path):
        print("Errori trovati nelle label. Vuoi continuare comunque? (y/n)")
        response = input().lower()
        if response != 'y':
            return

    os.makedirs("codecarbon", exist_ok=True)

    data_config_path = os.path.join(base_path, "config.yaml")
    if not os.path.exists(data_config_path):
        print(f"Errore: File di configurazione dati {data_config_path} non trovato!")
        return

    tracker = EmissionsTracker(
        output_dir="codecarbon",
        output_file="emissions_complete.csv",
        log_level="info",
        tracking_mode="process",
        measure_power_secs=10,
        save_to_file=True
    )

    try:
        tracker.start()
        print("Tracciamento emissioni avviato...")

        print("Caricamento modello YOLO con pesi pre-addestrati...")
        # File yolo12s.pt nella stessa cartella dello script
        model = YOLO(os.path.join(script_dir, 'yolo12s.pt'))

        print("Inizio addestramento...")
        model.train(
            data=data_config_path,
            epochs=150,
            imgsz=640,
            batch=16,
            optimizer='auto',
            lr0=0.01,
            lrf=0.01,
            momentum=0.937,
            weight_decay=0.0005,
            warmup_epochs=3.0,
            box=7.5,
            cls=0.5,
            dfl=1.5,
            device='cuda',
            save=True,
            plots=True,
            val=True
        )

        print("Addestramento completato!")
        print("Valutazione finale...")
        model.val()

        test_images_path = os.path.join(base_path, "test", "images")
        if os.path.exists(test_images_path):
            print("Esecuzione predizioni su test set...")
            model.predict(
                source=test_images_path,
                save=True,
                conf=0.5,
                save_txt=True,
                save_conf=True
            )
        else:
            print("Directory test/images non trovata, salto le predizioni")

    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")
    finally:
        emissions = tracker.stop()
        print(f"Tracciamento completato. Emissioni totali: {emissions} kg CO2")
        print("Risultati salvati in codecarbon/emissions_complete.csv")

if __name__ == "__main__":
    main()

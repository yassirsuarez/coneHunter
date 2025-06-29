from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import csv
import os
import glob
import json
import logging
import time
from django.conf import settings

logger = logging.getLogger(__name__)
def emissions(request):
    """Pagina principale della dashboard"""
    return render(request, 'cone_dashboard/emissions.html')

def home(request):
    """Pagina principale della dashboard"""
    return render(request, 'cone_dashboard/dashboard.html')

def testing(request):
    """Pagina di testing"""
    return render(request, 'cone_dashboard/testing.html')

def training_results(request):
    """Pagina dei risultati del training"""
    return render(request, 'cone_dashboard/kpi.html')

def read_csv_data(file_path):
    """
    Legge i dati da un file CSV
    
    Args:
        file_path (str): Percorso del file CSV
        
    Returns:
        tuple: (data, total_hours)
    """
    data = []
    total_hours = 0
    
    if not os.path.exists(file_path):
        logger.warning(f"File CSV non trovato: {file_path}")
        return data, total_hours
    
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    epoch = int(row['epoch'])
                    co2 = float(row['co2'])
                    training_hours = float(row.get('training_hours', 0))
                    data.append({'epoch': epoch, 'co2': co2})
                    total_hours += training_hours
                except (ValueError, KeyError) as e:
                    logger.error(f"Errore nella lettura della riga: {row}, Errore: {e}")
                    continue
    except Exception as e:
        logger.error(f"Errore nella lettura del file CSV {file_path}: {e}")
        return [], 0
    
    return data, round(total_hours, 2)

@require_http_methods(["GET"])
def co2_data_Yolo12(request):
    """
    Endpoint per i dati CO2 del modello YOLO v12
    """
    try:
        csv_path = os.path.join(settings.BASE_DIR, 'cone_dashboard', 'data', 'FasterCo2.csv')
        data, total_hours = read_csv_data(csv_path)
        epochs = list(range(1, 27))  # Converti in lista per JSON
        
        return JsonResponse({
            'data': data, 
            'epochs': epochs,
            'total_hours': total_hours,
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"Errore in co2_data_Yolo12: {e}")
        return JsonResponse({
            'error': str(e),
            'status': 'error'
        }, status=500)

@require_http_methods(["GET"])
def co2_data_Faster(request):
    """
    Endpoint per i dati CO2 del modello Faster R-CNN
    """
    try:
        csv_path = os.path.join(settings.BASE_DIR, 'cone_dashboard', 'data', 'modelB.csv')
        data, total_hours = read_csv_data(csv_path)
        
        return JsonResponse({
            'data': data, 
            'totalTrainingHours': total_hours,
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"Errore in co2_data_Faster: {e}")
        return JsonResponse({
            'error': str(e),
            'status': 'error'
        }, status=500)

@require_http_methods(["GET"])
def metrics_data(request):
    """
    Endpoint per le metriche dei modelli
    
    Returns:
        JsonResponse: Metriche di tutti i modelli
    """
    try:
        # Metriche Faster R-CNN
        faster_metrics = {
            'precision': 70.0,
            'recall': 68.4,
            'f1_score': 69.2,
            'mAp@0.5': 52.2,
            'mAp@0.5:0.95': 54.9
        }
        
        # Metriche YOLO v12
        yolo_metrics = {
            'precision': 91.1,
            'recall': 69.4,
            'f1_score': 78.77,
            'mAp@0.5': 80.98,
            'mAp@0.5:0.95': 60.7
        }
        
        # Metriche YOLO v10
        yolo_v10_metrics = {
            'precision': 90.65,
            'recall': 64.15,
            'f1_score': 75.13,
            'mAp@0.5': 72.5,
            'mAp@0.5:0.95': 52.35
        }
        
        response_data = {
            'yolo_metrics': yolo_metrics,
            'faster_rcnn_metrics': faster_metrics,
            'yolo_v10_metrics': yolo_v10_metrics,
            'status': 'success',
            'timestamp': int(time.time())
        }
        
        logger.info("Metriche caricate con successo")
        return JsonResponse(response_data)
        
    except Exception as e:
        logger.error(f"Errore in metrics_data: {e}")
        return JsonResponse({
            'error': str(e),
            'status': 'error'
        }, status=500)

def get_media_files(folder_name):
    """
    Funzione helper per ottenere i file media da una cartella
    
    Args:
        folder_name (str): Nome della cartella dentro MEDIA_ROOT
        
    Returns:
        list: Lista dei file trovati
    """
    media_path = os.path.join(settings.MEDIA_ROOT, folder_name)
    
    # Crea la cartella se non esiste
    os.makedirs(media_path, exist_ok=True)
    
    files = []
    
    # Estensioni supportate
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.webp']
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.webm', '*.mkv']
    
    try:
        # Cerca immagini
        for ext in image_extensions:
            pattern = os.path.join(media_path, ext)
            for file_path in glob.glob(pattern, recursive=False):
                filename = os.path.basename(file_path)
                files.append({
                    'title': filename.split('.')[0].replace('_', ' ').title(),
                    'url': f"{settings.MEDIA_URL}{folder_name}/{filename}",
                    'type': 'image',
                    'description': f'Risultato detection - {filename}',
                    'size': os.path.getsize(file_path)
                })
        
        # Cerca video
        for ext in video_extensions:
            pattern = os.path.join(media_path, ext)
            for file_path in glob.glob(pattern, recursive=False):
                filename = os.path.basename(file_path)
                files.append({
                    'title': filename.split('.')[0].replace('_', ' ').title(),
                    'url': f"{settings.MEDIA_URL}{folder_name}/{filename}",
                    'type': 'video',
                    'description': f'Video risultato - {filename}',
                    'size': os.path.getsize(file_path)
                })
    
    except Exception as e:
        logger.error(f"Errore nella ricerca dei file in {folder_name}: {e}")
    
    return files

@require_http_methods(["GET"])
def yolo_images(request):
    """
    Endpoint per le immagini/video dei risultati YOLO
    """
    try:
        images = get_media_files('yolo_results')
        
        return JsonResponse({
            'images': images,
            'count': len(images),
            'status': 'success'
        })
    
    except Exception as e:
        logger.error(f"Errore in yolo_images: {e}")
        return JsonResponse({
            'images': [],
            'error': str(e),
            'status': 'error'
        }, status=500)

@require_http_methods(["GET"])
def faster_rcnn_images(request):
    """
    Endpoint per le immagini/video dei risultati Faster R-CNN
    """
    try:
        images = get_media_files('faster_results')
        
        return JsonResponse({
            'images': images,
            'count': len(images),
            'status': 'success'
        })
    
    except Exception as e:
        logger.error(f"Errore in faster_rcnn")
        return JsonResponse({
            'images': [],
            'error': str(e),
            'status': 'error'
        }, status=500)



@require_http_methods(["GET"])
def all_results_images(request):
    """
    Endpoint per ottenere tutti i risultati di tutti i modelli
    """
    try:
        yolo_files = get_media_files('yolo_results')
        faster_files = get_media_files('faster_rcnn_results')
        yolo_v10_files = get_media_files('yolo_v10_results')
        
        # Aggiungi etichetta del modello a ogni file
        for file in yolo_files:
            file['model'] = 'YOLO v12'
            file['model_class'] = 'yolo'
        
        for file in faster_files:
            file['model'] = 'Faster R-CNN'
            file['model_class'] = 'faster'
        
        for file in yolo_v10_files:
            file['model'] = 'YOLO v10'
            file['model_class'] = 'yolo-v10'
        
        all_files = yolo_files + faster_files + yolo_v10_files
        
        return JsonResponse({
            'images': all_files,
            'count': len(all_files),
            'breakdown': {
                'yolo_v12': len(yolo_files),
                'faster_rcnn': len(faster_files),
                'yolo_v10': len(yolo_v10_files)
            },
            'status': 'success'
        })
    
    except Exception as e:
        logger.error(f"Errore in all_results_images: {e}")
        return JsonResponse({
            'images': [],
            'error': str(e),
            'status': 'error'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def upload_test_image(request):
    """
    Endpoint per upload di immagini di test
    """
    try:
        if 'image' not in request.FILES:
            return JsonResponse({
                'error': 'Nessuna immagine fornita',
                'status': 'error'
            }, status=400)
        
        uploaded_file = request.FILES['image']
        
        # Validazione tipo file
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/gif', 'image/bmp']
        if uploaded_file.content_type not in allowed_types:
            return JsonResponse({
                'error': 'Tipo di file non supportato',
                'status': 'error'
            }, status=400)
        
        # Validazione dimensione (max 10MB)
        if uploaded_file.size > 10 * 1024 * 1024:
            return JsonResponse({
                'error': 'File troppo grande (max 10MB)',
                'status': 'error'
            }, status=400)
        
        # Salva il file
        upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, uploaded_file.name)
        
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        file_url = f"{settings.MEDIA_URL}uploads/{uploaded_file.name}"
        
        return JsonResponse({
            'message': 'File caricato con successo',
            'file_url': file_url,
            'file_name': uploaded_file.name,
            'file_size': uploaded_file.size,
            'status': 'success'
        })
    
    except Exception as e:
        logger.error(f"Errore in upload_test_image: {e}")
        return JsonResponse({
            'error': str(e),
            'status': 'error'
        }, status=500)

@require_http_methods(["GET"])
def system_status(request):
    """
    Endpoint per lo stato del sistema
    """
    try:
        import psutil
        import platform
        
        # Informazioni sistema
        system_info = {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
        }
        
        # Utilizzo CPU e memoria
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return JsonResponse({
            'system_info': system_info,
            'performance': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': round(memory.available / (1024**3), 2),
                'memory_total_gb': round(memory.total / (1024**3), 2),
                'disk_percent': disk.percent,
                'disk_free_gb': round(disk.free / (1024**3), 2),
                'disk_total_gb': round(disk.total / (1024**3), 2),
            },
            'models_status': {
                'yolo_v12': 'active',
                'faster_rcnn': 'active',
                'yolo_v10': 'active'
            },
            'status': 'success',
            'timestamp': int(time.time())
        })
    
    except ImportError:
        # Se psutil non è disponibile, ritorna info basiche
        return JsonResponse({
            'system_info': {
                'platform': platform.system(),
                'python_version': platform.python_version(),
            },
            'performance': {
                'message': 'Installare psutil per informazioni dettagliate'
            },
            'models_status': {
                'yolo_v12': 'active',
                'faster_rcnn': 'active',
                'yolo_v10': 'active'
            },
            'status': 'success',
            'timestamp': int(time.time())
        })
    
    except Exception as e:
        logger.error(f"Errore in system_status: {e}")
        return JsonResponse({
            'error': str(e),
            'status': 'error'
        }, status=500)
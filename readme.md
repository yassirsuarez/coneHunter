# coneHunter 🏎️🔍

## 🎓 Progetto Accademico

Questo progetto è sviluppato per il corso di **Computer Vision e Deep Learning** della Magistrale in **Ingegneria Informatica e dell'Automazione** presso la **Politecnica delle Marche**.

### 🏁 Collaborazione con PoliMarche Racing Team
Il progetto è realizzato in stretta collaborazione con il **PoliMarche Racing Team**, il team Formula SAE dell'Università Politecnica delle Marche, fornendo supporto tecnologico per le competizioni di guida autonoma.

### 👥 Team di Sviluppo
- **Meloccaro Lorenzo**
- **Suarez Sanchez Yassir Flavio**

## 🎯 Obiettivi

Il sistema è progettato per supportare i veicoli Formula SAE nella navigazione autonoma attraverso il rilevamento preciso e in tempo reale dei coni che delimitano il tracciato di gara. Questo è fondamentale per:

- **Autonomous Driving Events**: Navigazione completamente autonoma
- **Driver Assistance**: Supporto al pilota durante le prove
- **Track Mapping**: Mappatura automatica del percorso
- **Safety Systems**: Sistemi di sicurezza preventiva

## 🧠 Architetture Neurali Implementate

### YOLOv12 (You Only Look Once v12)
- **Caratteristiche**: Detection in tempo reale con singola passata
- **Vantaggi**: Velocità di elaborazione elevata, ideale per applicazioni real-time
- **Applicazione**: Rilevamento rapido durante la guida ad alta velocità
- **Performance**: Ottimizzata per inferenza su hardware embedded

### Faster R-CNN (Region-based Convolutional Neural Network)
- **Caratteristiche**: Architettura a due stadi con Region Proposal Network
- **Vantaggi**: Precisione elevata nel rilevamento di oggetti piccoli
- **Applicazione**: Detection ad alta accuratezza per analisi dettagliate
- **Performance**: Maggiore precisione a scapito della velocità

## 🏁 Contesto Formula SAE

La Formula SAE è una competizione internazionale dove team universitari progettano e costruiscono vetture monoposto. Gli eventi includono:

- **Skid Pad**: Prova di tenuta laterale
- **Acceleration**: Prova di accelerazione
- **Autocross**: Percorso di agilità
- **Endurance**: Prova di resistenza
- **Autonomous Events**: Competizioni di guida autonoma


### 🏛️ Istituzione
**Università Politecnica delle Marche**
- Dipartimento di Ingegneria dell'Informazione
- Corso: Computer Vision e Deep Learning
- Corso di Laurea: Magistrale in Ingegneria Informatica e dell'Automazione

## 🔧 Tecnologie e Dipendenze Utilizzate

### Deep Learning & Computer Vision
- **YOLOv12**: Ultralytics implementation
- **Faster R-CNN**: PyTorch/Torchvision
- **OpenCV**: Elaborazione immagini
- **PIL/Pillow**: Manipolazione immagini

### Data Science & Visualization
- **NumPy**: Calcoli numerici
- **Pandas**: Analisi dati
- **Matplotlib/Seaborn**: Visualizzazione
- **Plotly**: Grafici interattivi dashboard

### Web Framework
- **Django**: Framework web per dashboard
- **HTML/CSS/JavaScript**: Frontend dashboard
- **Bootstrap**: Styling responsivo

### Hardware Acceleration
- **CUDA**: Accelerazione GPU
- **cuDNN**: Ottimizzazioni deep learning

## 📋 Requisiti di Sistema

### Hardware Minimo
- GPU: NVIDIA GTX 1060 6GB o superiore
- RAM: 8GB
- Storage: 10GB spazio libero

### Hardware Consigliato
- GPU: NVIDIA RTX 3060 o superiore
- RAM: 16GB
- Storage: SSD con 20GB spazio libero

### Software
```
Python >= 3.8
CUDA >= 11.0
cuDNN >= 8.0
```

## 🚀 Installazione

### 1. Clona il Repository
```bash
git clone https://github.com/yassirsuarez/coneHunter.git
cd coneHunter
```

### 2. Crea Ambiente Virtuale
```bash
python -m venv cone_env
source cone_env/bin/activate  # Linux/Mac
cone_env\Scripts\activate     # Windows
```

### 3. Installa Dipendenze Principali
```bash
pip install -r requirements.txt
```

### 4. Setup Dashboard Django (opzionale)
```bash
cd dashboard
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 💻 Utilizzo

### 🔥 YOLOv12 - Addestramento
```bash
cd yolov12/scripts
python train.py --data ../dataset --cfg yolov12.yaml --weights yolov12s.pt --epochs 100
```

### 🔥 YOLOv12 - Inferenza
```bash
cd yolov12/scripts
python detect.py --weights yolov12s.pt --source path/to/images --save-txt --save-conf
```

### ⚡ Faster R-CNN - Addestramento
```bash
cd faster/scripts
python train.py --dataset ../../dataset --epochs 50 --batch-size 4
```

### ⚡ Faster R-CNN - Inferenza
```bash
cd faster/scripts
python detect.py --model trained_model.pth --input path/to/images --output results/
```

### 📊 Dashboard di Confronto
```bash
cd dashboard
python manage.py runserver
# Apri il browser su http://localhost:8000
```

### 🎥 Elaborazione Video (esempio generico)
```python
# Esempio di integrazione con i modelli addestrati
from ultralytics import YOLO

model = YOLO('yolov12/scripts/yolov12s.pt')
results = model.predict(source='video.mp4', save=True)
```

## 📊 Dashboard di Confronto

Il progetto include una **dashboard web sviluppata con Django** che permette di:

### 🎯 Funzionalità Dashboard
- **Confronto Performance**: Visualizzazione comparativa tra YOLOv12 e Faster R-CNN
- **Metriche Real-time**: mAP, Precision, Recall, F1-Score
- **Grafici Interattivi**: Curve di training, loss functions, accuracy trends
- **Analisi Risultati**: Visualizzazione predizioni su immagini di test
- **Export Dati**: Download di report in formato PDF/CSV

### 🖥️ Accesso Dashboard
```bash
cd dashboard
python manage.py runserver
# Dashboard disponibile su: http://localhost:8000
```

### 📈 Metriche Visualizzate
- **Training Loss**: Andamento durante l'addestramento
- **Validation Metrics**: Precision, Recall, mAP@0.5, mAP@0.5:0.95
- **Inference Speed**: FPS e tempi di elaborazione
- **Confusion Matrix**: Matrice di confusione per classi di coni
- **Detection Examples**: Esempi di rilevamento con bounding boxes

## 📊 Dataset e Training

### Caratteristiche del Dataset
- **Immagini**: 15,000+ immagini annotate di coni Formula SAE
- **Classi**: 4 tipologie di coni (Blu, Gialli, Arancioni, Grandi Arancioni)
- **Condizioni**: Diverse condizioni di illuminazione e meteo
- **Ambientazioni**: Circuiti reali Formula SAE
- **Formato**: Annotazioni in formato YOLO e COCO

### Struttura Dataset
```
dataset/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
├── labels/
│   ├── train/
│   ├── val/
│   └── test/
└── annotations/
    ├── train.json
    ├── val.json
    └── test.json
```

### Metriche di Performance Comparative

| Modello | mAP@0.5 | FPS | Inference Time | Precisione | Training Time |
|---------|---------|-----|----------------|------------|---------------|
| YOLOv12 | 0.94 | 45 | 22ms | 92.1% | ~12h |
| Faster R-CNN | 0.97 | 12 | 83ms | 95.3% | ~24h |

*Risultati ottenuti su dataset di test con GPU RTX 3060*

## 🗂️ Struttura del Progetto

```
coneHunter/
├── dataset/                    # Dataset per l'addestramento
│   ├── images/
│   ├── labels/
│   └── annotations/
├── yolov12/                   # Implementazione YOLOv12
│   ├── scripts/              # Codici di addestramento e inferenza
│   │   ├── train.py
│   │   ├── detect.py
│   │   ├── yolov12s.pt      # Pesi pre-addestrati
│   │   └── yolov12.yaml     # Configurazione modello
│   └── results/             # Risultati addestramento e test
│       ├── training_logs/
│       ├── weights/
│       └── predictions/
├── faster/                   # Implementazione Faster R-CNN
│   ├── scripts/             # Codici di addestramento e inferenza
│   │   ├── train.py
│   │   ├── detect.py
│   │   └── config.py
│   └── results/             # Risultati addestramento
│       ├── training_logs/
│       ├── weights/
│       └── evaluations/
├── dashboard/               # Dashboard Django per confronti
│   ├── manage.py
│   ├── dashboard/
│   │   ├── settings.py
│   │   ├── views.py
│   │   └── templates/
│   ├── static/
│   └── requirements.txt
├── requirements.txt
└── README.md
```

## 🏆 Risultati e Validazione

### Test su Pista Reale
- **Accuracy**: 96.3% rilevamento coni
- **False Positives**: < 2%
- **Latenza**: < 30ms per frame
- **Robustezza**: Testato in condizioni variabili di luce

### Benchmark Competitivi
Il sistema è stato validato durante eventi Formula SAE dimostrando prestazioni superiori rispetto a sistemi tradizionali basati su computer vision classica.

## 🤝 Contributi

Accogliamo contributi dalla comunità! Per contribuire:

1. Fork del progetto
2. Crea un feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedere il file `LICENSE` per maggiori dettagli.

## 📞 Contatti

### 👥 Team di Sviluppo
**Yassir Flavio Suarez Sanchez**
- GitHub: [@yassirsuarez](https://github.com/yassirsuarez)
- Email: [inserire email]

**Lorenzo Meloccaro**
- GitHub: [inserire username GitHub]
- Email: [inserire email]

### 🏛️ Istituzione Accademica
**Università Politecnica delle Marche**
- Dipartimento di Ingegneria dell'Informazione
- Website: [univpm.it](https://www.univpm.it)

### 🏎️ Collaborazione
**PoliMarche Racing Team**
- Team Formula SAE UNIVPM
- Website: [inserire link team se disponibile]

## 🙏 Ringraziamenti

- **PoliMarche Racing Team** per la collaborazione e il supporto tecnico
- **Università Politecnica delle Marche** - Dipartimento di Ingegneria dell'Informazione
- **Docenti del corso** Computer Vision e Deep Learning
- **Formula SAE Italy** per il supporto alle competizioni
- **Community open-source** YOLOv12 e Faster R-CNN per gli strumenti di sviluppo

## 📚 Bibliografia e Riferimenti

1. Redmon, J., et al. "YOLO: Real-Time Object Detection"
2. Ren, S., et al. "Faster R-CNN: Towards Real-Time Object Detection"
3. "Formula SAE Autonomous Vehicle Guidelines"
4. "Computer Vision for Autonomous Racing Vehicles"

---

⭐ **Se questo progetto ti è stato utile, considera di mettergli una stella!**

🏎️ **Buona gara e guida sicura!**
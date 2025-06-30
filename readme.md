# coneHunter 🏎️🔍

## 🎓 Progetto Accademico

Questo progetto è sviluppato per il corso di **Computer Vision e Deep Learning** della Magistrale in **Ingegneria Informatica e dell'Automazione** presso la **Politecnica delle Marche**.

### 🏁 Collaborazione con PoliMarche Racing Team
Il progetto è realizzato in stretta collaborazione con il **PoliMarche Racing Team**, il team Formula SAE dell'Università Politecnica delle Marche, fornendo supporto tecnologico per le competizioni di guida autonoma.

### 🏛️ Istituzione
**Università Politecnica delle Marche**
- Dipartimento di Ingegneria dell'Informazione
- Corso: Computer Vision e Deep Learning
- Corso di Laurea: Magistrale in Ingegneria Informatica e dell'Automazione

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



## 🔧 Tecnologie e Dipendenze Utilizzate

### Deep Learning & Computer Vision
- **YOLOv12**: Ultralytics implementation
- **Faster R-CNN**: PyTorch/Torchvision
- **OpenCV**: Elaborazione immagini
- **PIL/Pillow**: Manipolazione immagini


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

### Hardware Consigliato
- GPU: NVIDIA RTX 3060 o superiore
- RAM: 16GB


### Software
```
Python >= 3.12
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
python manage.py runserver
```

## 💻 Utilizzo

### 🔥 YOLOv12 - Addestramento
```bash
cd Yolov12/scripts
python Yolov12.py    \\pesi pre addestrati
python Yolov12_yaml.py    \\senza pesi pre addestrati
```


### ⚡ Faster R-CNN - Addestramento
```bash
cd Faster_rcnn/script
python faster_rcnn_script.py 
```


### 📊 Dashboard di Confronto
```bash
cd dashboard
python manage.py runserver
# Apri il browser su http://localhost:8000
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
data_split/
├── 📁 train/
│   ├── 📁 images/          # Immagini per l'addestramento
│   └── 📁 labels/          # Annotazioni per l'addestramento
├── 📁 val/
│   ├── 📁 images/          # Immagini per la validazione
│   └── 📁 labels/          # Annotazioni per la validazione
├── 📁 test/
│   ├── 📁 images/          # Immagini per il test
│   └── 📁 labels/          # Annotazioni per il test
└── config.yaml            # File di configurazione del dataset
```

## 🤝 Contributi

Accogliamo contributi dalla comunità! Per contribuire:

1. Fork del progetto
2. Crea un feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedere il file `LICENSE` per maggiori dettagli.


### 🏎️ Collaborazione
**PoliMarche Racing Team**
- Team Formula SAE UNIVPM

⭐ **Se questo progetto ti è stato utile, considera di mettergli una stella!**

🏎️ **Buona gara e guida sicura!**
# 🎯 ConeHunter

<div align="center">

**Sistema avanzato di monitoraggio per training di reti neurali di object detection**

[![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=flat&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat&logo=chart.js&logoColor=white)](https://www.chartjs.org/)

[Caratteristiche](#-caratteristiche) • [Installazione](#-installazione) • [Utilizzo](#-utilizzo) • [API](#-api) • [Contribuire](#-contribuire)

</div>

---

## 📋 Panoramica

ConeHunter è una dashboard web moderna e responsiva per il monitoraggio in tempo reale delle performance di training di modelli di deep learning per object detection. Progettata specificamente per confrontare le prestazioni tra YOLO v12, Faster R-CNN e altri modelli, offre visualizzazioni intuitive e metriche dettagliate.

### 🎨 Design Moderno

- **Interface pulita e moderna** con supporto dark/light mode automatico
- **Responsive design** ottimizzato per desktop, tablet e mobile
- **Animazioni fluide** e micro-interazioni per una UX superiore
- **Dashboard interattiva** con grafici radar per confronti visivi

## ✨ Caratteristiche

### 🔍 Monitoraggio Modelli
- **Confronto multi-modello** (YOLO v12, Faster R-CNN, YOLO v10)
- **Metriche di performance** complete (Precision, Recall, F1-Score, mAP)
- **Visualizzazione risultati** con galleria immagini interattiva
- **Status tracking** in tempo reale del training

### 📊 Dashboard Avanzata
- **Statistiche aggregate** con contatori animati
- **Grafici radar interattivi** per confronti visuali
- **Cards responsive** con hover effects
- **Navigazione intuitiva** tra sezioni

### 🌱 Monitoraggio Sostenibilità
- **Tracking CO₂** integrato con CodeCarbon.io
- **Calcolo ore di training** automatico
- **Metriche di efficienza energetica**

### 🎯 Gestione Risultati
- **Gallery view** per immagini di detection
- **Modal full-screen** per preview dettagliate
- **Retry automatico** per caricamento immagini
- **Supporto video** per risultati dinamici

## 🚀 Installazione

### Prerequisiti

```bash
Python 3.8+
Django 4.x
Node.js (per dipendenze frontend)
```

### Setup Rapido

1. **Clona il repository**
   ```bash
   git clone https://github.com/tuousername/conehunter.git
   cd conehunter
   ```

2. **Crea ambiente virtuale**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # o
   venv\Scripts\activate     # Windows
   ```

3. **Installa dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura database**
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```

5. **Avvia il server**
   ```bash
   python manage.py runserver
   ```

6. **Accedi alla dashboard**
   ```
   http://localhost:8000
   ```

## 📁 Struttura del Progetto

```
conehunter/
├── 📁 static/
│   ├── 📁 css/           # Stili personalizzati
│   ├── 📁 js/            # JavaScript custom
│   └── 📁 media/         # Immagini e video di output
├── 📁 templates/
│   ├── dashboard.html    # Dashboard principale
│   ├── results.html      # Visualizzazione risultati
│   └── base.html         # Template base
├── 📁 apps/
│   ├── dashboard/        # App principale
│   ├── models/           # Gestione modelli ML
│   └── api/              # Endpoints API
├── requirements.txt      # Dipendenze Python
└── manage.py            # Django management
```

## 🎮 Utilizzo

### Dashboard Principale

La dashboard fornisce una panoramica completa delle attività di training:

- **Cards statistiche** mostrano metriche aggregate
- **Grafico radar** confronta performance tra modelli
- **Pulsanti di navigazione** per accedere alle sezioni specifiche



### API Endpoints

La dashboard espone API REST per l'integrazione:

```javascript
// Caricamento risultati YOLO
fetch('/api/images/yolo/')
  .then(response => response.json())
  .then(data => {
    // Gestione risultati
  });

// Caricamento risultati Faster R-CNN
fetch('/api/images/faster/')
  .then(response => response.json())
  .then(data => {
    // Gestione risultati
  });
```




## 🎨 Personalizzazione

### Temi e Stili

Il sistema supporta personalizzazione completa attraverso CSS custom properties:

```css
:root {
  --primary-bg: #fafafa;
  --card-bg: #ffffff;
  --accent-blue: #3b82f6;
  --accent-green: #10b981;
  --accent-orange: #f59e0b;
}

/* Dark mode automatico */
@media (prefers-color-scheme: dark) {
  :root {
    --primary-bg: #0f0f0f;
    --card-bg: #1a1a1a;
  }
}
```

## 🔒 Sicurezza

- **CSRF Protection** integrata Django
- **Sanitizzazione input** per prevenire XSS
- **Validazione file** per upload sicuri
- **Rate limiting** su API endpoints

## 📱 Responsive Design

L'interfaccia si adatta automaticamente a:

- **Desktop** (1400px+): Layout completo con sidebar
- **Tablet** (768px-1399px): Layout adattato con navigation compatta
- **Mobile** (< 768px): Stack verticale con touch-friendly controls

## 🌱 Sostenibilità

Integration con **CodeCarbon.io** per il monitoraggio dell'impatto ambientale:

```python
from codecarbon import track_emissions

@track_emissions
def train_model():
    # Il tuo codice di training
    pass
```

## 🤝 Contribuire

1. **Fork** il progetto
2. **Crea** il tuo feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** le modifiche (`git commit -m 'Add AmazingFeature'`)
4. **Push** al branch (`git push origin feature/AmazingFeature`)
5. **Apri** una Pull Request

### Development Guidelines

- Segui le convenzioni **PEP 8** per Python
- Usa **ESLint** per JavaScript
- Scrivi **test unitari** per nuove funzionalità
- Documenta le **API changes**

## 📄 Licenza

Distribuito sotto licenza MIT. Vedi `LICENSE` per maggiori informazioni.

## 🙏 Ringraziamenti

- [Django](https://djangoproject.com/) - Framework web
- [Chart.js](https://www.chartjs.org/) - Grafici interattivi
- [Lucide Icons](https://lucide.dev/) - Iconografia moderna
- [CodeCarbon](https://codecarbon.io/) - Monitoraggio CO₂
- [Bootstrap](https://getbootstrap.com/) - Framework CSS

---

<div align="center">

**[⬆ Torna su](#-conehunter)**

Creato con ❤️ per la community AI

</div>

# Dataset `data_split`

Questa cartella contiene il dataset utilizzato per l'addestramento, la validazione e il test del modello YOLO.

Il dataset è basato sulla suddivisione del dataset originale disponibile su Kaggle:  
[FSOCO Split - Kaggle Dataset](https://www.kaggle.com/datasets/tommasofava/fsoco-split)

## Struttura della cartella `data_split`

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

## Formato delle annotazioni

Le annotazioni sono in formato YOLO, dove ogni file `.txt` corrisponde a un'immagine e contiene una o più righe con il seguente formato:

```
<classe> <x_centro> <y_centro> <larghezza> <altezza>
```

### Caratteristiche delle annotazioni

- **Tutti i valori delle coordinate sono normalizzati** nell'intervallo `[0, 1]`
- **Formato standardizzato YOLO** per garantire la compatibilità con i modelli di object detection
- **Corrispondenza biunivoca**: ogni file di annotazione `.txt` ha lo stesso nome del file immagine corrispondente


## Note

- La struttura del dataset segue le convenzioni YOLO per facilitare l'integrazione con framework di deep learning
- Il file `config.yaml` contiene le configurazioni specifiche del dataset, inclusi i percorsi e le definizioni delle classi

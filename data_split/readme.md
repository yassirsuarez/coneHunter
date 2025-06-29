# Dataset `data_split`

Questa cartella contiene il dataset utilizzato per l'addestramento, la validazione e il test del modello YOLO.

Il dataset è basato sulla suddivisione del dataset originale disponibile su Kaggle:  
[FSOCO Split - Kaggle Dataset](https://www.kaggle.com/datasets/tommasofava/fsoco-split)

## Struttura della cartella `data_split`

data_split/
├── 📁 train/
│   ├── 📁 images/          
│   ├── 📁 labels/          
├── 📁 val/
│   ├── 📁 images/         
│   ├── 📁 labels/ 
├── 📁 test/
│   ├── 📁 images/           
│   ├── 📁 labels/           
└── config.yaml            

## Formato delle annotazioni

Le annotazioni sono in formato YOLO, dove ogni file `.txt` corrisponde a un'immagine e contiene una o più righe con:  
`<classe> <x_centro> <y_centro> <larghezza> <altezza>`

- Tutti i valori delle coordinate sono normalizzati nell'intervallo `[0, 1]`.
- La struttura segue le convenzioni YOLO per facilitare il training del modello.

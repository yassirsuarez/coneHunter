import pandas as pd
import matplotlib.pyplot as plt
import io
import math

# I tuoi dati CSV (senza le righe tagliate con "...")
csv_data = """
epoch,time,train/box_loss,train/cls_loss,train/dfl_loss,metrics/precision(B),metrics/recall(B),metrics/mAP50(B),metrics/mAP50-95(B),val/box_loss,val/cls_loss,val/dfl_loss,lr/pg0,lr/pg1,lr/pg2
1,92.0064,1.35974,1.67922,0.86909,0.56097,0.31185,0.34009,0.20181,1.11269,0.74188,0.83255,0.000369266,0.000369266,0.000369266
2,175.059,1.18986,0.85026,0.84905,0.68126,0.34489,0.38801,0.23071,1.09023,0.66536,0.83214,0.000724955,0.000724955,0.000724955
3,255.927,1.14652,0.73238,0.84187,0.63702,0.38751,0.43088,0.25748,1.02828,0.59538,0.82494,0.00106598,0.00106598,0.00106598
4,335.771,1.06221,0.66323,0.82856,0.68467,0.43297,0.47538,0.28722,1.00013,0.56161,0.82069,0.00139469,0.00139469,0.00139469
5,417.82,1.02759,0.62594,0.81889,0.71553,0.46057,0.50358,0.30415,0.98659,0.53883,0.81844,0.00171396,0.00171396,0.00171396
"""  # Puoi incollare fino a tutte le 50 righe qui

# Pulizia e caricamento
df = pd.read_csv(io.StringIO(csv_data.strip()))

# Lista delle metriche da plottare
metrics = [
    'train/box_loss', 'train/cls_loss', 'train/dfl_loss',
    'val/box_loss', 'val/cls_loss', 'val/dfl_loss',
    'metrics/precision(B)', 'metrics/recall(B)',
    'metrics/mAP50(B)', 'metrics/mAP50-95(B)',
    'lr/pg0', 'lr/pg1', 'lr/pg2'
]

# Impostazioni collage
num_metrics = len(metrics)
cols = 3
rows = math.ceil(num_metrics / cols)

# Crea subplots
fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
axes = axes.flatten()

# Plotta ogni metrica
for i, metric in enumerate(metrics):
    axes[i].plot(df['epoch'], df[metric], label=metric, color='tab:blue')
    axes[i].set_title(metric, fontsize=10)
    axes[i].set_xlabel('Epoch')
    axes[i].set_ylabel('Valore')
    axes[i].grid(True)
    axes[i].legend()

# Rimuove eventuali assi vuoti
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.suptitle("Metriche di Addestramento e Validazione", fontsize=16, y=1.02)
plt.show()

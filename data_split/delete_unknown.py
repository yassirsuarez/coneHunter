import os

def remove_unknown_labels(base_path, unknown_class_id=4):
    """
    Rimuove le righe contenenti la classe 'unknown' da tutti i file label nella struttura dataset.
    """
    removed_total = 0

    for split in ['train', 'val', 'test']:
        label_dir = os.path.join(base_path, split, 'labels')

        if not os.path.exists(label_dir):
            print(f"[!] Cartella labels non trovata per {split}")
            continue

        removed_count = 0
        print(f"\n[🧹 Pulizia {split.upper()}]")

        for label_file in os.listdir(label_dir):
            if not label_file.endswith('.txt'):
                continue

            label_path = os.path.join(label_dir, label_file)

            try:
                with open(label_path, 'r') as f:
                    lines = f.readlines()
            except Exception as e:
                print(f"[!] Errore lettura {label_path}: {e}")
                continue

            new_lines = [line for line in lines if not line.strip().startswith(str(unknown_class_id))]
            num_removed = len(lines) - len(new_lines)

            if num_removed > 0:
                removed_count += 1
                with open(label_path, 'w') as f:
                    f.writelines(new_lines)

        print(f"[✔] File modificati in {split}: {removed_count}")
        removed_total += removed_count

    print(f"\n[🧾 Totale file modificati: {removed_total}]")

# Esegui lo script
if __name__ == "__main__":
    # Ora il percorso è la cartella corrente (.) dato che lo script è dentro sta_split
    base_dataset_path = "."
    remove_unknown_labels(base_dataset_path)
import pandas as pd
import json
import os
from datetime import datetime
from sklearn.model_selection import train_test_split

def make_splits(df: pd.DataFrame, strategy: str = 'stratified', seed: int = 42) -> dict:
    """
    Розбиває датафрейм на train/val/test (80/10/10).
    """
    # Додаємо колонку id, якщо її немає (для збереження ids)
    if 'id' not in df.columns:
        df['id'] = df.index

    if strategy == 'stratified':
        # Спочатку відрізаємо 10% на test
        train_val, test = train_test_split(df, test_size=0.1, random_state=seed, stratify=df['label'])
        
        # З решти (90%) відрізаємо ще частину на val (щоб від початкового датасету це було 10%)
        # 10 / 90 = 1/9
        train, val = train_test_split(train_val, test_size=(1/9), random_state=seed, stratify=train_val['label'])
        
        return {
            'train': train,
            'val': val,
            'test': test,
            'strategy': strategy,
            'seed': seed
        }
    else:
        raise ValueError("Наразі підтримується лише 'stratified' стратегія.")

def save_splits(splits: dict, data_dir: str, docs_dir: str):
    """
    Зберігає ID кожного спліту та генерує JSON маніфест.
    """
    sample_dir = os.path.join(data_dir, 'sample_v2') # Використовуємо вашу папку sample
    os.makedirs(sample_dir, exist_ok=True)
    os.makedirs(docs_dir, exist_ok=True)

    # 1. Зберігаємо .txt файли з ID
    for split_name in ['train', 'val', 'test']:
        ids = splits[split_name]['id'].astype(str).tolist()
        file_path = os.path.join(sample_dir, f'splits_{split_name}_ids.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(ids))

    # 2. Генеруємо Manifest JSON
    manifest = {
        "seed": splits['seed'],
        "strategy": splits['strategy'],
        "sizes": {
            "train": len(splits['train']),
            "val": len(splits['val']),
            "test": len(splits['test'])
        },
        "generated_at": datetime.now().isoformat(),
        "columns_used": "label (for stratification)"
    }
    
    manifest_path = os.path.join(docs_dir, 'splits_manifest_lab5.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=4)
        
    print(f"Спліти збережено! Маніфест: {manifest_path}")
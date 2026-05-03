"""
Script pour diviser les données en ensembles d'entraînement et de test.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os
import json

def load_data(input_path):
    """Charger les données brutes."""
    df = pd.read_csv(input_path)
    print(f"Données chargées depuis {input_path}")
    print(f"Shape: {df.shape}")
    return df

def split_data(df, test_size=0.2, random_state=42):
    """
    Diviser les données en ensembles d'entraînement et de test.
    La variable cible est silica_concentrate (dernière colonne).
    """
    # Séparer les features et la cible
    X = df.drop(['date', 'silica_concentrate'], axis=1)
    y = df['silica_concentrate']
    
    print(f"\nDimensions originales:")
    print(f"X: {X.shape}")
    print(f"y: {y.shape}")
    
    # Division
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=test_size, 
        random_state=random_state
    )
    
    print(f"\nAprès split:")
    print(f"X_train: {X_train.shape}")
    print(f"X_test: {X_test.shape}")
    print(f"y_train: {y_train.shape}")
    print(f"y_test: {y_test.shape}")
    
    return X_train, X_test, y_train, y_test

def save_splits(X_train, X_test, y_train, y_test, output_dir="data/processed"):
    """Sauvegarder les datasets splitées."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Créer des DataFrames pour sauvegarder avec les index
    X_train_df = X_train.copy()
    X_test_df = X_test.copy()
    
    # Sauvegarder
    X_train_df.to_csv(f"{output_dir}/X_train.csv", index=False)
    X_test_df.to_csv(f"{output_dir}/X_test.csv", index=False)
    y_train.to_csv(f"{output_dir}/y_train.csv", index=False, header=['silica_concentrate'])
    y_test.to_csv(f"{output_dir}/y_test.csv", index=False, header=['silica_concentrate'])
    
    print(f"\nFichiers sauvegardés dans {output_dir}:")
    print(f"- X_train.csv")
    print(f"- X_test.csv")
    print(f"- y_train.csv")
    print(f"- y_test.csv")
    
    return {
        'X_train_path': f"{output_dir}/X_train.csv",
        'X_test_path': f"{output_dir}/X_test.csv",
        'y_train_path': f"{output_dir}/y_train.csv",
        'y_test_path': f"{output_dir}/y_test.csv"
    }

def main():
    """Fonction principale."""
    input_path = "data/raw/raw.csv"
    output_dir = "data/processed"
    
    # Charger les données
    df = load_data(input_path)
    
    # Diviser les données
    X_train, X_test, y_train, y_test = split_data(df)
    
    # Sauvegarder
    paths = save_splits(X_train, X_test, y_train, y_test, output_dir)
    
    # Sauvegarder les paths dans un fichier JSON pour DVC
    with open("data/processed/split_paths.json", "w") as f:
        json.dump(paths, f, indent=2)
    
    print("\nSplit des données terminé!")

if __name__ == "__main__":
    main()

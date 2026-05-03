"""
Script pour normaliser les données d'entraînement et de test.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import os

def load_split_data(data_dir="data/processed"):
    """Charger les données splitées."""
    X_train = pd.read_csv(f"{data_dir}/X_train.csv")
    X_test = pd.read_csv(f"{data_dir}/X_test.csv")
    y_train = pd.read_csv(f"{data_dir}/y_train.csv")
    y_test = pd.read_csv(f"{data_dir}/y_test.csv")
    
    print(f"Données chargées depuis {data_dir}")
    print(f"X_train shape: {X_train.shape}")
    print(f"X_test shape: {X_test.shape}")
    
    return X_train, X_test, y_train, y_test

def normalize_data(X_train, X_test):
    """
    Normaliser les données avec StandardScaler.
    Fit sur l'ensemble d'entraînement, transformer sur les deux ensembles.
    """
    scaler = StandardScaler()
    
    # Fit sur l'ensemble d'entraînement
    X_train_scaled = scaler.fit_transform(X_train)
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)
    
    # Transformer l'ensemble de test
    X_test_scaled = scaler.transform(X_test)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns)
    
    print(f"\nNormalisation effectuée avec StandardScaler")
    print(f"X_train_scaled shape: {X_train_scaled.shape}")
    print(f"X_test_scaled shape: {X_test_scaled.shape}")
    print(f"\nStatistiques X_train_scaled:")
    print(f"Mean: {X_train_scaled.mean().mean():.6f}")
    print(f"Std: {X_train_scaled.std().mean():.6f}")
    
    return X_train_scaled, X_test_scaled, scaler

def save_scaled_data(X_train_scaled, X_test_scaled, scaler, output_dir="data/processed"):
    """Sauvegarder les données normalisées et le scaler."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Sauvegarder les données normalisées
    X_train_scaled.to_csv(f"{output_dir}/X_train_scaled.csv", index=False)
    X_test_scaled.to_csv(f"{output_dir}/X_test_scaled.csv", index=False)
    
    # Sauvegarder le scaler
    joblib.dump(scaler, f"{output_dir}/scaler.pkl")
    
    print(f"\nFichiers sauvegardés dans {output_dir}:")
    print(f"- X_train_scaled.csv")
    print(f"- X_test_scaled.csv")
    print(f"- scaler.pkl")

def main():
    """Fonction principale."""
    data_dir = "data/processed"
    output_dir = "data/processed"
    
    # Charger les données splitées
    X_train, X_test, y_train, y_test = load_split_data(data_dir)
    
    # Normaliser
    X_train_scaled, X_test_scaled, scaler = normalize_data(X_train, X_test)
    
    # Sauvegarder
    save_scaled_data(X_train_scaled, X_test_scaled, scaler, output_dir)
    
    print("\n✓ Normalisation des données terminée!")

if __name__ == "__main__":
    main()

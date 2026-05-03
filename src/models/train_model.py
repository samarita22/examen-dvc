"""
Script pour entraîner le modèle avec les meilleurs paramètres trouvés par GridSearch.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import json
import os

def load_data_and_params(data_dir="data/processed", models_dir="models"):
    """Charger les données normalisées et les meilleurs paramètres."""
    X_train = pd.read_csv(f"{data_dir}/X_train_scaled.csv")
    y_train = pd.read_csv(f"{data_dir}/y_train.csv")
    
    # Convertir y_train en array 1D
    y_train = y_train.iloc[:, 0].values
    
    # Charger les meilleurs paramètres
    best_params = joblib.load(f"{models_dir}/best_params.pkl")
    
    print(f"Données chargées depuis {data_dir}")
    print(f"X_train shape: {X_train.shape}")
    print(f"y_train shape: {y_train.shape}")
    print(f"Meilleurs paramètres chargés depuis {models_dir}/best_params.pkl")
    print(f"Paramètres: {best_params}")
    
    return X_train, y_train, best_params

def train_model(X_train, y_train, best_params):
    """Entraîner le modèle avec les meilleurs paramètres."""
    print("\nEntraînement du modèle RandomForestRegressor...")
    
    # Créer le modèle avec les meilleurs paramètres
    model = RandomForestRegressor(**best_params)
    
    # Entraîner
    model.fit(X_train, y_train)
    
    # Évaluation sur l'ensemble d'entraînement
    train_r2 = model.score(X_train, y_train)
    
    print(f"Modèle entraîné!")
    print(f"Score R² sur l'ensemble d'entraînement: {train_r2:.4f}")
    
    return model

def save_model(model, output_dir="models"):
    """Sauvegarder le modèle entraîné."""
    os.makedirs(output_dir, exist_ok=True)
    
    model_path = f"{output_dir}/model.pkl"
    joblib.dump(model, model_path)
    
    print(f"\nModèle sauvegardé dans {model_path}")
    
    # Sauvegarder également les caractéristiques du modèle
    model_info = {
        'model_type': 'RandomForestRegressor',
        'n_estimators': model.n_estimators,
        'max_depth': model.max_depth,
        'model_path': model_path
    }
    
    with open(f"{output_dir}/model_info.json", "w") as f:
        json.dump(model_info, f, indent=2, default=str)
    
    print(f"Informations du modèle sauvegardées dans {output_dir}/model_info.json")

def main():
    """Fonction principale."""
    data_dir = "data/processed"
    models_dir = "models"
    
    # Charger les données et les paramètres
    X_train, y_train, best_params = load_data_and_params(data_dir, models_dir)
    
    # Entraîner le modèle
    model = train_model(X_train, y_train, best_params)
    
    # Sauvegarder le modèle
    save_model(model, models_dir)
    
    print("\nEntraînement du modèle terminé!")

if __name__ == "__main__":
    main()

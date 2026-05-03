"""
Script pour effectuer un GridSearch et trouver les meilleurs paramètres.
Nous utilisons RandomForestRegressor comme modèle.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import joblib
import json
import os

def load_scaled_data(data_dir="data/processed"):
    """Charger les données normalisées."""
    X_train = pd.read_csv(f"{data_dir}/X_train_scaled.csv")
    y_train = pd.read_csv(f"{data_dir}/y_train.csv")
    
    # Convertir y_train en array 1D
    y_train = y_train.iloc[:, 0].values
    
    print(f"Données normalisées chargées depuis {data_dir}")
    print(f"X_train shape: {X_train.shape}")
    print(f"y_train shape: {y_train.shape}")
    
    return X_train, y_train

def grid_search_rf(X_train, y_train, cv=5, n_jobs=-1):
    """
    Effectuer un GridSearch pour RandomForestRegressor.
    """
    print("\nDémarrage du GridSearch pour RandomForestRegressor...")
    
    # Définir les paramètres à tester (version optimisée)
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [15, 30],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2],
        'random_state': [42]
    }
    
    # Créer le modèle de base
    rf = RandomForestRegressor(random_state=42)
    
    # GridSearch
    grid_search = GridSearchCV(
        rf,
        param_grid,
        cv=cv,
        scoring='r2',
        n_jobs=n_jobs,
        verbose=1
    )
    
    grid_search.fit(X_train, y_train)
    
    print(f"\nGridSearch terminé!")
    print(f"Meilleurs paramètres: {grid_search.best_params_}")
    print(f"Meilleur score (R²): {grid_search.best_score_:.4f}")
    
    return grid_search

def save_best_params(grid_search, output_dir="models"):
    """Sauvegarder les meilleurs paramètres dans un fichier pkl."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Sauvegarder l'objet GridSearch complet
    joblib.dump(grid_search.best_params_, f"{output_dir}/best_params.pkl")
    
    # Également sauvegarder les résultats en JSON pour la lisibilité
    best_params_json = {k: (int(v) if isinstance(v, np.integer) else v) 
                        for k, v in grid_search.best_params_.items()}
    
    with open(f"{output_dir}/best_params.json", "w") as f:
        json.dump(best_params_json, f, indent=2)
    
    print(f"\nFichiers sauvegardés dans {output_dir}:")
    print(f"- best_params.pkl")
    print(f"- best_params.json")
    print(f"\nMeilleurs paramètres:\n{json.dumps(best_params_json, indent=2)}")

def main():
    """Fonction principale."""
    data_dir = "data/processed"
    output_dir = "models"
    
    # Charger les données normalisées
    X_train, y_train = load_scaled_data(data_dir)
    
    # GridSearch
    grid_search = grid_search_rf(X_train, y_train, cv=5, n_jobs=-1)
    
    # Sauvegarder les meilleurs paramètres
    save_best_params(grid_search, output_dir)
    
    print("\nGridSearch terminé et sauvegardé!")

if __name__ == "__main__":
    main()

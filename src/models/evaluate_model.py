"""
Script pour évaluer le modèle entraîné et générer des prédictions.
"""

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import json
import os

def load_data_and_model(data_dir="data/processed", models_dir="models"):
    """Charger les données de test et le modèle entraîné."""
    X_test = pd.read_csv(f"{data_dir}/X_test_scaled.csv")
    y_test = pd.read_csv(f"{data_dir}/y_test.csv")
    
    # Convertir y_test en array 1D
    y_test = y_test.iloc[:, 0].values
    
    # Charger le modèle
    model = joblib.load(f"{models_dir}/model.pkl")
    
    print(f"Données de test chargées depuis {data_dir}")
    print(f"X_test shape: {X_test.shape}")
    print(f"y_test shape: {y_test.shape}")
    print(f"Modèle chargé depuis {models_dir}/model.pkl")
    
    return X_test, y_test, model

def evaluate_model(X_test, y_test, model):
    """Évaluer le modèle sur l'ensemble de test."""
    print("\nÉvaluation du modèle...")
    
    # Faire les prédictions
    y_pred = model.predict(X_test)
    
    # Calculer les métriques
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Calculer aussi le MAPE (Mean Absolute Percentage Error)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    
    print(f"MSE: {mse:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE: {mae:.4f}")
    print(f"R²: {r2:.4f}")
    print(f"MAPE: {mape:.4f}%")
    
    metrics = {
        'mse': float(mse),
        'rmse': float(rmse),
        'mae': float(mae),
        'r2': float(r2),
        'mape': float(mape)
    }
    
    return y_pred, metrics

def save_predictions_and_metrics(X_test, y_test, y_pred, metrics, 
                                 output_data_dir="data/processed", 
                                 output_metrics_dir="metrics"):
    """Sauvegarder les prédictions et les métriques."""
    
    # Créer un DataFrame avec les prédictions
    predictions_df = X_test.copy()
    predictions_df['actual'] = y_test
    predictions_df['predicted'] = y_pred
    predictions_df['residual'] = y_test - y_pred
    
    # Sauvegarder les prédictions
    os.makedirs(output_data_dir, exist_ok=True)
    predictions_df.to_csv(f"{output_data_dir}/predictions.csv", index=False)
    print(f"\nPrédictions sauvegardées dans {output_data_dir}/predictions.csv")
    
    # Sauvegarder les métriques en JSON
    os.makedirs(output_metrics_dir, exist_ok=True)
    with open(f"{output_metrics_dir}/scores.json", "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"Métriques sauvegardées dans {output_metrics_dir}/scores.json")
    
    # Afficher les métriques
    print(f"\nMétriques d'évaluation:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")

def main():
    """Fonction principale."""
    data_dir = "data/processed"
    models_dir = "models"
    output_data_dir = "data/processed"
    output_metrics_dir = "metrics"
    
    # Charger les données et le modèle
    X_test, y_test, model = load_data_and_model(data_dir, models_dir)
    
    # Évaluer le modèle
    y_pred, metrics = evaluate_model(X_test, y_test, model)
    
    # Sauvegarder les prédictions et les métriques
    save_predictions_and_metrics(X_test, y_test, y_pred, metrics, 
                                 output_data_dir, output_metrics_dir)
    
    print("\nÉvaluation du modèle terminée!")

if __name__ == "__main__":
    main()

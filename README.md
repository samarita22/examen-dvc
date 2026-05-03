# Examen DVC et DagsHub - Solution Implémentée

## Vue d'ensemble du Projet

Ce projet implémente un pipeline complet de machine learning utilisant DVC (Data Version Control) pour modéliser le processus de flottation minérale. L'objectif est de prédire la concentration de silice en fonction des paramètres opérationnels.

## Architecture du Projet

```
examen_dvc/
├── .dvc/                          # Configuration DVC
│   ├── config                     # Configuration du remote (DagsHub)
│   └── .gitignore                 # Ignore les fichiers cache DVC
├── data/
│   ├── raw/
│   │   └── raw.csv               # Données brutes (1817 entrées)
│   └── processed/
│       ├── X_train.csv           # Features entraînement
│       ├── X_test.csv            # Features test
│       ├── y_train.csv           # Target entraînement
│       ├── y_test.csv            # Target test
│       ├── X_train_scaled.csv    # Features normalisées entraînement
│       ├── X_test_scaled.csv     # Features normalisées test
│       ├── scaler.pkl            # StandardScaler pour normalisation
│       └── predictions.csv       # Prédictions du modèle
├── models/
│   ├── best_params.pkl          # Meilleurs paramètres (GridSearch)
│   ├── best_params.json         # Meilleurs paramètres (JSON)
│   ├── model.pkl                # Modèle RandomForest entraîné
│   └── model_info.json          # Métadonnées du modèle
├── metrics/
│   └── scores.json              # Métriques d'évaluation
├── src/
│   ├── data/
│   │   ├── split_data.py        # Split données train/test
│   │   └── normalize_data.py    # Normalisation StandardScaler
│   └── models/
│       ├── grid_search.py       # GridSearch RandomForestRegressor
│       ├── train_model.py       # Entraînement du modèle
│       └── evaluate_model.py    # Évaluation et prédictions
├── dvc.yaml                      # Définition de la pipeline DVC
├── dvc.lock                      # Dépendances verrouillées
├── .gitignore                    # Fichiers ignorés par git
├── SUBMISSION.md                 # Rapport de soumission
└── README.md                     # Ce fichier
```

## Pipeline DVC

Le pipeline comprend 5 étapes principales définies dans `dvc.yaml`:

### 1. **Split** - Divisio des données
```bash
python src/data/split_data.py
```
- Charge `data/raw/raw.csv` (1817 entrées)
- Divise en 80% entraînement, 20% test
- Exclut les colonnes 'date' et la cible 'silica_concentrate'
- Produit: X_train, X_test, y_train, y_test

### 2. **Normalize** - Normalisation des données
```bash
python src/data/normalize_data.py
```
- Applique StandardScaler
- Fit sur ensemble d'entraînement
- Applique sur ensemble de test
- Produit: X_train_scaled, X_test_scaled, scaler.pkl

### 3. **Grid Search** - Recherche des meilleurs paramètres
```bash
python src/models/grid_search.py
```
- Modèle: RandomForestRegressor
- Paramètres testés:
  - n_estimators: [100, 200]
  - max_depth: [15, 30]
  - min_samples_split: [2, 5]
  - min_samples_leaf: [1, 2]
- Validation croisée: 5 folds
- Produit: best_params.pkl, best_params.json

### 4. **Train** - Entraînement du modèle
```bash
python src/models/train_model.py
```
- Utilise les meilleurs paramètres du GridSearch
- Entraîne sur l'ensemble d'entraînement normalisé
- Produit: model.pkl, model_info.json

### 5. **Evaluate** - Évaluation du modèle
```bash
python src/models/evaluate_model.py
```
- Évalue sur l'ensemble de test
- Génère les prédictions
- Calcule métriques: MSE, RMSE, MAE, R², MAPE
- Produit: predictions.csv, scores.json

## Résultats

### Meilleurs Paramètres
```json
{
  "n_estimators": 200,
  "max_depth": 15,
  "min_samples_split": 2,
  "min_samples_leaf": 2,
  "random_state": 42
}
```

### Métriques d'Évaluation
| Métrique | Valeur  |
|----------|---------|
| MSE      | 0.7732  |
| RMSE     | 0.8793  |
| MAE      | 0.6762  |
| R²       | 0.2274  |
| MAPE     | 36.74%  |

## Configuration DVC

### Remote Storage
Le projet utilise DagsHub comme remote storage:
```
URL: s3://dagshub/samarita22/examen-dvc/dvc
```

Configuration visible dans `.dvc/config`:
```ini
[core]
    remote = myremote
['remote "myremote"']
    url = s3://dagshub/samarita22/examen-dvc/dvc
```

## Installation et Utilisation

### Prérequis
- Python 3.12+
- Virtual environment

### Installation
```bash
# Créer et activer l'environnement virtuel
python3 -m venv env
source env/bin/activate  # Linux/macOS
# ou
env\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Exécution du Pipeline Complet
```bash
source env/bin/activate
dvc repro
```

### Exécution d'une étape spécifique
```bash
# Split des données
python src/data/split_data.py

# Normalisation
python src/data/normalize_data.py

# GridSearch
python src/models/grid_search.py

# Entraînement
python src/models/train_model.py

# Évaluation
python src/models/evaluate_model.py
```

### Push vers DagsHub
```bash
dvc push
```

## Dépôt DagsHub

**URL:** https://dagshub.com/samarita22/examen-dvc

N'oubliez pas de partager le dépôt avec `licence.pedago` en tant que collaborateur avec droits de lecture.

## Données

Les données sont téléchargées de:
```
https://datascientest-mlops.s3.eu-west-1.amazonaws.com/mlops_dvc_fr/raw.csv
```

### Description des Colonnes
- `ave_flot_air_flow`: Débit d'air moyen dans le processus de flottation
- `ave_flot_level`: Niveau moyen dans les cellules de flottation
- `iron_feed`: Quantité de minerai de fer
- `starch_flow`: Débit d'amidon
- `amina_flow`: Débit d'amine
- `ore_pulp_flow`: Débit de la pulpe
- `ore_pulp_pH`: pH de la pulpe
- `ore_pulp_density`: Densité de la pulpe
- `silica_concentrate`: **Concentration de silice (TARGET)**

## Fichiers Clés

- `dvc.yaml`: Définition complète de la pipeline
- `dvc.lock`: Dépendances verrouillées et versions des outputs
- `.dvc/config`: Configuration du remote storage DVC
- `SUBMISSION.md`: Rapport de soumission avec informations personnelles

## Auteur

**Nom:** VODOUNON Rodrigue  
**Email:** bignonvodounon@gmail.com  
**Date:** 3 Mai 2026

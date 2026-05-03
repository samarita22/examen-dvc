# Examen DVC - Rapport de Submission

## Informations Personnelles

**Nom:** VODOUNON  
**Prénom:** Rodrigue  
**Email:** bignonvodounon@gmail.com  

---

## Dépôt DagsHub

**URL du dépôt DagsHub:** https://dagshub.com/samarita22/examen-dvc

---

## Résumé du Projet

Ce projet implémente un pipeline complet de machine learning pour la modélisation du processus de flottation minérale, permettant de prédire la concentration de silice basée sur les paramètres opérationnels.

### Architecture du Pipeline

Le pipeline DVC comprend 5 étapes principales:

1. **Split des Données** (`split_data.py`)
   - Charge les données brutes depuis `data/raw/raw.csv`
   - Divise les données en ensembles d'entraînement (80%) et de test (20%)
   - Sortie: `X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv`

2. **Normalisation** (`normalize_data.py`)
   - Applique StandardScaler sur les données
   - Fit sur l'ensemble d'entraînement, applique sur l'ensemble de test
   - Sortie: `X_train_scaled.csv`, `X_test_scaled.csv`, `scaler.pkl`

3. **GridSearch** (`grid_search.py`)
   - Recherche les meilleurs paramètres pour RandomForestRegressor
   - Teste 16 combinaisons de paramètres avec validation croisée (k=5)
   - Meilleurs paramètres trouvés:
     - `n_estimators`: 200
     - `max_depth`: 15
     - `min_samples_split`: 2
     - `min_samples_leaf`: 2
   - Sortie: `best_params.pkl`, `best_params.json`

4. **Entraînement** (`train_model.py`)
   - Entraîne le modèle RandomForestRegressor avec les meilleurs paramètres
   - Score R² sur ensemble d'entraînement: 0.8223
   - Sortie: `model.pkl`, `model_info.json`

5. **Évaluation** (`evaluate_model.py`)
   - Évalue les performances du modèle sur l'ensemble de test
   - Génère les prédictions
   - Calcule les métriques: MSE, RMSE, MAE, R², MAPE
   - Sortie: `predictions.csv`, `scores.json`

### Métriques de Performance

Les métriques d'évaluation du modèle sur l'ensemble de test:

| Métrique | Valeur    |
|----------|-----------|
| MSE      | 0.7732    |
| RMSE     | 0.8793    |
| MAE      | 0.6762    |
| R²       | 0.2274    |
| MAPE     | 36.74%    |

### Structure du Projet

```
examen_dvc/
├── data/
│   ├── raw/
│   │   └── raw.csv (données brutes)
│   └── processed/
│       ├── X_train.csv
│       ├── X_test.csv
│       ├── y_train.csv
│       ├── y_test.csv
│       ├── X_train_scaled.csv
│       ├── X_test_scaled.csv
│       ├── scaler.pkl
│       └── predictions.csv
├── models/
│   ├── best_params.pkl
│   ├── best_params.json
│   ├── model.pkl
│   └── model_info.json
├── metrics/
│   └── scores.json
├── src/
│   ├── data/
│   │   ├── split_data.py
│   │   └── normalize_data.py
│   └── models/
│       ├── grid_search.py
│       ├── train_model.py
│       └── evaluate_model.py
├── dvc.yaml (définition de la pipeline)
├── dvc.lock (fichier de dépendances verrouillées)
└── .dvc/
    └── config (configuration DVC avec DagsHub comme remote)
```

### Configuration DVC

- **Remote Storage:** DagsHub S3 (`s3://dagshub/samarita22/examen-dvc/dvc`)
- **Fichier Config:** `.dvc/config`
- **Fichier Lock:** `dvc.lock`

### Environnement Virtuel

Un environnement virtuel Python est inclus dans le répertoire `env/` avec les dépendances:
- pandas
- scikit-learn
- dvc
- dvc[s3]
- joblib
- numpy

### Utilisation

Pour reproduire le pipeline complet:

```bash
source env/bin/activate
dvc repro
```

Pour exécuter une étape spécifique:

```bash
dvc repro src/data/split_data.py
dvc repro src/data/normalize_data.py
dvc repro src/models/grid_search.py
dvc repro src/models/train_model.py
dvc repro src/models/evaluate_model.py
```

---

## Checklist de Livraison

- 5 scripts de preprocessing, modélisation et évaluation
- Dossier `.dvc` avec fichier `config` pointant vers DagsHub
- Fichier `.pkl` du modèle entraîné dans le dossier `models`
- Fichier `.json` des métriques d'évaluation dans le dossier `metrics`
- Fichier `dvc.yaml` avec les étapes de la pipeline
- Fichier `dvc.lock` avec les informations de dépendances
- Dossier `data` bien structuré avec données brutes et traitées
- Pipeline DVC fonctionnelle et reproductible

**Date de Submission:** 3 Mai 2026
**Statut:** Complété

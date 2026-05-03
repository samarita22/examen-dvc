#!/bin/bash

# Script de test complet du projet DVC
# Vérifie que toute la pipeline est correctement configurée et fonctionne

set -e

echo "=========================================="
echo "TEST COMPLET DU PROJET DVC"
echo "=========================================="

PROJECT_DIR="/home/ubuntu/examen_dvc"
cd "$PROJECT_DIR"

# Couleurs pour les messages
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

test_count=0
pass_count=0
fail_count=0

# Fonction pour tester
test_condition() {
    local test_name="$1"
    local condition="$2"
    
    ((test_count++))
    echo -n "[$test_count] $test_name... "
    
    if eval "$condition" &>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        ((pass_count++))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        ((fail_count++))
        return 1
    fi
}

echo -e "\n${YELLOW}=== VÉRIFICATION DE LA STRUCTURE ===${NC}\n"

test_condition "Dossier src/data existe" "test -d src/data"
test_condition "Dossier src/models existe" "test -d src/models"
test_condition "Dossier data/raw existe" "test -d data/raw"
test_condition "Dossier data/processed existe" "test -d data/processed"
test_condition "Dossier models existe" "test -d models"
test_condition "Dossier metrics existe" "test -d metrics"
test_condition "Dossier .dvc existe" "test -d .dvc"

echo -e "\n${YELLOW}=== VÉRIFICATION DES SCRIPTS PYTHON ===${NC}\n"

# Vérifier les scripts
test_condition "split_data.py existe" "test -f src/data/split_data.py"
test_condition "normalize_data.py existe" "test -f src/data/normalize_data.py"
test_condition "grid_search.py existe" "test -f src/models/grid_search.py"
test_condition "train_model.py existe" "test -f src/models/train_model.py"
test_condition "evaluate_model.py existe" "test -f src/models/evaluate_model.py"

echo -e "\n${YELLOW}=== VÉRIFICATION DE LA CONFIGURATION DVC ===${NC}\n"

# Vérifier DVC
test_condition "dvc.yaml existe" "test -f dvc.yaml"
test_condition "dvc.lock existe" "test -f dvc.lock"
test_condition ".dvc/config existe" "test -f .dvc/config"
test_condition "DVC remote configuré" "grep -q 'myremote' .dvc/config"

echo -e "\n${YELLOW}=== VÉRIFICATION DES DONNÉES ===${NC}\n"

# Vérifier les données
test_condition "raw.csv existe" "test -f data/raw/raw.csv"
test_condition "X_train.csv existe" "test -f data/processed/X_train.csv"
test_condition "X_test.csv existe" "test -f data/processed/X_test.csv"
test_condition "y_train.csv existe" "test -f data/processed/y_train.csv"
test_condition "y_test.csv existe" "test -f data/processed/y_test.csv"

echo -e "\n${YELLOW}=== VÉRIFICATION DES DONNÉES NORMALISÉES ===${NC}\n"

# Vérifier les données normalisées
test_condition "X_train_scaled.csv existe" "test -f data/processed/X_train_scaled.csv"
test_condition "X_test_scaled.csv existe" "test -f data/processed/X_test_scaled.csv"
test_condition "scaler.pkl existe" "test -f data/processed/scaler.pkl"

echo -e "\n${YELLOW}=== VÉRIFICATION DU MODÈLE ===${NC}\n"

# Vérifier le modèle
test_condition "best_params.pkl existe" "test -f models/best_params.pkl"
test_condition "best_params.json existe" "test -f models/best_params.json"
test_condition "model.pkl existe" "test -f models/model.pkl"
test_condition "model_info.json existe" "test -f models/model_info.json"

echo -e "\n${YELLOW}=== VÉRIFICATION DES MÉTRIQUES ===${NC}\n"

# Vérifier les métriques
test_condition "scores.json existe" "test -f metrics/scores.json"
test_condition "predictions.csv existe" "test -f data/processed/predictions.csv"

echo -e "\n${YELLOW}=== VÉRIFICATION DE GIT ===${NC}\n"

# Vérifier git
test_condition ".git existe" "test -d .git"
test_condition "Remote origin configuré" "git remote -v | grep -q 'origin'"

echo -e "\n${YELLOW}=== TESTS DE CONTENU ===${NC}\n"

# Vérifier le contenu
test_condition "raw.csv a du contenu" "test -s data/raw/raw.csv"
test_condition "X_train.csv a du contenu" "test -s data/processed/X_train.csv"
test_condition "model.pkl a du contenu" "test -s models/model.pkl"
test_condition "scores.json contient les métriques" "grep -q '\"r2\"' metrics/scores.json"

echo -e "\n${YELLOW}=== VÉRIFICATION PYTHON ===${NC}\n"

# Vérifier que Python peut importer les modules
if source env/bin/activate 2>/dev/null; then
    test_condition "pandas peut être importé" "python3 -c 'import pandas' 2>/dev/null"
    test_condition "sklearn peut être importé" "python3 -c 'import sklearn' 2>/dev/null"
    test_condition "dvc peut être importé" "python3 -c 'import dvc' 2>/dev/null"
    test_condition "joblib peut être importé" "python3 -c 'import joblib' 2>/dev/null"
else
    echo -e "${YELLOW}! Venv non activé, test Python ignoré${NC}"
fi

echo -e "\n${YELLOW}=== VÉRIFICATION DES PARAMÈTRES DU MODÈLE ===${NC}\n"

# Vérifier les paramètres
echo "Meilleurs paramètres trouvés:"
cat models/best_params.json | python3 -m json.tool

echo -e "\n${YELLOW}=== VÉRIFICATION DES MÉTRIQUES ===${NC}\n"

echo "Métriques d'évaluation:"
cat metrics/scores.json | python3 -m json.tool

echo -e "\n${YELLOW}=== VÉRIFICATION DE LA PIPELINE DVC ===${NC}\n"

# Lister les stages
echo "Stages configurés dans dvc.yaml:"
grep "^[a-z_]*:" dvc.yaml | head -5

echo -e "\n${YELLOW}=== RÉSUMÉ ===${NC}\n"

echo "Tests exécutés: $test_count"
echo -e "Réussis: ${GREEN}$pass_count${NC}"
echo -e "Échoués: ${RED}$fail_count${NC}"

if [ $fail_count -eq 0 ]; then
    echo -e "\n${GREEN}TOUS LES TESTS SONT PASSES${NC}"
    echo -e "\n${GREEN}Le projet est correctement configure et pret a etre soumis.${NC}"
    exit 0
else
    echo -e "\n${RED}CERTAINS TESTS ONT ECHOUE${NC}"
    echo "Veuillez verifier les elements manquants ci-dessus."
    exit 1
fi

#!/bin/bash

echo "========================================"
echo " Plant-Based Optimizer - API REST"
echo "========================================"
echo ""
echo "Démarrage de l'API..."
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "ERREUR: Python 3 n'est pas installé"
    echo "Veuillez installer Python 3.8+ depuis https://www.python.org/"
    exit 1
fi

# Vérifier si les dépendances sont installées
python3 -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installation des dépendances..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERREUR: Échec de l'installation des dépendances"
        exit 1
    fi
fi

echo ""
echo "========================================"
echo " API démarrée sur http://localhost:8000"
echo " Documentation: http://localhost:8000/docs"
echo "========================================"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter l'API"
echo ""

# Démarrer l'API
python3 api_rest.py

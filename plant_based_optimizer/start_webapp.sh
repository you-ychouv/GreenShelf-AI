#!/bin/bash

echo "========================================"
echo " Plant-Based Optimizer - Web App"
echo "========================================"
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "ERREUR: Python 3 n'est pas installé"
    exit 1
fi

echo "[1/3] Démarrage de l'API..."
python3 api_rest.py &
API_PID=$!

echo "[2/3] Attente du démarrage de l'API (5 secondes)..."
sleep 5

echo "[3/3] Ouverture de la Web App..."

# Détecter l'OS et ouvrir le navigateur
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open http://localhost:8000/docs
    sleep 2
    open webapp/index.html
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open http://localhost:8000/docs &
    sleep 2
    xdg-open webapp/index.html &
fi

echo ""
echo "========================================"
echo " Web App lancée!"
echo "========================================"
echo ""
echo "API Backend: http://localhost:8000"
echo "Documentation: http://localhost:8000/docs"
echo "Web App: Ouverte dans votre navigateur"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter l'API"
echo ""

# Attendre que l'utilisateur arrête
wait $API_PID

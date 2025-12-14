@echo off
echo ========================================
echo  Plant-Based Optimizer - API REST
echo ========================================
echo.
echo Demarrage de l'API...
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou n'est pas dans le PATH
    echo Veuillez installer Python 3.8+ depuis https://www.python.org/
    pause
    exit /b 1
)

REM Vérifier si les dépendances sont installées
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo Installation des dependances...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERREUR: Echec de l'installation des dependances
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo  API demarree sur http://localhost:8000
echo  Documentation: http://localhost:8000/docs
echo ========================================
echo.
echo Appuyez sur Ctrl+C pour arreter l'API
echo.

REM Démarrer l'API
python api_rest.py

pause

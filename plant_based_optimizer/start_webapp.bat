@echo off
echo ========================================
echo  Plant-Based Optimizer - Web App
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe
    pause
    exit /b 1
)

echo [1/3] Demarrage de l'API...
start "API Backend" cmd /k "python api_rest.py"

echo [2/3] Attente du demarrage de l'API (5 secondes)...
timeout /t 5 /nobreak >nul

echo [3/3] Ouverture de la Web App...
start "" "http://localhost:8000/docs"
timeout /t 2 /nobreak >nul

REM Ouvrir le fichier HTML avec le chemin absolu
start "" "%~dp0webapp\index.html"

echo.
echo ========================================
echo  Web App lancee!
echo ========================================
echo.
echo API Backend: http://localhost:8000
echo Documentation: http://localhost:8000/docs
echo Web App: Ouverte dans votre navigateur
echo.
echo IMPORTANT: Si la page est blanche, ouvrez manuellement:
echo %~dp0webapp\index.html
echo.
echo Appuyez sur une touche pour fermer...
pause >nul

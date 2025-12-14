# 🚀 Démarrage Manuel - Guide Complet

## Si le script automatique ne fonctionne pas

### Méthode 1: Démarrage en 2 Étapes (Recommandé)

#### Étape 1: Démarrer l'API

Ouvrir un terminal dans le dossier `plant_based_optimizer`:

```bash
# Windows
python api_rest.py

# Linux/Mac
python3 api_rest.py
```

**Vérifier**: Vous devriez voir:
```
🌱 PLANT-BASED OPTIMIZER API
Démarrage de l'API sur http://127.0.0.1:8000
```

#### Étape 2: Ouvrir la Web App

**Option A - Double-clic:**
- Aller dans le dossier `webapp`
- Double-cliquer sur `index.html`

**Option B - Navigateur:**
- Ouvrir votre navigateur
- Faire Ctrl+O (ou Cmd+O sur Mac)
- Naviguer vers: `plant_based_optimizer/webapp/index.html`
- Cliquer sur "Ouvrir"

**Option C - Chemin direct:**
Copier-coller dans la barre d'adresse:
```
file:///C:/Users/Fatou SY/Desktop/plant_based_optimizer/webapp/index.html
```

---

### Méthode 2: Avec Serveur Local (Meilleure)

#### Étape 1: Démarrer l'API
```bash
python api_rest.py
```

#### Étape 2: Démarrer un serveur web local

**Terminal 2** (nouveau terminal):

```bash
# Aller dans le dossier webapp
cd plant_based_optimizer/webapp

# Démarrer un serveur Python
python -m http.server 8080
```

#### Étape 3: Ouvrir dans le navigateur
```
http://localhost:8080
```

---

### Vérifications

#### 1. L'API fonctionne?

Ouvrir dans le navigateur:
```
http://localhost:8000/health
```

Vous devriez voir:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "message": "API opérationnelle"
}
```

#### 2. La Web App se charge?

Dans le footer de la page, vous devriez voir:
```
API: ✓ En ligne
```

Si vous voyez "✗ Hors ligne", l'API n'est pas démarrée.

---

### Problèmes Courants

#### Problème 1: "API Hors ligne"

**Cause**: L'API n'est pas démarrée

**Solution**:
1. Ouvrir un terminal
2. Aller dans `plant_based_optimizer`
3. Lancer: `python api_rest.py`

#### Problème 2: Page blanche

**Cause**: Fichiers CSS/JS non chargés

**Solution**: Utiliser un serveur local (Méthode 2)

#### Problème 3: Erreur CORS

**Cause**: Restrictions de sécurité du navigateur

**Solution**: 
- Utiliser un serveur local (Méthode 2)
- OU ouvrir Chrome avec: `chrome.exe --disable-web-security --user-data-dir="C:/temp"`

#### Problème 4: Module 'fastapi' not found

**Cause**: Dépendances manquantes

**Solution**:
```bash
pip install -r requirements.txt
pip install fastapi uvicorn pydantic
```

---

### Test Rapide

Une fois tout démarré:

1. **Cliquer sur "Exemple"** dans la web app
2. **Cliquer sur "Optimiser"**
3. **Attendre 30-60 secondes**
4. **Vérifier les résultats**

Si ça fonctionne, tout est OK! 🎉

---

### Chemins Importants

```
plant_based_optimizer/
├── api_rest.py              ← Démarrer en premier
├── webapp/
│   ├── index.html          ← Ouvrir dans le navigateur
│   ├── styles.css          ← Styles (chargé automatiquement)
│   └── app.js              ← JavaScript (chargé automatiquement)
└── start_webapp.bat        ← Script automatique (si ça marche)
```

---

### Commandes Utiles

#### Vérifier Python
```bash
python --version
# Devrait afficher: Python 3.8 ou supérieur
```

#### Vérifier les dépendances
```bash
pip list | findstr fastapi
pip list | findstr uvicorn
pip list | findstr pydantic
```

#### Tuer un processus sur le port 8000 (si occupé)
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

---

### Alternative: Tout en Un

Si vous voulez tout dans un seul terminal:

```bash
# Démarrer l'API en arrière-plan et ouvrir la web app
python api_rest.py & start webapp/index.html
```

---

### Support

Si rien ne fonctionne:

1. **Vérifier les logs** dans le terminal où l'API tourne
2. **Ouvrir la console du navigateur** (F12) et regarder les erreurs
3. **Vérifier que le port 8000 est libre**
4. **Réinstaller les dépendances**: `pip install -r requirements.txt --force-reinstall`

---

**Une fois que ça marche, vous n'aurez plus besoin de ce guide! 🚀**

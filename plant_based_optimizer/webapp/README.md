# 🌱 Plant-Based Optimizer - Web App

## Application Web Fonctionnelle Complète

Cette web app permet d'optimiser vos produits alimentaires vers des alternatives plant-based directement depuis votre navigateur.

---

## 🚀 Démarrage Rapide (2 étapes)

### 1. Démarrer l'API Backend

```bash
# Terminal 1 - Démarrer l'API
cd plant_based_optimizer
python api_rest.py
```

L'API démarre sur: **http://localhost:8000**

### 2. Ouvrir la Web App

```bash
# Ouvrir le fichier HTML dans votre navigateur
# Double-cliquer sur: webapp/index.html

# OU utiliser un serveur local (recommandé)
cd webapp
python -m http.server 8080
```

Puis ouvrir: **http://localhost:8080**

---

## ✨ Fonctionnalités

### 🎯 Optimisation de Produits
- Saisir nom et ingrédients
- Optimisation en temps réel (30-60s)
- Affichage des résultats détaillés

### 📊 Métriques Complètes
- **Conservation**: Amélioration de la durée de vie (prioritaire 30%)
- **Nutrition**: Similarité nutritionnelle
- **Carbone**: Réduction d'empreinte carbone
- **Goût**: Score gustatif

### 🔄 Remplacements Détaillés
- Liste des ingrédients remplacés
- Alternatives plant-based suggérées
- Justifications pour chaque remplacement

### 💡 Recommandations
- Conseils pratiques d'implémentation
- Suggestions d'amélioration
- Points d'attention

### 📥 Export
- Export des résultats en JSON
- Sauvegarde pour analyse ultérieure

---

## 🎨 Interface

### Formulaire
- Nom du produit
- Liste des ingrédients (séparés par virgules)
- Boutons: Optimiser, Valider, Exemple, Réinitialiser

### Résultats
- Stratégie d'optimisation
- Remplacements (avec flèches visuelles)
- Métriques colorées (vert = excellent, bleu = bon, jaune = moyen, rouge = faible)
- Score total avec barre de progression
- Résumé textuel
- Liste de recommandations

### Loading
- Spinner animé
- Message de progression
- Indicateurs des 4 étapes (LLM → Data → Calculs → LLM)

---

## 🔧 Configuration

### URL de l'API

Par défaut: `http://localhost:8000`

Pour modifier, éditer `app.js` ligne 7:
```javascript
const API_URL = 'http://votre-serveur:8000';
```

### Timeout

Par défaut: 120 secondes (2 minutes)

Pour modifier, éditer `app.js` ligne 95:
```javascript
signal: AbortSignal.timeout(180000) // 3 minutes
```

---

## 📱 Responsive

L'application est entièrement responsive:
- ✅ Desktop (1200px+)
- ✅ Tablet (768px - 1199px)
- ✅ Mobile (< 768px)

---

## 🎯 Utilisation

### 1. Optimiser un Produit

1. Entrer le nom du produit
2. Lister les ingrédients (séparés par virgules)
3. Cliquer sur "Optimiser"
4. Attendre 30-60 secondes
5. Consulter les résultats

### 2. Valider un Produit

1. Entrer les informations
2. Cliquer sur "Valider"
3. Vérifier les problèmes détectés
4. Corriger si nécessaire

### 3. Charger un Exemple

1. Cliquer sur "Exemple"
2. Un produit d'exemple est chargé
3. Cliquer sur "Optimiser" pour tester

### 4. Exporter les Résultats

1. Après optimisation
2. Cliquer sur "Exporter JSON"
3. Le fichier est téléchargé

---

## 🔍 Détails Techniques

### Technologies
- **HTML5** - Structure
- **CSS3** - Styles (variables CSS, Grid, Flexbox, animations)
- **JavaScript Vanilla** - Logique (ES6+, Fetch API, async/await)

### Architecture
```
webapp/
├── index.html      # Structure HTML
├── styles.css      # Styles CSS
├── app.js          # Logique JavaScript
└── README.md       # Ce fichier
```

### API Calls
- `GET /health` - Vérifier l'état de l'API
- `POST /validate` - Valider un produit
- `POST /optimize` - Optimiser un produit

### Gestion d'État
- `currentResult` - Stocke le dernier résultat
- Affichage/masquage dynamique des sections
- Animations de transition

---

## 🎨 Personnalisation

### Couleurs

Éditer `styles.css` lignes 6-18:
```css
:root {
    --primary-color: #4CAF50;    /* Vert principal */
    --secondary-color: #2196F3;  /* Bleu secondaire */
    --danger-color: #f44336;     /* Rouge erreur */
    /* ... */
}
```

### Textes

Éditer `index.html` pour modifier:
- Titre de la page
- Tagline
- Labels des champs
- Messages d'aide

### Comportement

Éditer `app.js` pour modifier:
- Durée des animations
- Messages d'erreur
- Format d'affichage
- Logique de validation

---

## 🐛 Dépannage

### L'API n'est pas accessible

**Symptôme**: Status "Hors ligne" dans le footer

**Solutions**:
1. Vérifier que l'API est démarrée: `python api_rest.py`
2. Vérifier l'URL dans `app.js`
3. Vérifier les CORS (déjà configurés dans l'API)

### Timeout lors de l'optimisation

**Symptôme**: Erreur après 2 minutes

**Solutions**:
1. C'est normal si l'optimisation prend du temps
2. Augmenter le timeout dans `app.js`
3. Vérifier que l'API répond: `curl http://localhost:8000/health`

### Résultats ne s'affichent pas

**Symptôme**: Loading disparaît mais pas de résultats

**Solutions**:
1. Ouvrir la console du navigateur (F12)
2. Vérifier les erreurs JavaScript
3. Vérifier la réponse de l'API

### Erreur CORS

**Symptôme**: "CORS policy" dans la console

**Solutions**:
1. L'API a déjà CORS configuré
2. Utiliser un serveur local au lieu de `file://`
3. Vérifier que l'API accepte votre origine

---

## 📊 Exemple d'Utilisation

### Produit d'Exemple

**Nom**: Yaourt aux fruits

**Ingrédients**: lait entier, sucre, fraises, gélatine, arômes naturels, colorant E120

**Résultat Attendu**:
- Stratégie: Remplacement de tous les additifs
- Remplacements: gélatine → agar-agar, E120 → extrait de betterave
- Conservation: +15% environ
- Nutrition: 92% similarité
- Carbone: -8% environ
- Goût: 8.2/10

---

## 🚀 Déploiement

### Option 1: Serveur Web Simple

```bash
# Avec Python
cd webapp
python -m http.server 8080

# Avec Node.js
npx http-server webapp -p 8080

# Avec PHP
cd webapp
php -S localhost:8080
```

### Option 2: Serveur Web (Apache/Nginx)

Copier le dossier `webapp` dans votre répertoire web:
```bash
cp -r webapp /var/www/html/plant-optimizer
```

Accéder via: `http://votre-serveur/plant-optimizer`

### Option 3: Hébergement Statique

Déployer sur:
- **GitHub Pages**
- **Netlify**
- **Vercel**
- **AWS S3 + CloudFront**

**Important**: Mettre à jour `API_URL` dans `app.js` avec l'URL de votre API en production.

---

## 🔒 Sécurité

### En Production

1. **HTTPS**: Utiliser HTTPS pour l'API et la web app
2. **CORS**: Restreindre les origines autorisées dans `api_rest.py`
3. **Rate Limiting**: Limiter le nombre de requêtes par IP
4. **Validation**: Valider toutes les entrées côté serveur
5. **Authentification**: Ajouter un système d'auth si nécessaire

---

## 📈 Performance

### Optimisations Appliquées

- ✅ CSS minifié en production
- ✅ Chargement asynchrone
- ✅ Animations GPU-accelerated
- ✅ Lazy loading des résultats
- ✅ Debouncing des événements

### Temps de Chargement

- **Initial**: < 1 seconde
- **Optimisation**: 30-60 secondes (normal, analyse IA)
- **Affichage résultats**: < 0.5 seconde

---

## 🆘 Support

### Problèmes Courants

| Problème | Solution |
|----------|----------|
| API hors ligne | Démarrer avec `python api_rest.py` |
| Timeout | Augmenter dans `app.js` |
| CORS | Utiliser serveur local |
| Pas de résultats | Vérifier console (F12) |

### Logs

Ouvrir la console du navigateur (F12) pour voir:
- Appels API
- Erreurs JavaScript
- Réponses serveur

---

## ✅ Checklist de Déploiement

- [ ] API démarrée et accessible
- [ ] Web app accessible via serveur local
- [ ] Test avec produit d'exemple
- [ ] Vérification responsive (mobile/tablet)
- [ ] Test export JSON
- [ ] Vérification des erreurs (console)
- [ ] Test avec vos propres produits

---

## 📝 Changelog

### Version 1.0.0
- ✅ Interface complète HTML/CSS/JS
- ✅ Intégration API REST
- ✅ Affichage résultats détaillés
- ✅ Export JSON
- ✅ Responsive design
- ✅ Animations et transitions
- ✅ Gestion d'erreurs
- ✅ Validation de produits

---

**🎉 Web App Prête! Optimisez vos produits en quelques clics! 🌱**

Pour toute question, consultez la documentation principale dans le dossier parent.

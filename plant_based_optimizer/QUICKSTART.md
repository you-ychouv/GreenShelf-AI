# ⚡ Quick Start - Plant-Based Optimizer

## 🚀 Démarrage en 3 Minutes

### Étape 1: Installation (30 secondes)

```bash
cd plant_based_optimizer
pip install -r requirements.txt
```

### Étape 2: Test Rapide (1 minute)

```bash
python test_quick.py
```

Cela va:
- ✅ Tester le système sans API
- ✅ Optimiser 3 produits d'exemple
- ✅ Générer `test_result.json`

### Étape 3: Exemple Complet (1 minute)

```bash
python main.py
```

Cela va:
- ✅ Optimiser un yaourt aux fruits
- ✅ Afficher les résultats détaillés
- ✅ Générer `result_optimization.json`

### Étape 4: Visualisation (30 secondes)

```bash
python visualize_results.py result_optimization.json
```

Cela affiche:
- 📊 Tableau comparatif avant/après
- 🔄 Comparaison des ingrédients
- 🌍 Impact environnemental
- 🥗 Détails nutritionnels
- 🔬 Justification scientifique

---

## 🎯 Pour le Hackathon

### Démo Rapide (5 minutes)

```bash
# 1. Test système
python test_quick.py

# 2. Exemple yaourt
python main.py

# 3. Visualisation
python visualize_results.py result_optimization.json

# 4. Produit personnalisé
python main.py custom
```

### Optimiser Vos Produits

```bash
# Créer un fichier mes_produits.json
[
  {
    "name": "Mon Produit",
    "ingredients": "lait, sucre, gélatine, arômes"
  }
]

# Optimiser
python main.py batch
# Entrer: mes_produits.json

# Visualiser
python visualize_results.py results_batch.json
```

---

## 📊 Résultats Attendus

### Yaourt aux Fruits
- ✅ Durée de conservation: **+15-20%**
- ✅ Réduction carbone: **-40-50%**
- ✅ Nutrition maintenue: **>90%**
- ✅ Goût: **7.5-8.0/10**

### Crème Dessert
- ✅ Durée de conservation: **+10-15%**
- ✅ Réduction carbone: **-35-45%**
- ✅ Nutrition maintenue: **>85%**
- ✅ Goût: **7.0-7.5/10**

---

## 🔧 Configuration Optionnelle

### Avec API Blackbox (Parsing Intelligent)

```bash
# 1. Copier le template
copy .env.example .env

# 2. Éditer .env
BLACKBOX_API_KEY=votre_clé_ici

# 3. Relancer
python main.py
```

### Sans API (Parsing Basique)

Le système fonctionne automatiquement avec un parsing basé sur des règles. Aucune configuration nécessaire!

---

## 📁 Fichiers Générés

Après exécution, vous aurez:

```
plant_based_optimizer/
├── test_result.json              # Test rapide
├── result_optimization.json      # Exemple principal
├── results_batch.json            # Optimisation par lot
└── optimizer.log                 # Logs détaillés
```

---

## 🎓 Documentation Complète

- 📖 **README.md** - Vue d'ensemble
- 📘 **GUIDE_UTILISATION.md** - Guide détaillé
- 🏗️ **ARCHITECTURE.md** - Architecture technique
- ⚡ **QUICKSTART.md** - Ce fichier

---

## 🆘 Problèmes Courants

### "Module not found"
```bash
pip install -r requirements.txt
```

### "File not found"
```bash
# Vérifier que vous êtes dans le bon dossier
cd plant_based_optimizer
```

### Scores très bas
```bash
# Normal pour certains produits difficiles
# Ajouter plus d'alternatives dans data/plant_based_alternatives.csv
```

---

## 💡 Astuces Hackathon

### 1. Préparer des Exemples Impressionnants

Choisir des produits avec:
- Gélatine (remplacement facile par agar-agar)
- Produits laitiers (bonnes alternatives végétales)
- Conservateurs chimiques (alternatives naturelles)

### 2. Personnaliser les Pondérations

Éditer `config.py` selon les priorités du jury:

```python
# Si le jury valorise l'environnement
WEIGHTS = {
    "shelf_life": 0.20,
    "nutrition": 0.25,
    "carbon": 0.40,      # ⬆️ Augmenté
    "taste": 0.15
}
```

### 3. Ajouter Vos Données

Enrichir les CSV dans `data/` avec:
- Produits locaux
- Nouvelles alternatives
- Données spécifiques à votre région

### 4. Présentation Visuelle

```bash
# Générer plusieurs résultats
python main.py  # Produit 1
python main.py custom  # Produit 2
python main.py custom  # Produit 3

# Comparer visuellement
python visualize_results.py result_*.json
```

---

## 🏆 Points Forts à Mettre en Avant

1. **Données Réelles**
   - USDA (nutrition)
   - Agribalyse (carbone)
   - Sources scientifiques

2. **Calculs Rigoureux**
   - Modèles biologiques (shelf life)
   - Optimisation multi-objectifs
   - Validation scientifique

3. **IA Explicable**
   - Justifications détaillées
   - Transparence des calculs
   - Recommandations actionnables

4. **Robustesse**
   - Fonctionne avec ou sans API
   - Fallback automatique
   - Gestion d'erreurs

5. **Scalabilité**
   - Optimisation par lot
   - Architecture modulaire
   - Extensible facilement

---

## 🎯 Checklist Avant Présentation

- [ ] Tester `python test_quick.py` ✅
- [ ] Tester `python main.py` ✅
- [ ] Préparer 2-3 produits d'exemple
- [ ] Vérifier les résultats sont cohérents
- [ ] Préparer les slides avec captures d'écran
- [ ] Tester la démo en conditions réelles
- [ ] Avoir un backup sans internet (fallback)

---

## 📞 Support Rapide

**Problème**: Le système ne trouve pas d'alternatives
**Solution**: Ajouter dans `data/plant_based_alternatives.csv`

**Problème**: Scores nutritionnels trop bas
**Solution**: Réduire `MIN_NUTRITION_SIMILARITY` dans `config.py`

**Problème**: LLM ne répond pas
**Solution**: Le système utilise automatiquement le fallback

---

**Prêt pour le hackathon! Bonne chance! 🚀🌱**

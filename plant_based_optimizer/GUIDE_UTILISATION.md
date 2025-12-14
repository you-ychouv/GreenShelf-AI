# 📖 Guide d'Utilisation - Plant-Based Optimizer

## 🚀 Installation Rapide

### 1. Installer les dépendances

```bash
cd plant_based_optimizer
pip install -r requirements.txt
```

### 2. Configurer l'API Blackbox (Optionnel)

Si vous voulez utiliser le LLM pour le parsing intelligent:

```bash
# Copier le fichier d'exemple
copy .env.example .env

# Éditer .env et ajouter votre clé API
BLACKBOX_API_KEY=votre_clé_api_ici
```

**Note**: Le système fonctionne aussi sans API grâce au parsing de secours basé sur des règles.

## 💻 Utilisation

### Mode 1: Exemple par défaut

Teste le système avec un yaourt aux fruits:

```bash
python main.py
```

### Mode 2: Produit personnalisé

Optimise votre propre produit:

```bash
python main.py custom
```

Le système vous demandera:
- Nom du produit
- Liste des ingrédients

### Mode 3: Optimisation par lot

Optimise plusieurs produits depuis un fichier JSON:

```bash
python main.py batch
```

Exemple de fichier JSON (`mes_produits.json`):
```json
[
  {
    "name": "Mon Produit 1",
    "ingredients": "lait, sucre, gélatine"
  },
  {
    "name": "Mon Produit 2",
    "ingredients": "crème, œufs, chocolat"
  }
]
```

## 📊 Utilisation Programmatique

```python
from optimizer import PlantBasedOptimizer

# Initialiser
optimizer = PlantBasedOptimizer()

# Définir un produit
product = {
    "name": "Yaourt nature",
    "ingredients": "lait, ferments lactiques, gélatine"
}

# Optimiser
result = optimizer.optimize(product)

# Accéder aux résultats
print(f"Score total: {result['metrics']['total_score']}")
print(f"Remplacements: {result['optimized_product']['replacements']}")
```

## 🎯 Comprendre les Résultats

### Structure du résultat

```json
{
  "original_product": {
    "name": "Nom du produit",
    "ingredients": ["liste", "des", "ingrédients"],
    "non_plant_based_ingredients": ["ingrédients", "animaux"]
  },
  "strategy": "replace_all_additives" ou "replace_one_ingredient",
  "optimized_product": {
    "ingredients": ["nouvelle", "liste"],
    "replacements": [
      {
        "original": "lait",
        "replacement": "lait de soja",
        "reason": "Remplacement d'ingrédient non plant-based"
      }
    ]
  },
  "metrics": {
    "shelf_life": {
      "original_days": 7.0,
      "new_days": 8.5,
      "improvement_percent": 21.4,
      "score": 0.714
    },
    "nutrition": {
      "similarity_percent": 92.5,
      "score": 0.925
    },
    "carbon": {
      "reduction_percent": 45.2,
      "score": 0.452
    },
    "taste": {
      "overall_score": 7.8,
      "score": 0.780
    },
    "total_score": 0.715
  },
  "justification": {
    "summary": "Résumé de la recommandation",
    "shelf_life_analysis": "Analyse détaillée...",
    "nutrition_analysis": "Analyse détaillée...",
    "carbon_analysis": "Analyse détaillée...",
    "taste_analysis": "Analyse détaillée...",
    "trade_offs": "Compromis acceptés..."
  },
  "recommendations": [
    "Recommandation 1",
    "Recommandation 2"
  ]
}
```

### Interprétation des scores

- **Score total** (0-1): Score global pondéré
  - > 0.7: Excellent
  - 0.5-0.7: Bon
  - < 0.5: À améliorer

- **Durée de conservation**: 
  - Amélioration en % et en jours
  - Score basé sur l'amélioration

- **Nutrition**: 
  - Similarité en % (objectif: > 85%)
  - Compare protéines, lipides, glucides, fibres, calories

- **Empreinte carbone**: 
  - Réduction en % (objectif: maximiser)
  - kg CO2eq par kg de produit

- **Goût**: 
  - Score sur 10 (objectif: > 6.0)
  - Basé sur profils sensoriels

## 🔧 Configuration Avancée

### Modifier les pondérations

Éditez `config.py`:

```python
WEIGHTS = {
    "shelf_life": 0.30,   # 30% - Durée de conservation
    "nutrition": 0.25,    # 25% - Nutrition
    "carbon": 0.25,       # 25% - Carbone
    "taste": 0.20         # 20% - Goût
}
```

### Modifier les seuils

```python
MIN_NUTRITION_SIMILARITY = 0.85  # 85% minimum
MAX_CARBON_INCREASE = 0.0        # Pas d'augmentation
MIN_TASTE_SCORE = 6.0            # Score minimum
```

### Nombre de candidats générés

```python
NUM_CANDIDATES = 5  # Nombre de formulations à évaluer
```

## 📁 Ajouter vos Propres Données

### 1. Données nutritionnelles (USDA)

Éditez `data/usda_nutrition.csv`:

```csv
name,protein_g,fat_g,carbs_g,fiber_g,calories_kcal,water_g
mon_ingredient,10.0,5.0,20.0,3.0,150,60
```

### 2. Empreinte carbone (Agribalyse)

Éditez `data/agribalyse_carbon.csv`:

```csv
name,co2_kg_per_kg,land_use_m2,water_use_l
mon_ingredient,2.5,3.0,1500
```

### 3. Alternatives plant-based

Éditez `data/plant_based_alternatives.csv`:

```csv
original_ingredient,plant_based_alternative,compatibility_score,category
mon_ingredient_animal,mon_alternative_vegetale,0.85,protein
```

### 4. Profils gustatifs

Éditez `data/taste_profiles.csv`:

```csv
name,sweetness,saltiness,sourness,bitterness,umami,overall_score
mon_ingredient,5.0,3.0,2.0,1.0,4.0,7.5
```

### 5. Données de conservation

Éditez `data/shelf_life_data.csv`:

```csv
name,ph,water_activity,antimicrobial_score
mon_ingredient,6.5,0.90,5
```

## 🐛 Dépannage

### Problème: "Aucun candidat valide généré"

**Causes possibles:**
- Ingrédients non trouvés dans les bases de données
- Seuils trop stricts

**Solutions:**
1. Ajouter les ingrédients manquants dans les CSV
2. Réduire les seuils dans `config.py`
3. Vérifier l'orthographe des ingrédients

### Problème: "Erreur lors de l'appel au LLM"

**Causes possibles:**
- Clé API invalide ou manquante
- Problème de connexion

**Solutions:**
1. Vérifier la clé API dans `.env`
2. Le système utilisera le parsing de secours automatiquement
3. Vérifier la connexion internet

### Problème: Scores très bas

**Causes possibles:**
- Alternatives limitées dans la base
- Contraintes trop strictes

**Solutions:**
1. Ajouter plus d'alternatives dans `plant_based_alternatives.csv`
2. Ajuster les pondérations dans `config.py`
3. Enrichir les bases de données

## 📈 Exemples d'Utilisation

### Exemple 1: Yaourt aux fruits

```python
product = {
    "name": "Yaourt aux fruits",
    "ingredients": "lait, sucre, fraises, gélatine, colorant E120"
}
```

**Résultat attendu:**
- Stratégie: `replace_all_additives` (gélatine + E120)
- Remplacements: gélatine → agar-agar, E120 → colorant végétal
- Amélioration durée: +15-20%
- Réduction carbone: -40-50%

### Exemple 2: Crème dessert

```python
product = {
    "name": "Crème dessert chocolat",
    "ingredients": "lait, crème, sucre, chocolat, gélatine"
}
```

**Résultat attendu:**
- Stratégie: `replace_all_additives` (gélatine)
- Remplacements: gélatine → agar-agar
- Amélioration durée: +10-15%
- Réduction carbone: -30-40%

### Exemple 3: Gâteau

```python
product = {
    "name": "Gâteau marbré",
    "ingredients": "farine, sucre, œufs, beurre, lait"
}
```

**Résultat attendu:**
- Stratégie: `replace_one_ingredient` (pas d'additifs)
- Remplacements: œufs → graines de lin + eau OU beurre → margarine végétale
- Similarité nutrition: 90%+
- Réduction carbone: -20-30%

## 🎓 Pour le Hackathon

### Présentation des résultats

1. **Montrer l'architecture 4 étapes**
   - Parsing LLM
   - Enrichissement données
   - Calculs scientifiques
   - Sélection LLM

2. **Démonstration live**
   ```bash
   python main.py
   ```

3. **Métriques clés à présenter**
   - Amélioration durée de conservation
   - Réduction empreinte carbone
   - Maintien qualité nutritionnelle
   - Score gustatif

4. **Points forts**
   - Données réelles (USDA, Agribalyse)
   - Calculs scientifiques rigoureux
   - Optimisation multi-objectifs
   - Justifications explicables

### Extensions possibles

1. **Interface web** (Streamlit/Gradio)
2. **API REST** (FastAPI)
3. **Visualisations** (graphiques comparatifs)
4. **Base de données** (PostgreSQL)
5. **Tests sensoriels** (intégration résultats réels)

## 📞 Support

Pour toute question ou problème:
1. Vérifier ce guide
2. Consulter les exemples dans `examples/`
3. Examiner les logs dans `optimizer.log`

Bon hackathon! 🚀🌱

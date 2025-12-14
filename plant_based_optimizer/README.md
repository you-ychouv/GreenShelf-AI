# 🌱 Plant-Based Ingredient Optimizer

## Hackathon IA - Transformation Agroalimentaire

Système d'optimisation intelligent pour remplacer les ingrédients non plant-based par des alternatives végétales tout en respectant des contraintes strictes.

## 🎯 Objectifs

1. ✅ **Augmenter la durée de conservation**
2. ✅ **Assurer les mêmes apports nutritionnels**
3. ✅ **Diminuer l'empreinte carbone**
4. ✅ **Maintenir un goût proche/bon**

## 📋 Règles de Remplacement

- **Si conservateurs/additifs NON plant-based** → Remplacer TOUS
- **Sinon** → Remplacer UN ingrédient non plant-based

## 🏗️ Architecture

```
ÉTAPE 1: LLM - Parsing & Classification
    ↓
ÉTAPE 2: Database - Enrichissement (USDA, Agribalyse)
    ↓
ÉTAPE 3: Calculs - Optimisation multi-objectifs
    ↓
ÉTAPE 4: LLM - Sélection & Justification
```

## 🚀 Installation

```bash
pip install -r requirements.txt
```

## 💻 Utilisation

```python
from optimizer import PlantBasedOptimizer

# Initialiser l'optimiseur
optimizer = PlantBasedOptimizer()

# Analyser un produit
product = {
    "name": "Yaourt aux fruits",
    "ingredients": "lait, sucre, fraises, gélatine, arômes naturels"
}

# Obtenir la recommandation
result = optimizer.optimize(product)
print(result)
```

## 📊 Sources de Données

- **Nutrition**: USDA FoodData Central
- **Empreinte Carbone**: Agribalyse
- **Alternatives**: Base de données plant-based
- **Goût**: Profils sensoriels (CSV)

## 📁 Structure du Projet

```
plant_based_optimizer/
├── main.py                 # Point d'entrée principal
├── optimizer.py            # Logique d'optimisation
├── llm_handler.py          # Intégration LLM (Blackbox)
├── data_enrichment.py      # Enrichissement données
├── calculations.py         # Calculs scientifiques
├── config.py              # Configuration
├── requirements.txt       # Dépendances
├── data/
│   ├── usda_nutrition.csv
│   ├── agribalyse_carbon.csv
│   ├── plant_based_alternatives.csv
│   ├── taste_profiles.csv
│   └── shelf_life_data.csv
└── examples/
    └── example_products.json
```

## 🧪 Exemple de Résultat

```json
{
  "original_product": {
    "name": "Yaourt aux fruits",
    "ingredients": ["lait", "sucre", "fraises", "gélatine", "arômes naturels"]
  },
  "strategy": "replace_additives",
  "optimized_product": {
    "ingredients": ["lait d'amande", "sucre", "fraises", "agar-agar", "arômes naturels"],
    "replacements": [
      {"original": "lait", "replacement": "lait d'amande"},
      {"original": "gélatine", "replacement": "agar-agar"}
    ]
  },
  "metrics": {
    "shelf_life_improvement": "+15%",
    "nutrition_similarity": "98%",
    "carbon_reduction": "-45%",
    "taste_score": "8.5/10"
  },
  "justification": "Remplacement de la gélatine (additif animal) par l'agar-agar..."
}
```

## 🔬 Méthodologie Scientifique

### Calcul Durée de Conservation
- Modèle de croissance microbienne
- Facteurs: pH, activité de l'eau (Aw), conservateurs

### Calcul Nutritionnel
- Somme pondérée des macronutriments
- Comparaison protéines, lipides, glucides, fibres

### Calcul Empreinte Carbone
- kg CO2eq par kg d'ingrédient
- Données Agribalyse

### Scoring Multi-Objectifs
- Pondération des 4 critères
- Sélection de la meilleure formulation

## 👥 Équipe

Hackathon IA - Transformation Agroalimentaire

## 📄 Licence

MIT License

# 📑 Index - Plant-Based Optimizer

## 🎯 Par Où Commencer?

### Je veux tester rapidement (5 min)
→ **[QUICKSTART.md](QUICKSTART.md)**

### Je veux comprendre le projet (10 min)
→ **[README.md](README.md)**

### Je veux utiliser le système (20 min)
→ **[GUIDE_UTILISATION.md](GUIDE_UTILISATION.md)**

### Je veux comprendre l'architecture (15 min)
→ **[ARCHITECTURE.md](ARCHITECTURE.md)**

### Je prépare la présentation hackathon (30 min)
→ **[PRESENTATION_HACKATHON.md](PRESENTATION_HACKATHON.md)**

---

## 📚 Documentation Complète

### 📖 Guides Utilisateur

| Fichier | Description | Temps de lecture |
|---------|-------------|------------------|
| **README.md** | Vue d'ensemble du projet | 5 min |
| **QUICKSTART.md** | Démarrage rapide en 3 minutes | 3 min |
| **GUIDE_UTILISATION.md** | Guide complet d'utilisation | 20 min |

### 🏗️ Documentation Technique

| Fichier | Description | Temps de lecture |
|---------|-------------|------------------|
| **ARCHITECTURE.md** | Architecture détaillée du système | 15 min |
| **config.py** | Configuration et paramètres | 5 min |

### 🎓 Hackathon

| Fichier | Description | Temps de lecture |
|---------|-------------|------------------|
| **PRESENTATION_HACKATHON.md** | Présentation complète pour le jury | 30 min |
| **INDEX.md** | Ce fichier - Navigation | 2 min |

---

## 🐍 Code Source

### Modules Principaux

| Fichier | Rôle | Lignes |
|---------|------|--------|
| **optimizer.py** | Orchestration principale | ~400 |
| **llm_handler.py** | Intégration LLM (Étapes 1 & 4) | ~300 |
| **data_enrichment.py** | Enrichissement données (Étape 2) | ~400 |
| **calculations.py** | Calculs scientifiques (Étape 3) | ~350 |
| **config.py** | Configuration globale | ~100 |

### Scripts d'Utilisation

| Fichier | Rôle | Usage |
|---------|------|-------|
| **main.py** | Point d'entrée principal | `python main.py` |
| **test_quick.py** | Tests rapides | `python test_quick.py` |
| **visualize_results.py** | Visualisation résultats | `python visualize_results.py result.json` |

---

## 📊 Données

### Bases de Données CSV

| Fichier | Source | Entrées | Description |
|---------|--------|---------|-------------|
| **usda_nutrition.csv** | USDA FoodData Central | 80+ | Données nutritionnelles |
| **agribalyse_carbon.csv** | Agribalyse (ADEME) | 100+ | Empreinte carbone |
| **plant_based_alternatives.csv** | Propriétaire | 80+ | Alternatives végétales |
| **taste_profiles.csv** | Propriétaire | 70+ | Profils gustatifs |
| **shelf_life_data.csv** | Propriétaire | 90+ | Données conservation |

### Exemples

| Fichier | Description |
|---------|-------------|
| **examples/example_products.json** | 15 produits d'exemple |

---

## 🚀 Commandes Rapides

### Installation
```bash
cd plant_based_optimizer
pip install -r requirements.txt
```

### Tests
```bash
# Test rapide (sans API)
python test_quick.py

# Exemple complet
python main.py

# Produit personnalisé
python main.py custom

# Optimisation par lot
python main.py batch
```

### Visualisation
```bash
# Visualiser un résultat
python visualize_results.py result_optimization.json

# Comparer plusieurs résultats
python visualize_results.py result1.json result2.json result3.json
```

---

## 📁 Structure du Projet

```
plant_based_optimizer/
│
├── 📚 Documentation
│   ├── README.md                    ⭐ Commencer ici
│   ├── QUICKSTART.md                ⚡ Démarrage rapide
│   ├── GUIDE_UTILISATION.md         📖 Guide complet
│   ├── ARCHITECTURE.md              🏗️ Architecture technique
│   ├── PRESENTATION_HACKATHON.md    🎓 Présentation jury
│   └── INDEX.md                     📑 Ce fichier
│
├── 🐍 Code Source
│   ├── config.py                    ⚙️ Configuration
│   ├── llm_handler.py               🤖 LLM (Étapes 1 & 4)
│   ├── data_enrichment.py           📊 Enrichissement (Étape 2)
│   ├── calculations.py              🔬 Calculs (Étape 3)
│   └── optimizer.py                 🎯 Orchestration
│
├── 🚀 Scripts
│   ├── main.py                      ▶️ Point d'entrée
│   ├── test_quick.py                🧪 Tests rapides
│   └── visualize_results.py         📊 Visualisation
│
├── 📊 Données
│   └── data/
│       ├── usda_nutrition.csv
│       ├── agribalyse_carbon.csv
│       ├── plant_based_alternatives.csv
│       ├── taste_profiles.csv
│       └── shelf_life_data.csv
│
├── 📁 Exemples
│   └── examples/
│       └── example_products.json
│
└── ⚙️ Configuration
    ├── requirements.txt
    └── .env.example
```

---

## 🎯 Cas d'Usage

### 1. Je suis développeur
→ Lire **ARCHITECTURE.md** puis explorer le code source

### 2. Je suis utilisateur final
→ Suivre **QUICKSTART.md** puis **GUIDE_UTILISATION.md**

### 3. Je prépare le hackathon
→ Lire **PRESENTATION_HACKATHON.md** et préparer la démo

### 4. Je veux contribuer
→ Comprendre **ARCHITECTURE.md** et ajouter des données dans `data/`

### 5. Je veux intégrer dans mon système
→ Voir **GUIDE_UTILISATION.md** section "Utilisation Programmatique"

---

## 🔍 Recherche Rapide

### Trouver une Information

| Je cherche... | Fichier | Section |
|---------------|---------|---------|
| Comment installer | QUICKSTART.md | Installation |
| Comment utiliser | GUIDE_UTILISATION.md | Utilisation |
| Comment ça marche | ARCHITECTURE.md | Architecture |
| Données nutritionnelles | data/usda_nutrition.csv | - |
| Alternatives végétales | data/plant_based_alternatives.csv | - |
| Modifier les pondérations | config.py | WEIGHTS |
| Ajouter un ingrédient | GUIDE_UTILISATION.md | Ajouter vos Données |
| Comprendre les scores | GUIDE_UTILISATION.md | Interprétation |
| Préparer la démo | PRESENTATION_HACKATHON.md | Démonstration |

---

## 📊 Statistiques du Projet

### Code
- **Lignes de code Python**: ~1,500
- **Modules**: 5 principaux
- **Scripts**: 3 utilitaires
- **Tests**: Intégrés

### Documentation
- **Pages de documentation**: 6
- **Mots**: ~15,000
- **Exemples de code**: 50+
- **Diagrammes**: 3

### Données
- **Bases de données**: 5 CSV
- **Ingrédients documentés**: 200+
- **Alternatives végétales**: 80+
- **Produits d'exemple**: 15

---

## 🆘 Support

### Problèmes Courants

| Problème | Solution | Fichier |
|----------|----------|---------|
| Module not found | `pip install -r requirements.txt` | requirements.txt |
| Scores très bas | Ajouter alternatives dans CSV | GUIDE_UTILISATION.md |
| LLM ne répond pas | Utilise fallback automatique | llm_handler.py |
| Fichier non trouvé | Vérifier le chemin | config.py |

### Où Trouver de l'Aide?

1. **GUIDE_UTILISATION.md** → Section "Dépannage"
2. **QUICKSTART.md** → Section "Problèmes Courants"
3. **ARCHITECTURE.md** → Section "Sécurité & Fiabilité"

---

## 🎓 Ressources Externes

### Sources de Données
- **USDA FoodData Central**: https://fdc.nal.usda.gov/
- **Agribalyse**: https://agribalyse.ademe.fr/
- **Documentation scientifique**: Voir ARCHITECTURE.md

### Technologies Utilisées
- **Python**: 3.8+
- **Pandas**: Manipulation données
- **NumPy**: Calculs scientifiques
- **Requests**: API calls
- **Blackbox AI**: LLM

---

## ✅ Checklist Complète

### Avant le Hackathon
- [ ] Lire README.md
- [ ] Tester avec `python test_quick.py`
- [ ] Lire PRESENTATION_HACKATHON.md
- [ ] Préparer 2-3 produits d'exemple
- [ ] Tester la démo complète
- [ ] Vérifier que tout fonctionne sans internet (fallback)

### Pendant le Hackathon
- [ ] Présenter l'architecture (ARCHITECTURE.md)
- [ ] Faire la démo live (QUICKSTART.md)
- [ ] Montrer les résultats (visualize_results.py)
- [ ] Expliquer les métriques (PRESENTATION_HACKATHON.md)
- [ ] Répondre aux questions techniques (ARCHITECTURE.md)

### Après le Hackathon
- [ ] Collecter feedback
- [ ] Améliorer les données
- [ ] Développer interface web
- [ ] Créer API REST
- [ ] Publier sur GitHub

---

## 🏆 Points Clés à Retenir

1. **4 Étapes**: LLM → Data → Calculs → LLM
2. **4 Critères**: Durée, Nutrition, Carbone, Goût
3. **2 Stratégies**: Remplacer tous additifs OU un ingrédient
4. **Données Réelles**: USDA + Agribalyse
5. **IA Explicable**: Justifications détaillées

---

**Bon hackathon! 🚀🌱**

*Dernière mise à jour: [Date]*

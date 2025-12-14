# 🧪 Guide de Test Complet

## Comment Tout Tester - Étape par Étape

---

## 📋 Prérequis

### 1. Vérifier que l'API est démarrée

```bash
# Terminal 1 - Démarrer l'API
cd plant_based_optimizer
python api_rest.py
```

Vous devriez voir:
```
🌱 Initialisation du Plant-Based Optimizer...
✓ Optimiseur initialisé

🚀 Démarrage de l'API sur http://127.0.0.1:8000
📚 Documentation: http://127.0.0.1:8000/docs
```

### 2. Vérifier que vos codes LLM sont pris en compte

L'API utilise **automatiquement** vos codes existants:
- ✅ `llm_handler.py` - Votre code LLM (Étapes 1 & 4)
- ✅ `data_enrichment.py` - Enrichissement données
- ✅ `calculations.py` - Calculs scientifiques
- ✅ `optimizer.py` - Orchestration

**Rien n'a été modifié dans ces fichiers!** L'API les utilise tels quels.

---

## 🧪 Tests à Effectuer

### Test 1: Health Check (10 secondes)

**Objectif**: Vérifier que l'API fonctionne

```bash
# Méthode 1: Navigateur
# Ouvrir: http://localhost:8000/health

# Méthode 2: cURL (Windows PowerShell)
curl http://localhost:8000/health

# Méthode 3: Python
python -c "import requests; print(requests.get('http://localhost:8000/health').json())"
```

**Résultat attendu**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "message": "API opérationnelle"
}
```

---

### Test 2: Validation de Produit (5 secondes)

**Objectif**: Vérifier qu'un produit est valide avant optimisation

```bash
# PowerShell
curl -X POST "http://localhost:8000/validate" `
  -H "Content-Type: application/json" `
  -d '{\"name\":\"Yaourt aux fruits\",\"ingredients\":\"lait entier, sucre, fraises, gélatine\"}'
```

**Résultat attendu**:
```json
{
  "valid": true,
  "issues": [],
  "warnings": [],
  "ingredient_count": 4
}
```

---

### Test 3: Optimisation Simple (30-60 secondes)

**Objectif**: Optimiser un produit avec VOS CODES LLM

```bash
# PowerShell
curl -X POST "http://localhost:8000/optimize?return_format=simple" `
  -H "Content-Type: application/json" `
  -d '{\"name\":\"Yaourt aux fruits\",\"ingredients\":\"lait entier, sucre, fraises, gélatine, arômes naturels, colorant E120\"}'
```

**Ce qui se passe en arrière-plan** (VOS CODES):
1. ✅ **llm_handler.py** → Parse et classifie les ingrédients (IA)
2. ✅ **data_enrichment.py** → Enrichit avec bases de données
3. ✅ **calculations.py** → Calcule les scores (conservation, nutrition, carbone, goût)
4. ✅ **llm_handler.py** → Sélectionne et justifie (IA)

**Résultat attendu**:
```json
{
  "success": true,
  "product_name": "Yaourt aux fruits",
  "strategy": "replace_all_additives",
  "replacements": [
    {
      "original": "gélatine",
      "replacement": "agar-agar",
      "reason": "Remplacement d'additif non plant-based"
    },
    {
      "original": "colorant E120",
      "replacement": "extrait de betterave",
      "reason": "Remplacement d'additif non plant-based"
    }
  ],
  "scores": {
    "shelf_life_improvement": 15.5,
    "nutrition_similarity": 92.3,
    "carbon_reduction": 8.7,
    "taste_score": 8.2,
    "total_score": 0.847
  },
  "summary": "Remplacement réussi des additifs non plant-based...",
  "recommendations": [...]
}
```

---

### Test 4: Optimisation en Lot (2-3 minutes)

**Objectif**: Optimiser plusieurs produits

```bash
# PowerShell
curl -X POST "http://localhost:8000/optimize/batch" `
  -H "Content-Type: application/json" `
  -d '{\"products\":[{\"name\":\"Yaourt\",\"ingredients\":\"lait, sucre, gélatine\"},{\"name\":\"Crème\",\"ingredients\":\"lait, crème fraîche, amidon\"}],\"return_format\":\"simple\"}'
```

---

### Test 5: Script de Test Automatisé (5 minutes)

**Objectif**: Tester tous les scénarios automatiquement

```bash
# Terminal 2 (pendant que l'API tourne dans Terminal 1)
cd plant_based_optimizer
python test_api.py
```

**Ce script teste**:
- ✅ Health check
- ✅ Validation
- ✅ Optimisation simple (avec VOS CODES LLM)
- ✅ Optimisation batch
- ✅ Gestion d'erreurs

---

### Test 6: Documentation Interactive Swagger (2 minutes)

**Objectif**: Tester visuellement avec interface

1. Ouvrir: **http://localhost:8000/docs**
2. Cliquer sur `/optimize` → "Try it out"
3. Entrer:
   ```json
   {
     "name": "Yaourt aux fruits",
     "ingredients": "lait entier, sucre, fraises, gélatine"
   }
   ```
4. Cliquer "Execute"
5. Voir le résultat en temps réel

---

### Test 7: Avec VOS Propres Produits (1 minute par produit)

**Objectif**: Tester avec les produits de votre entreprise

```bash
# Remplacer par vos produits
curl -X POST "http://localhost:8000/optimize?return_format=simple" `
  -H "Content-Type: application/json" `
  -d '{\"name\":\"VOTRE_PRODUIT\",\"ingredients\":\"vos, ingrédients, ici\"}'
```

---

## 🔍 Vérifier que VOS CODES LLM Fonctionnent

### Méthode 1: Logs en Direct

Quand vous lancez `python api_rest.py`, vous verrez:

```
🌱 Initialisation du Plant-Based Optimizer...
✓ Optimiseur initialisé

[Lors d'une optimisation]
📋 ÉTAPE 1: Parsing et Classification des Ingrédients
✓ Produit: Yaourt aux fruits
✓ Stratégie: replace_all_additives

📊 ÉTAPE 2: Enrichissement des Données
✓ 6 ingrédients enrichis

🔬 ÉTAPE 3: Génération et Évaluation des Candidats
✓ 5 candidats générés et évalués

🎓 ÉTAPE 4: Sélection Finale et Justification
✓ Candidat sélectionné: #1
```

**Ces logs prouvent que VOS CODES sont exécutés!**

### Méthode 2: Vérifier les Fichiers Utilisés

```bash
# Vérifier que l'API importe vos codes
cd plant_based_optimizer
python -c "
from api import EnterpriseOptimizer
import inspect
print('Fichiers utilisés:')
print('- optimizer.py:', inspect.getfile(EnterpriseOptimizer.optimizer.__class__))
"
```

### Méthode 3: Test avec Produit Connu

Testez avec un produit dont vous connaissez le résultat attendu:

```bash
curl -X POST "http://localhost:8000/optimize?return_format=detailed" `
  -H "Content-Type: application/json" `
  -d '{\"name\":\"Yaourt nature\",\"ingredients\":\"lait entier, ferments lactiques, gélatine\"}' `
  > result_test.json
```

Vérifiez dans `result_test.json`:
- ✅ Les remplacements suggérés
- ✅ Les scores calculés
- ✅ La justification IA

---

## 📊 Tableau de Tests

| Test | Durée | Vérifie | Commande |
|------|-------|---------|----------|
| Health Check | 10s | API fonctionne | `curl http://localhost:8000/health` |
| Validation | 5s | Format produit | `curl -X POST .../validate` |
| Optimisation Simple | 60s | **VOS CODES LLM** | `curl -X POST .../optimize` |
| Optimisation Batch | 3min | Plusieurs produits | `curl -X POST .../optimize/batch` |
| Script Auto | 5min | Tous les scénarios | `python test_api.py` |
| Swagger UI | 2min | Interface visuelle | http://localhost:8000/docs |
| Vos Produits | 1min | Cas réels | `curl -X POST ...` avec vos données |

---

## ✅ Checklist de Test

### Tests Basiques
- [ ] L'API démarre sans erreur
- [ ] Health check retourne "healthy"
- [ ] Validation fonctionne
- [ ] Documentation Swagger accessible

### Tests Fonctionnels (VOS CODES)
- [ ] Optimisation simple fonctionne
- [ ] Les 4 étapes s'exécutent (logs visibles)
- [ ] Remplacements cohérents
- [ ] Scores calculés correctement
- [ ] Justification IA présente

### Tests Avancés
- [ ] Optimisation batch fonctionne
- [ ] Gestion d'erreurs (produit vide, etc.)
- [ ] Format simple ET détaillé
- [ ] Vos propres produits testés

### Tests d'Intégration
- [ ] Appel depuis JavaScript fonctionne
- [ ] CORS configuré correctement
- [ ] Timeout approprié (60s+)

---

## 🐛 Dépannage

### Problème: "Module not found"
```bash
pip install -r requirements.txt
pip install fastapi uvicorn pydantic
```

### Problème: "Port 8000 already in use"
```bash
# Changer le port
python api_rest.py --port 8001
```

### Problème: "Timeout"
C'est normal! L'optimisation prend 30-60s car elle utilise VOS CODES LLM qui font:
1. Analyse IA (10-20s)
2. Enrichissement données (5-10s)
3. Calculs (5-10s)
4. Sélection IA (10-20s)

### Problème: "LLM ne répond pas"
Vérifiez votre clé API dans `.env`:
```bash
BLACKBOX_API_KEY=votre_cle_api
```

---

## 📝 Exemple de Test Complet

```bash
# Terminal 1: Démarrer l'API
cd plant_based_optimizer
python api_rest.py

# Terminal 2: Tests
cd plant_based_optimizer

# Test 1: Health
curl http://localhost:8000/health

# Test 2: Validation
curl -X POST "http://localhost:8000/validate" `
  -H "Content-Type: application/json" `
  -d '{\"name\":\"Test\",\"ingredients\":\"lait, sucre\"}'

# Test 3: Optimisation (VOS CODES LLM)
curl -X POST "http://localhost:8000/optimize?return_format=simple" `
  -H "Content-Type: application/json" `
  -d '{\"name\":\"Yaourt\",\"ingredients\":\"lait, sucre, gélatine\"}' `
  > result.json

# Voir le résultat
cat result.json

# Test 4: Script complet
python test_api.py
```

---

## 🎯 Confirmation que VOS CODES sont Utilisés

L'API **ne modifie AUCUN de vos codes**. Elle les utilise via:

```python
# Dans api.py
from optimizer import PlantBasedOptimizer  # ← Votre code

class EnterpriseOptimizer:
    def __init__(self):
        self.optimizer = PlantBasedOptimizer()  # ← Utilise VOTRE optimiseur
    
    def optimize_product(self, name, ingredients):
        result = self.optimizer.optimize(product)  # ← Appelle VOTRE code
        return result
```

**Rien n'est modifié!** L'API est juste une **couche HTTP** au-dessus de vos codes existants.

---

## 📞 Support

Si un test échoue:
1. Vérifiez les logs dans le terminal de l'API
2. Consultez `INTEGRATION_ENTREPRISE.md` section "Dépannage"
3. Testez avec `python test_api.py` pour voir les détails

---

**Tous vos codes LLM sont préservés et utilisés! L'API est juste une interface HTTP. 🌱**

# 🏢 Guide d'Intégration Entreprise

## Plant-Based Optimizer - API REST pour Web App

Ce guide explique comment intégrer l'optimiseur plant-based dans votre application web.

---

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Installation](#installation)
3. [Démarrage de l'API](#démarrage-de-lapi)
4. [Utilisation de l'API](#utilisation-de-lapi)
5. [Exemples d'intégration](#exemples-dintégration)
6. [Format des données](#format-des-données)
7. [Gestion des erreurs](#gestion-des-erreurs)
8. [Déploiement](#déploiement)

---

## 🎯 Vue d'ensemble

L'optimiseur est disponible sous deux formes:

1. **API REST** (`api_rest.py`) - Pour intégration web (recommandé)
2. **Module Python** (`api.py`) - Pour intégration dans code Python

### Architecture

```
┌─────────────────┐
│   Web App       │
│  (Frontend)     │
└────────┬────────┘
         │ HTTP/JSON
         ▼
┌─────────────────┐
│   API REST      │
│  (FastAPI)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Optimizer      │
│  (Backend)      │
└─────────────────┘
```

---

## 🚀 Installation

### 1. Prérequis

```bash
Python 3.8+
pip
```

### 2. Installer les dépendances

```bash
cd plant_based_optimizer
pip install -r requirements.txt
```

### 3. Installer les dépendances API

```bash
pip install fastapi uvicorn pydantic python-multipart
```

### 4. Configuration (optionnel)

Créer un fichier `.env` pour la clé API LLM:

```bash
BLACKBOX_API_KEY=votre_cle_api_ici
```

---

## 🎬 Démarrage de l'API

### Mode Développement

```bash
python api_rest.py
```

L'API démarre sur `http://127.0.0.1:8000`

### Mode Production

```bash
uvicorn api_rest:app --host 0.0.0.0 --port 8000 --workers 4
```

### Vérifier que l'API fonctionne

```bash
curl http://localhost:8000/health
```

Réponse attendue:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "message": "API opérationnelle"
}
```

---

## 📡 Utilisation de l'API

### Documentation Interactive

Une fois l'API démarrée, accédez à:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Disponibles

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Informations sur l'API |
| `/health` | GET | Health check |
| `/optimize` | POST | Optimiser un produit |
| `/optimize/batch` | POST | Optimiser plusieurs produits |
| `/validate` | POST | Valider un produit |

---

## 💻 Exemples d'intégration

### 1. JavaScript/TypeScript (Frontend)

#### Optimiser un seul produit

```javascript
async function optimizeProduct(name, ingredients) {
  try {
    const response = await fetch('http://localhost:8000/optimize?return_format=simple', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: name,
        ingredients: ingredients
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Erreur lors de l\'optimisation:', error);
    throw error;
  }
}

// Utilisation
const result = await optimizeProduct(
  "Yaourt aux fruits",
  "lait entier, sucre, fraises, gélatine, arômes naturels"
);

console.log('Remplacements:', result.replacements);
console.log('Scores:', result.scores);
console.log('Résumé:', result.summary);
```

#### Optimiser plusieurs produits

```javascript
async function optimizeBatch(products) {
  const response = await fetch('http://localhost:8000/optimize/batch', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      products: products,
      return_format: 'simple'
    })
  });
  
  return await response.json();
}

// Utilisation
const products = [
  {
    name: "Yaourt aux fruits",
    ingredients: "lait entier, sucre, fraises, gélatine"
  },
  {
    name: "Crème dessert",
    ingredients: "lait, sucre, chocolat, crème fraîche"
  }
];

const results = await optimizeBatch(products);
console.log(`${results.successful}/${results.total_products} produits optimisés`);
```

#### Valider avant d'optimiser

```javascript
async function validateProduct(name, ingredients) {
  const response = await fetch('http://localhost:8000/validate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: name,
      ingredients: ingredients
    })
  });
  
  return await response.json();
}

// Utilisation
const validation = await validateProduct(
  "Yaourt",
  "lait, sucre, fraises"
);

if (!validation.valid) {
  console.error('Problèmes:', validation.issues);
}
if (validation.warnings.length > 0) {
  console.warn('Avertissements:', validation.warnings);
}
```

### 2. React Example

```jsx
import React, { useState } from 'react';

function ProductOptimizer() {
  const [product, setProduct] = useState({ name: '', ingredients: '' });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleOptimize = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/optimize?return_format=simple', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(product)
      });
      
      if (!response.ok) {
        throw new Error('Erreur lors de l\'optimisation');
      }
      
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="optimizer">
      <h2>Optimiseur Plant-Based</h2>
      
      <input
        type="text"
        placeholder="Nom du produit"
        value={product.name}
        onChange={(e) => setProduct({...product, name: e.target.value})}
      />
      
      <textarea
        placeholder="Ingrédients (séparés par des virgules)"
        value={product.ingredients}
        onChange={(e) => setProduct({...product, ingredients: e.target.value})}
      />
      
      <button onClick={handleOptimize} disabled={loading}>
        {loading ? 'Optimisation...' : 'Optimiser'}
      </button>
      
      {error && <div className="error">{error}</div>}
      
      {result && (
        <div className="results">
          <h3>Résultats</h3>
          <p><strong>Stratégie:</strong> {result.strategy}</p>
          
          <h4>Remplacements:</h4>
          <ul>
            {result.replacements.map((r, i) => (
              <li key={i}>{r.original} → {r.replacement}</li>
            ))}
          </ul>
          
          <h4>Scores:</h4>
          <ul>
            <li>Conservation: {result.scores.shelf_life_improvement.toFixed(1)}%</li>
            <li>Nutrition: {result.scores.nutrition_similarity.toFixed(1)}%</li>
            <li>Carbone: {result.scores.carbon_reduction.toFixed(1)}%</li>
            <li>Goût: {result.scores.taste_score.toFixed(1)}/10</li>
          </ul>
          
          <p><strong>Résumé:</strong> {result.summary}</p>
        </div>
      )}
    </div>
  );
}

export default ProductOptimizer;
```

### 3. Python (Backend)

```python
import requests

# Optimiser un produit
def optimize_product(name: str, ingredients: str):
    response = requests.post(
        'http://localhost:8000/optimize',
        params={'return_format': 'simple'},
        json={
            'name': name,
            'ingredients': ingredients
        }
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erreur: {response.status_code} - {response.text}")

# Utilisation
result = optimize_product(
    name="Yaourt aux fruits",
    ingredients="lait entier, sucre, fraises, gélatine"
)

print(f"Stratégie: {result['strategy']}")
print(f"Score total: {result['scores']['total_score']}")
```

### 4. cURL (Tests)

```bash
# Optimiser un produit
curl -X POST "http://localhost:8000/optimize?return_format=simple" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Yaourt aux fruits",
    "ingredients": "lait entier, sucre, fraises, gélatine"
  }'

# Valider un produit
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Yaourt",
    "ingredients": "lait, sucre"
  }'

# Health check
curl http://localhost:8000/health
```

---

## 📊 Format des données

### Requête - Optimiser un produit

```json
{
  "name": "Yaourt aux fruits",
  "ingredients": "lait entier, sucre, fraises, gélatine, arômes naturels, colorant E120"
}
```

### Réponse - Format Simple

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
  "recommendations": [
    "Tester la texture avec l'agar-agar",
    "Ajuster la concentration de colorant naturel",
    "Vérifier la stabilité du produit"
  ]
}
```

### Réponse - Format Détaillé

```json
{
  "success": true,
  "product_name": "Yaourt aux fruits",
  "strategy": "replace_all_additives",
  "replacements": [...],
  "scores": {
    "shelf_life": {
      "original_days": 21.0,
      "new_days": 24.3,
      "improvement_percent": 15.5,
      "score": 0.85
    },
    "nutrition": {
      "similarity_percent": 92.3,
      "original_profile": {...},
      "new_profile": {...},
      "score": 0.92
    },
    "carbon": {
      "original_co2_kg": 2.3,
      "new_co2_kg": 2.1,
      "reduction_percent": 8.7,
      "score": 0.78
    },
    "taste": {
      "similarity": 0.88,
      "overall_score": 8.2,
      "score": 0.82
    },
    "total_score": 0.847
  },
  "summary": "...",
  "recommendations": [...]
}
```

### Requête - Batch

```json
{
  "products": [
    {
      "name": "Yaourt aux fruits",
      "ingredients": "lait entier, sucre, fraises, gélatine"
    },
    {
      "name": "Crème dessert",
      "ingredients": "lait, sucre, chocolat, crème fraîche"
    }
  ],
  "return_format": "simple"
}
```

### Réponse - Batch

```json
{
  "success": true,
  "total_products": 2,
  "successful": 2,
  "failed": 0,
  "results": [
    {
      "success": true,
      "product_index": 0,
      "product_name": "Yaourt aux fruits",
      "result": {...}
    },
    {
      "success": true,
      "product_index": 1,
      "product_name": "Crème dessert",
      "result": {...}
    }
  ]
}
```

---

## ⚠️ Gestion des erreurs

### Codes HTTP

| Code | Signification | Action |
|------|---------------|--------|
| 200 | Succès | Traiter le résultat |
| 400 | Requête invalide | Vérifier les données d'entrée |
| 500 | Erreur serveur | Réessayer ou contacter support |
| 503 | Service indisponible | Attendre et réessayer |

### Exemple de gestion d'erreurs

```javascript
async function optimizeWithErrorHandling(name, ingredients) {
  try {
    const response = await fetch('http://localhost:8000/optimize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, ingredients })
    });
    
    if (response.status === 400) {
      const error = await response.json();
      throw new Error(`Données invalides: ${error.detail}`);
    }
    
    if (response.status === 500) {
      throw new Error('Erreur serveur, veuillez réessayer');
    }
    
    if (response.status === 503) {
      throw new Error('Service temporairement indisponible');
    }
    
    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }
    
    return await response.json();
    
  } catch (error) {
    console.error('Erreur:', error);
    // Afficher un message à l'utilisateur
    // Logger l'erreur
    // Réessayer si approprié
    throw error;
  }
}
```

---

## 🚀 Déploiement

### Option 1: Serveur dédié

```bash
# Installer les dépendances
pip install -r requirements.txt
pip install fastapi uvicorn gunicorn

# Lancer avec Gunicorn (production)
gunicorn api_rest:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Option 2: Docker

Créer un `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi uvicorn

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api_rest:app", "--host", "0.0.0.0", "--port", "8000"]
```

Construire et lancer:

```bash
docker build -t plant-optimizer-api .
docker run -p 8000:8000 plant-optimizer-api
```

### Option 3: Cloud (Heroku, AWS, etc.)

Créer un `Procfile`:

```
web: uvicorn api_rest:app --host 0.0.0.0 --port $PORT
```

---

## 🔒 Sécurité

### Recommandations

1. **CORS**: En production, limiter les origines autorisées
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://votre-domaine.com"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

2. **Rate Limiting**: Limiter le nombre de requêtes par IP

3. **Authentication**: Ajouter une authentification par token si nécessaire

4. **HTTPS**: Utiliser HTTPS en production

---

## 📈 Performance

### Optimisations

- **Cache**: Mettre en cache les résultats fréquents
- **Workers**: Utiliser plusieurs workers (4-8 recommandés)
- **Async**: L'API est déjà asynchrone avec FastAPI
- **Timeout**: Configurer des timeouts appropriés

### Monitoring

```python
# Ajouter des logs
import logging
logging.basicConfig(level=logging.INFO)

# Métriques
from prometheus_client import Counter, Histogram
optimization_counter = Counter('optimizations_total', 'Total optimizations')
optimization_duration = Histogram('optimization_duration_seconds', 'Optimization duration')
```

---

## 🆘 Support

### Problèmes courants

**L'API ne démarre pas**
- Vérifier que le port 8000 est libre
- Vérifier les dépendances: `pip install -r requirements.txt`

**Erreur 503**
- L'optimiseur n'est pas initialisé
- Vérifier les logs au démarrage

**Résultats lents**
- Augmenter le nombre de workers
- Vérifier la connexion au LLM

### Contact

Pour toute question ou problème, consulter:
- Documentation complète: `GUIDE_UTILISATION.md`
- Architecture: `ARCHITECTURE.md`
- Exemples: `examples/`

---

## 📝 Changelog

### Version 1.0.0
- API REST complète avec FastAPI
- Support format simple et détaillé
- Optimisation batch
- Validation de produits
- Documentation interactive (Swagger)
- CORS configuré pour web apps

---

**Bonne intégration! 🌱**

# 🚀 API REST - Plant-Based Optimizer

## Démarrage Rapide (5 minutes)

### 1. Installation

```bash
cd plant_based_optimizer
pip install -r requirements.txt
```

### 2. Démarrer l'API

```bash
python api_rest.py
```

L'API démarre sur: **http://localhost:8000**

### 3. Tester l'API

```bash
# Dans un autre terminal
python test_api.py
```

### 4. Documentation Interactive

Ouvrez dans votre navigateur:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📡 Endpoints Disponibles

### GET `/health`
Vérifie que l'API fonctionne

```bash
curl http://localhost:8000/health
```

### POST `/optimize`
Optimise un seul produit

```bash
curl -X POST "http://localhost:8000/optimize?return_format=simple" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Yaourt aux fruits",
    "ingredients": "lait entier, sucre, fraises, gélatine"
  }'
```

### POST `/optimize/batch`
Optimise plusieurs produits

```bash
curl -X POST "http://localhost:8000/optimize/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "products": [
      {"name": "Yaourt", "ingredients": "lait, sucre, gélatine"},
      {"name": "Crème", "ingredients": "lait, crème, amidon"}
    ],
    "return_format": "simple"
  }'
```

### POST `/validate`
Valide un produit sans l'optimiser

```bash
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Yaourt",
    "ingredients": "lait, sucre"
  }'
```

---

## 💻 Intégration dans votre Web App

### JavaScript/Fetch

```javascript
async function optimizeProduct(name, ingredients) {
  const response = await fetch('http://localhost:8000/optimize?return_format=simple', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, ingredients })
  });
  
  return await response.json();
}

// Utilisation
const result = await optimizeProduct(
  "Yaourt aux fruits",
  "lait entier, sucre, fraises, gélatine"
);

console.log('Remplacements:', result.replacements);
console.log('Score:', result.scores.total_score);
```

### React

```jsx
import { useState } from 'react';

function ProductOptimizer() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleOptimize = async (name, ingredients) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/optimize?return_format=simple', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, ingredients })
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Erreur:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {loading && <p>Optimisation en cours...</p>}
      {result && (
        <div>
          <h3>Résultats</h3>
          <p>Score: {result.scores.total_score}</p>
          {/* Afficher les autres résultats */}
        </div>
      )}
    </div>
  );
}
```

### Python

```python
import requests

def optimize_product(name, ingredients):
    response = requests.post(
        'http://localhost:8000/optimize',
        params={'return_format': 'simple'},
        json={'name': name, 'ingredients': ingredients}
    )
    return response.json()

# Utilisation
result = optimize_product(
    "Yaourt aux fruits",
    "lait entier, sucre, fraises, gélatine"
)

print(f"Score: {result['scores']['total_score']}")
```

---

## 📊 Format des Réponses

### Format Simple (recommandé pour web app)

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
    }
  ],
  "scores": {
    "shelf_life_improvement": 15.5,
    "nutrition_similarity": 92.3,
    "carbon_reduction": 8.7,
    "taste_score": 8.2,
    "total_score": 0.847
  },
  "summary": "Remplacement réussi...",
  "recommendations": [
    "Tester la texture",
    "Ajuster la concentration",
    "Vérifier la stabilité"
  ]
}
```

### Format Détaillé (pour analyse approfondie)

Utilisez `return_format=detailed` pour obtenir toutes les métriques détaillées.

---

## 🔧 Configuration

### Variables d'environnement

Créer un fichier `.env`:

```bash
BLACKBOX_API_KEY=votre_cle_api
```

### CORS

Par défaut, l'API accepte les requêtes de toutes les origines. En production, modifiez `api_rest.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://votre-domaine.com"],  # Spécifier votre domaine
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

---

## 🚀 Déploiement

### Production avec Gunicorn

```bash
pip install gunicorn
gunicorn api_rest:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker

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

```bash
docker build -t plant-optimizer-api .
docker run -p 8000:8000 plant-optimizer-api
```

---

## 📚 Documentation Complète

Pour plus de détails, consultez:
- **[INTEGRATION_ENTREPRISE.md](INTEGRATION_ENTREPRISE.md)** - Guide complet d'intégration
- **[GUIDE_UTILISATION.md](GUIDE_UTILISATION.md)** - Guide d'utilisation général
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Architecture technique

---

## 🆘 Dépannage

### L'API ne démarre pas

```bash
# Vérifier les dépendances
pip install -r requirements.txt
pip install fastapi uvicorn pydantic

# Vérifier que le port 8000 est libre
netstat -an | grep 8000  # Linux/Mac
netstat -an | findstr 8000  # Windows
```

### Erreur 503 (Service Unavailable)

L'optimiseur n'est pas initialisé. Vérifiez les logs au démarrage de l'API.

### Timeout

L'optimisation peut prendre 30-60 secondes. Augmentez le timeout dans votre client:

```javascript
fetch(url, { 
  method: 'POST',
  body: JSON.stringify(data),
  signal: AbortSignal.timeout(120000) // 2 minutes
})
```

---

## 📈 Performance

- **Temps moyen**: 30-60 secondes par produit
- **Concurrent**: Utiliser plusieurs workers (`-w 4`)
- **Cache**: Les résultats peuvent être mis en cache côté client

---

## 🔒 Sécurité

- ✅ Validation des entrées avec Pydantic
- ✅ Gestion des erreurs robuste
- ✅ CORS configurable
- ⚠️ En production: Ajouter authentification et rate limiting

---

## 📝 Exemples de Produits

Voir `templates/products_template.json` et `examples/example_products.json`

---

**Prêt à intégrer! 🌱**

Pour toute question: consultez la documentation complète ou testez avec `python test_api.py`

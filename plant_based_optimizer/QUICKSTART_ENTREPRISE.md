# 🚀 Démarrage Rapide Entreprise

## En 3 étapes simples

### 1️⃣ Installation (2 minutes)

```bash
cd plant_based_optimizer
pip install -r requirements.txt
```

### 2️⃣ Démarrer l'API (30 secondes)

```bash
python api_rest.py
```

✅ L'API est maintenant disponible sur **http://localhost:8000**

### 3️⃣ Tester (1 minute)

Ouvrez votre navigateur: **http://localhost:8000/docs**

Ou testez avec le script:
```bash
python test_api.py
```

---

## 💡 Utilisation Simple

### Depuis votre Web App (JavaScript)

```javascript
// Optimiser un produit
const response = await fetch('http://localhost:8000/optimize?return_format=simple', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: "Yaourt aux fruits",
    ingredients: "lait entier, sucre, fraises, gélatine, arômes naturels"
  })
});

const result = await response.json();

// Afficher les résultats
console.log('Remplacements:', result.replacements);
console.log('Score total:', result.scores.total_score);
console.log('Résumé:', result.summary);
```

### Exemple de Réponse

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
  "summary": "Remplacement réussi des additifs non plant-based...",
  "recommendations": [
    "Tester la texture avec l'agar-agar",
    "Ajuster la concentration",
    "Vérifier la stabilité du produit"
  ]
}
```

---

## 📋 Format d'Entrée

### Un seul produit

```json
{
  "name": "Nom du produit",
  "ingredients": "ingrédient1, ingrédient2, ingrédient3, ..."
}
```

### Plusieurs produits (batch)

```json
{
  "products": [
    {
      "name": "Produit 1",
      "ingredients": "ingrédient1, ingrédient2, ..."
    },
    {
      "name": "Produit 2",
      "ingredients": "ingrédient1, ingrédient2, ..."
    }
  ],
  "return_format": "simple"
}
```

---

## 🎯 Endpoints Principaux

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/health` | GET | Vérifier que l'API fonctionne |
| `/optimize` | POST | Optimiser un produit |
| `/optimize/batch` | POST | Optimiser plusieurs produits |
| `/validate` | POST | Valider un produit |

---

## 📚 Documentation Complète

- **[API_README.md](API_README.md)** - Guide API complet
- **[INTEGRATION_ENTREPRISE.md](INTEGRATION_ENTREPRISE.md)** - Guide d'intégration détaillé
- **http://localhost:8000/docs** - Documentation interactive (Swagger)

---

## 🆘 Besoin d'Aide?

### L'API ne démarre pas?

```bash
# Réinstaller les dépendances
pip install -r requirements.txt
pip install fastapi uvicorn pydantic
```

### Tester manuellement?

```bash
# Health check
curl http://localhost:8000/health

# Optimiser un produit
curl -X POST "http://localhost:8000/optimize?return_format=simple" \
  -H "Content-Type: application/json" \
  -d '{"name":"Yaourt","ingredients":"lait, sucre, gélatine"}'
```

---

## 🚀 Prêt pour la Production?

Voir **[INTEGRATION_ENTREPRISE.md](INTEGRATION_ENTREPRISE.md)** section "Déploiement"

---

**C'est tout! Vous êtes prêt à intégrer l'optimiseur dans votre web app! 🌱**

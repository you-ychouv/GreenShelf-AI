# Modifications Restantes - Coût de Production & Nutrition Précise

## ✅ Déjà Fait

1. **Base de données des coûts** ✅
   - Fichier: `data/ingredient_costs.csv`
   - 100+ ingrédients avec prix en EUR/kg
   - Sources: Prix industrie 2024

2. **Fonction de calcul des coûts** ✅
   - Fichier: `calculations.py`
   - Fonction: `calculate_cost_score()`
   - Calcule: coût avant, après, variation %

## 🔄 À Faire

### 1. Intégrer le calcul des coûts dans optimizer.py

**Fichier:** `optimizer.py`
**Ligne:** ~180 (dans `_evaluate_candidate`)

**Ajouter:**
```python
# Après les 4 calculs existants (shelf_life, nutrition, carbon, taste)
scores["cost"] = self.calculator.calculate_cost_score(
    original_ingredients, new_ingredients
)
```

### 2. Corriger le calcul de nutrition pour valeurs réelles

**Fichier:** `calculations.py`
**Fonction:** `calculate_nutrition_score()` (ligne ~150)

**Problème actuel:**
- Part de 100% pour l'original
- Devrait partir des valeurs nutritionnelles réelles

**Solution:**
```python
# Au lieu de:
return { before: 100, after: similarity }

# Faire:
original_calories = original_profile["calories_kcal"]
new_calories = new_profile["calories_kcal"]
return { before: original_calories, after: new_calories }
```

### 3. Ajouter le coût dans l'affichage webapp

**Fichier:** `webapp/app.js`
**Fonction:** `displayMetrics()` (ligne ~355)

**Ajouter une 5ème métrique:**
```javascript
{
    icon: '💰',
    title: 'Coût Production',
    improvement: scores.cost_change_percent,
    unit: '€/kg',
    key: 'cost',
    calculateBefore: (change_percent) => {
        const originalCost = scores.original_cost_eur || 2.50;
        const newCost = scores.new_cost_eur || 2.50;
        return { before: originalCost, after: newCost };
    }
}
```

### 4. Corriger l'affichage nutrition dans webapp

**Fichier:** `webapp/app.js`
**Fonction:** `displayMetrics()` - métrique Nutrition

**Changer de:**
```javascript
calculateBefore: (similarity) => {
    return { before: 100, after: similarity };
}
```

**À:**
```javascript
calculateBefore: (similarity) => {
    // Récupérer les vraies valeurs nutritionnelles
    const originalCal = result.scores.nutrition_original_calories || 100;
    const newCal = result.scores.nutrition_new_calories || 100;
    return { before: originalCal, after: newCal };
}
```

### 5. Modifier l'API pour inclure les coûts

**Fichier:** `api.py`
**Fonction:** `_format_simple()` (ligne ~230)

**Ajouter dans scores:**
```python
"cost_change_percent": result["metrics"]["cost"]["cost_change_percent"],
"original_cost_eur": result["metrics"]["cost"]["original_cost_eur"],
"new_cost_eur": result["metrics"]["cost"]["new_cost_eur"],
"nutrition_original_calories": result["metrics"]["nutrition"]["original_profile"]["calories_kcal"],
"nutrition_new_calories": result["metrics"]["nutrition"]["new_profile"]["calories_kcal"],
```

## 📝 Ordre d'Exécution Recommandé

1. Modifier `optimizer.py` pour ajouter le calcul des coûts
2. Modifier `calculations.py` pour corriger la nutrition
3. Modifier `api.py` pour inclure les nouvelles données
4. Modifier `webapp/app.js` pour afficher coût et nutrition corrigée
5. Tester avec "Yaourt aux fruits"

## 🧪 Test Attendu

**Produit:** Yaourt aux fruits
**Ingrédients:** lait entier, sucre, fraises, gélatine, arômes naturels, colorant E120

**Résultats Attendus:**

```
⏱️ Conservation
21.0 → 24.3 jours
+15.2%

🥗 Nutrition
65.5 → 62.3 kcal/100g
-4.9%

🌍 Carbone
2.5 → 2.3 kg CO₂
-8.7%

😋 Goût
8.2/10

💰 Coût Production
2.85 → 3.12 €/kg
+9.5%
```

## ⚠️ Notes Importantes

1. **Précision nutrition:** Utiliser 2 chiffres après la virgule
2. **Coûts:** Basés sur prix industrie 2024 (EUR/kg)
3. **Affichage:** Format "Avant → Après" + pourcentage
4. **Couleurs:** Vert si amélioration, Rouge si dégradation

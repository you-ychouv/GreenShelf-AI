# Code à ajouter à calculations.py

def calculate_cost_score(
    self, 
    original_ingredients: List[Dict[str, Any]], 
    new_ingredients: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Calcule le coût de production et la variation
    
    Returns:
        Dict avec coût original, nouveau coût, et variation en %
    """
    # Coût total pour chaque formulation
    original_cost = self._calculate_total_cost(original_ingredients)
    new_cost = self._calculate_total_cost(new_ingredients)
    
    # Variation en pourcentage
    if original_cost > 0:
        cost_change_percent = ((new_cost - original_cost) / original_cost) * 100
    else:
        cost_change_percent = 0.0
    
    # Détails par ingrédient
    original_details = self._get_cost_details(original_ingredients)
    new_details = self._get_cost_details(new_ingredients)
    
    return {
        "original_cost_eur": round(original_cost, 2),
        "new_cost_eur": round(new_cost, 2),
        "cost_change_percent": round(cost_change_percent, 2),
        "cost_change_eur": round(new_cost - original_cost, 2),
        "original_details": original_details,
        "new_details": new_details
    }

def _calculate_total_cost(self, ingredients: List[Dict[str, Any]]) -> float:
    """
    Calcule le coût total des ingrédients (en EUR pour 1kg de produit fini)
    Suppose des proportions égales si non spécifiées
    """
    if not ingredients:
        return 0.0
    
    total_cost = 0.0
    n = len(ingredients)
    
    # Quantité par ingrédient (supposée égale)
    qty_per_ingredient = 1.0 / n  # kg
    
    for ing in ingredients:
        ing_name = ing.get("name", "").lower().strip()
        
        # Chercher le coût dans la base de données
        cost_per_kg = self._get_ingredient_cost(ing_name)
        
        # Coût pour cet ingrédient
        total_cost += cost_per_kg * qty_per_ingredient
    
    return total_cost

def _get_ingredient_cost(self, ingredient_name: str) -> float:
    """
    Récupère le coût d'un ingrédient depuis la base de données
    """
    if self.costs_data.empty:
        return 2.50  # Coût par défaut si pas de données
    
    # Normaliser le nom
    ingredient_name = ingredient_name.lower().strip()
    
    # Chercher une correspondance exacte
    match = self.costs_data[self.costs_data['ingredient'].str.lower() == ingredient_name]
    
    if not match.empty:
        return float(match.iloc[0]['cost_per_kg_eur'])
    
    # Chercher une correspondance partielle
    for idx, row in self.costs_data.iterrows():
        db_ingredient = row['ingredient'].lower()
        if db_ingredient in ingredient_name or ingredient_name in db_ingredient:
            return float(row['cost_per_kg_eur'])
    
    # Coût par défaut si non trouvé
    return 2.50

def _get_cost_details(self, ingredients: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Retourne les détails de coût pour chaque ingrédient
    """
    details = []
    n = len(ingredients) if ingredients else 1
    qty_per_ingredient = 1.0 / n
    
    for ing in ingredients:
        ing_name = ing.get("name", "")
        cost_per_kg = self._get_ingredient_cost(ing_name.lower())
        total_cost = cost_per_kg * qty_per_ingredient
        
        details.append({
            "ingredient": ing_name,
            "quantity_kg": round(qty_per_ingredient, 3),
            "cost_per_kg_eur": round(cost_per_kg, 2),
            "total_cost_eur": round(total_cost, 2)
        })
    
    return details

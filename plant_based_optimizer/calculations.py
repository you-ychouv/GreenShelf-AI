"""
Calculations - ÉTAPE 3
Effectue tous les calculs scientifiques:
- Durée de conservation (modèles biologiques)
- Similarité nutritionnelle
- Empreinte carbone
- Score gustatif
- Coût de production
- Scoring multi-objectifs
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
import config
import os


class Calculator:
    """Gestionnaire des calculs scientifiques"""
    
    def __init__(self):
        self.weights = config.WEIGHTS
        self.shelf_life_params = config.SHELF_LIFE_PARAMS
        
        # Charger les données de coûts
        self.costs_data = self._load_costs_data()
    
    def _load_costs_data(self) -> pd.DataFrame:
        """Charge les données de coûts des ingrédients"""
        try:
            costs_path = os.path.join(os.path.dirname(__file__), "data", "ingredient_costs.csv")
            df = pd.read_csv(costs_path, encoding='utf-8')
            return df
        except Exception as e:
            print(f"⚠️ Erreur chargement coûts: {e}")
            return pd.DataFrame(columns=['ingredient', 'cost_per_kg_eur'])
    
    def calculate_shelf_life_score(
        self, 
        original_ingredients: List[Dict[str, Any]], 
        new_ingredients: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calcule le score de durée de conservation
        Basé sur des modèles de croissance microbienne et facteurs biologiques
        
        Args:
            original_ingredients: Liste des ingrédients originaux enrichis
            new_ingredients: Liste des nouveaux ingrédients enrichis
        
        Returns:
            Dict avec score et détails
        """
        # Calcul pour formulation originale
        original_shelf_life = self._estimate_shelf_life(original_ingredients)
        
        # Calcul pour nouvelle formulation
        new_shelf_life = self._estimate_shelf_life(new_ingredients)
        
        # Amélioration en pourcentage
        improvement = ((new_shelf_life - original_shelf_life) / original_shelf_life) * 100
        
        # Score normalisé (0-1)
        # Positif si amélioration, pénalité si dégradation
        if improvement >= 0:
            score = min(1.0, 0.5 + (improvement / 100))  # Max 1.0
        else:
            score = max(0.0, 0.5 + (improvement / 100))  # Min 0.0
        
        return {
            "score": score,
            "original_days": original_shelf_life,
            "new_days": new_shelf_life,
            "improvement_percent": improvement,
            "details": {
                "original_ph": self._calculate_avg_ph(original_ingredients),
                "new_ph": self._calculate_avg_ph(new_ingredients),
                "original_aw": self._calculate_avg_aw(original_ingredients),
                "new_aw": self._calculate_avg_aw(new_ingredients),
                "antimicrobial_boost": self._calculate_antimicrobial_score(new_ingredients) - 
                                      self._calculate_antimicrobial_score(original_ingredients)
            }
        }
    
    def _estimate_shelf_life(self, ingredients: List[Dict[str, Any]]) -> float:
        """
        Estime la durée de conservation en jours
        Basé sur le modèle de croissance microbienne et facteurs intrinsèques
        """
        # Facteurs moyens
        avg_ph = self._calculate_avg_ph(ingredients)
        avg_aw = self._calculate_avg_aw(ingredients)
        antimicrobial = self._calculate_antimicrobial_score(ingredients)
        
        # Durée de base (jours) à température de réfrigération
        base_shelf_life = 7.0
        
        # Facteur pH (optimal = 6.5)
        ph_optimal = self.shelf_life_params["ph_optimal"]
        ph_factor = 1.0 + (0.2 * abs(avg_ph - ph_optimal))  # Plus on s'éloigne, plus c'est stable
        
        # Facteur Aw (optimal = 0.95, plus bas = plus stable)
        aw_optimal = self.shelf_life_params["aw_optimal"]
        aw_factor = 1.0 + (2.0 * (aw_optimal - avg_aw))  # Aw plus bas = meilleure conservation
        
        # Facteur antimicrobien (0-10, plus élevé = meilleure conservation)
        antimicrobial_factor = 1.0 + (antimicrobial / 10.0)
        
        # Calcul final
        estimated_days = base_shelf_life * ph_factor * aw_factor * antimicrobial_factor
        
        return max(1.0, estimated_days)  # Minimum 1 jour
    
    def _calculate_avg_ph(self, ingredients: List[Dict[str, Any]]) -> float:
        """Calcule le pH moyen pondéré"""
        if not ingredients:
            return 6.5
        
        ph_values = []
        for ing in ingredients:
            biological = ing.get("enriched_data", {}).get("biological", {})
            ph_values.append(biological.get("ph", 6.5))
        
        return np.mean(ph_values)
    
    def _calculate_avg_aw(self, ingredients: List[Dict[str, Any]]) -> float:
        """Calcule l'activité de l'eau moyenne"""
        if not ingredients:
            return 0.95
        
        aw_values = []
        for ing in ingredients:
            biological = ing.get("enriched_data", {}).get("biological", {})
            aw_values.append(biological.get("water_activity", 0.95))
        
        return np.mean(aw_values)
    
    def _calculate_antimicrobial_score(self, ingredients: List[Dict[str, Any]]) -> float:
        """Calcule le score antimicrobien total"""
        if not ingredients:
            return 0.0
        
        scores = []
        for ing in ingredients:
            biological = ing.get("enriched_data", {}).get("biological", {})
            scores.append(biological.get("antimicrobial_score", 0))
        
        return np.sum(scores)  # Somme car effets cumulatifs
    
    def calculate_nutrition_score(
        self, 
        original_ingredients: List[Dict[str, Any]], 
        new_ingredients: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calcule la similarité nutritionnelle
        
        Returns:
            Dict avec score de similarité (0-1) et détails
        """
        # Profils nutritionnels
        original_profile = self._calculate_nutrition_profile(original_ingredients)
        new_profile = self._calculate_nutrition_profile(new_ingredients)
        
        # Calcul de similarité pour chaque nutriment
        similarities = {}
        for nutrient in ["protein_g", "fat_g", "carbs_g", "fiber_g", "calories_kcal"]:
            original_val = original_profile.get(nutrient, 0)
            new_val = new_profile.get(nutrient, 0)
            
            if original_val == 0 and new_val == 0:
                similarities[nutrient] = 1.0
            elif original_val == 0:
                similarities[nutrient] = 0.0
            else:
                # Similarité basée sur la différence relative
                diff = abs(new_val - original_val) / original_val
                similarities[nutrient] = max(0.0, 1.0 - diff)
        
        # Score global (moyenne pondérée)
        weights = {
            "protein_g": 0.30,
            "fat_g": 0.20,
            "carbs_g": 0.20,
            "fiber_g": 0.15,
            "calories_kcal": 0.15
        }
        
        total_score = sum(similarities[k] * weights[k] for k in weights.keys())
        
        return {
            "score": total_score,
            "original_profile": original_profile,
            "new_profile": new_profile,
            "similarities": similarities,
            "meets_threshold": total_score >= config.MIN_NUTRITION_SIMILARITY
        }
    
    def _calculate_nutrition_profile(self, ingredients: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calcule le profil nutritionnel total (pour 100g de produit)"""
        profile = {
            "protein_g": 0.0,
            "fat_g": 0.0,
            "carbs_g": 0.0,
            "fiber_g": 0.0,
            "calories_kcal": 0.0,
            "water_g": 0.0
        }
        
        # Somme des nutriments (en supposant proportions égales)
        # Dans un cas réel, il faudrait les proportions exactes
        n = len(ingredients) if ingredients else 1
        
        for ing in ingredients:
            nutrition = ing.get("enriched_data", {}).get("nutrition", {})
            for key in profile.keys():
                profile[key] += nutrition.get(key, 0) / n
        
        return profile
    
    def calculate_carbon_score(
        self, 
        original_ingredients: List[Dict[str, Any]], 
        new_ingredients: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calcule le score d'empreinte carbone
        
        Returns:
            Dict avec score de réduction et détails
        """
        # Empreinte totale
        original_carbon = self._calculate_total_carbon(original_ingredients)
        new_carbon = self._calculate_total_carbon(new_ingredients)
        
        # Réduction en pourcentage
        reduction = ((original_carbon - new_carbon) / original_carbon) * 100
        
        # Score normalisé (0-1)
        # Positif si réduction, pénalité si augmentation
        if reduction >= 0:
            score = min(1.0, reduction / 100)  # Max 1.0 pour 100% réduction
        else:
            score = 0.0  # Pénalité totale si augmentation
        
        return {
            "score": score,
            "original_co2_kg": original_carbon,
            "new_co2_kg": new_carbon,
            "reduction_percent": reduction,
            "meets_threshold": new_carbon <= original_carbon  # Pas d'augmentation
        }
    
    def _calculate_total_carbon(self, ingredients: List[Dict[str, Any]]) -> float:
        """Calcule l'empreinte carbone totale (kg CO2eq)"""
        if not ingredients:
            return 0.0
        
        total = 0.0
        n = len(ingredients)
        
        for ing in ingredients:
            carbon = ing.get("enriched_data", {}).get("carbon_footprint", {})
            total += carbon.get("co2_kg_per_kg", 0) / n
        
        return total
    
    def calculate_taste_score(
        self, 
        original_ingredients: List[Dict[str, Any]], 
        new_ingredients: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calcule le score gustatif
        
        Returns:
            Dict avec score de similarité gustative
        """
        # Profils gustatifs
        original_profile = self._calculate_taste_profile(original_ingredients)
        new_profile = self._calculate_taste_profile(new_ingredients)
        
        # Similarité des profils (distance euclidienne normalisée)
        taste_dimensions = ["sweetness", "saltiness", "sourness", "bitterness", "umami"]
        
        distances = []
        for dim in taste_dimensions:
            diff = abs(original_profile[dim] - new_profile[dim])
            distances.append(diff)
        
        # Distance moyenne (0-10)
        avg_distance = np.mean(distances)
        
        # Score de similarité (0-1)
        similarity_score = max(0.0, 1.0 - (avg_distance / 10.0))
        
        # Score global basé sur le score overall du nouveau profil
        overall_score = new_profile["overall_score"] / 10.0
        
        # Combinaison: 60% similarité + 40% qualité absolue
        final_score = (0.6 * similarity_score) + (0.4 * overall_score)
        
        return {
            "score": final_score,
            "original_profile": original_profile,
            "new_profile": new_profile,
            "similarity": similarity_score,
            "overall_quality": overall_score,
            "meets_threshold": new_profile["overall_score"] >= config.MIN_TASTE_SCORE
        }
    
    def _calculate_taste_profile(self, ingredients: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calcule le profil gustatif moyen"""
        profile = {
            "sweetness": 0.0,
            "saltiness": 0.0,
            "sourness": 0.0,
            "bitterness": 0.0,
            "umami": 0.0,
            "overall_score": 0.0
        }
        
        if not ingredients:
            return profile
        
        n = len(ingredients)
        
        for ing in ingredients:
            taste = ing.get("enriched_data", {}).get("taste_profile", {})
            for key in profile.keys():
                profile[key] += taste.get(key, 5.0) / n
        
        return profile
    
    def calculate_total_score(self, scores: Dict[str, Dict[str, Any]]) -> float:
        """
        Calcule le score total multi-objectifs
        
        Args:
            scores: Dict avec les 4 scores (shelf_life, nutrition, carbon, taste)
        
        Returns:
            Score total pondéré (0-1)
        """
        total = 0.0
        
        total += scores["shelf_life"]["score"] * self.weights["shelf_life"]
        total += scores["nutrition"]["score"] * self.weights["nutrition"]
        total += scores["carbon"]["score"] * self.weights["carbon"]
        total += scores["taste"]["score"] * self.weights["taste"]
        
        return total
    
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
    
    def is_valid_candidate(self, scores: Dict[str, Dict[str, Any]]) -> Tuple[bool, List[str]]:
        """
        Vérifie si un candidat respecte tous les seuils
        
        Returns:
            (is_valid, list_of_violations)
        """
        violations = []
        
        # Vérifier nutrition
        if not scores["nutrition"].get("meets_threshold", False):
            violations.append(f"Similarité nutritionnelle insuffisante: {scores['nutrition']['score']:.2%}")
        
        # Vérifier carbone
        if not scores["carbon"].get("meets_threshold", False):
            violations.append(f"Empreinte carbone augmentée: {scores['carbon']['reduction_percent']:.1f}%")
        
        # Vérifier goût
        if not scores["taste"].get("meets_threshold", False):
            violations.append(f"Score gustatif insuffisant: {scores['taste']['new_profile']['overall_score']:.1f}/10")
        
        is_valid = len(violations) == 0
        
        return is_valid, violations

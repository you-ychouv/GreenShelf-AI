"""
API Module - Interface simplifiée pour intégration entreprise
Permet d'utiliser l'optimiseur de manière programmatique
"""

from typing import Dict, List, Any, Optional
from optimizer import PlantBasedOptimizer
import json


class EnterpriseOptimizer:
    """
    Interface simplifiée pour l'optimisation plant-based
    Conçue pour une intégration facile dans des applications web
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialise l'optimiseur
        
        Args:
            api_key: Clé API pour le LLM (optionnel, utilise variable d'environnement si non fourni)
        """
        self.optimizer = PlantBasedOptimizer(api_key)
    
    def optimize_product(
        self, 
        name: str, 
        ingredients: str,
        return_format: str = "detailed"
    ) -> Dict[str, Any]:
        """
        Optimise un seul produit
        
        Args:
            name: Nom du produit
            ingredients: Liste des ingrédients (séparés par des virgules)
            return_format: Format de retour ("detailed" ou "simple")
        
        Returns:
            Dict contenant les résultats de l'optimisation
            
        Raises:
            ValueError: Si les paramètres sont invalides
            Exception: Si l'optimisation échoue
            
        Example:
            >>> optimizer = EnterpriseOptimizer()
            >>> result = optimizer.optimize_product(
            ...     name="Yaourt aux fruits",
            ...     ingredients="lait entier, sucre, fraises, gélatine"
            ... )
        """
        # Validation
        if not name or not name.strip():
            raise ValueError("Le nom du produit ne peut pas être vide")
        
        if not ingredients or not ingredients.strip():
            raise ValueError("La liste des ingrédients ne peut pas être vide")
        
        # Préparer le produit
        product = {
            "name": name.strip(),
            "ingredients": ingredients.strip()
        }
        
        try:
            # Optimiser
            result = self.optimizer.optimize(product)
            
            # Formater selon le format demandé
            if return_format == "simple":
                return self._format_simple(result)
            else:
                return result
                
        except Exception as e:
            raise Exception(f"Erreur lors de l'optimisation: {str(e)}")
    
    def optimize_batch(
        self, 
        products: List[Dict[str, str]],
        return_format: str = "detailed"
    ) -> List[Dict[str, Any]]:
        """
        Optimise plusieurs produits en lot
        
        Args:
            products: Liste de dicts avec 'name' et 'ingredients'
            return_format: Format de retour ("detailed" ou "simple")
        
        Returns:
            Liste des résultats d'optimisation
            
        Raises:
            ValueError: Si la liste de produits est invalide
            
        Example:
            >>> optimizer = EnterpriseOptimizer()
            >>> products = [
            ...     {"name": "Yaourt", "ingredients": "lait, sucre, gélatine"},
            ...     {"name": "Crème", "ingredients": "lait, crème, amidon"}
            ... ]
            >>> results = optimizer.optimize_batch(products)
        """
        # Validation
        if not products or not isinstance(products, list):
            raise ValueError("La liste de produits doit être une liste non vide")
        
        if len(products) == 0:
            raise ValueError("La liste de produits ne peut pas être vide")
        
        results = []
        errors = []
        
        for i, product in enumerate(products):
            try:
                # Valider le format du produit
                if not isinstance(product, dict):
                    raise ValueError(f"Produit {i+1}: Format invalide (doit être un dict)")
                
                if "name" not in product or "ingredients" not in product:
                    raise ValueError(f"Produit {i+1}: Champs 'name' et 'ingredients' requis")
                
                # Optimiser
                result = self.optimize_product(
                    name=product["name"],
                    ingredients=product["ingredients"],
                    return_format=return_format
                )
                
                results.append({
                    "success": True,
                    "product_index": i,
                    "product_name": product["name"],
                    "result": result
                })
                
            except Exception as e:
                errors.append({
                    "success": False,
                    "product_index": i,
                    "product_name": product.get("name", "Inconnu"),
                    "error": str(e)
                })
        
        # Retourner tous les résultats (succès et erreurs)
        return results + errors
    
    def validate_product(self, name: str, ingredients: str) -> Dict[str, Any]:
        """
        Valide un produit sans l'optimiser
        
        Args:
            name: Nom du produit
            ingredients: Liste des ingrédients
        
        Returns:
            Dict avec le statut de validation et les messages
            
        Example:
            >>> optimizer = EnterpriseOptimizer()
            >>> validation = optimizer.validate_product(
            ...     name="Yaourt",
            ...     ingredients="lait, sucre"
            ... )
        """
        issues = []
        warnings = []
        
        # Vérifier le nom
        if not name or not name.strip():
            issues.append("Le nom du produit est requis")
        elif len(name.strip()) < 3:
            warnings.append("Le nom du produit est très court")
        
        # Vérifier les ingrédients
        if not ingredients or not ingredients.strip():
            issues.append("La liste des ingrédients est requise")
        else:
            ing_list = [i.strip() for i in ingredients.split(",")]
            
            if len(ing_list) < 2:
                warnings.append("Le produit contient très peu d'ingrédients")
            
            if len(ing_list) > 50:
                warnings.append("Le produit contient beaucoup d'ingrédients")
            
            # Vérifier les ingrédients vides
            empty_ingredients = [i for i in ing_list if not i]
            if empty_ingredients:
                issues.append(f"{len(empty_ingredients)} ingrédient(s) vide(s) détecté(s)")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "ingredient_count": len([i.strip() for i in ingredients.split(",")]) if ingredients else 0
        }
    
    def _format_simple(self, detailed_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formate le résultat en version simplifiée pour l'API
        
        Args:
            detailed_result: Résultat détaillé de l'optimisation
        
        Returns:
            Version simplifiée du résultat
        """
        # Gestion sécurisée des clés qui peuvent ne pas exister
        try:
            product_name = detailed_result.get("original_product", {}).get("name", "Produit")
            strategy = detailed_result.get("strategy", "unknown")
            replacements = detailed_result.get("optimized_product", {}).get("replacements", [])
            
            metrics = detailed_result.get("metrics", {})
            shelf_life = metrics.get("shelf_life", {})
            nutrition = metrics.get("nutrition", {})
            carbon = metrics.get("carbon", {})
            taste = metrics.get("taste", {})
            
            justification = detailed_result.get("justification", {})
            recommendations = detailed_result.get("recommendations", [])
            
            # Extraire les données de coût
            cost = metrics.get("cost", {})
            
            # Extraire les valeurs nutritionnelles réelles
            original_profile = nutrition.get("original_profile", {})
            new_profile = nutrition.get("new_profile", {})
            
            return {
                "product_name": product_name,
                "strategy": strategy,
                "replacements": replacements,
                "scores": {
                    "shelf_life_improvement": shelf_life.get("improvement_percent", 0),
                    "nutrition_similarity": nutrition.get("similarity_percent", 0),
                    "nutrition_original_calories": round(original_profile.get("calories_kcal", 0), 2),
                    "nutrition_new_calories": round(new_profile.get("calories_kcal", 0), 2),
                    "carbon_reduction": carbon.get("reduction_percent", 0),
                    "taste_score": taste.get("overall_score", 0),
                    "cost_change_percent": cost.get("cost_change_percent", 0),
                    "original_cost_eur": cost.get("original_cost_eur", 0),
                    "new_cost_eur": cost.get("new_cost_eur", 0),
                    "total_score": metrics.get("total_score", 0)
                },
                "summary": justification.get("summary", "Optimisation effectuée"),
                "top_recommendations": recommendations[:3] if recommendations else []
            }
        except Exception as e:
            # En cas d'erreur, retourner un format minimal
            return {
                "product_name": "Erreur",
                "strategy": "unknown",
                "replacements": [],
                "scores": {
                    "shelf_life_improvement": 0,
                    "nutrition_similarity": 0,
                    "carbon_reduction": 0,
                    "taste_score": 0,
                    "total_score": 0
                },
                "summary": f"Erreur de formatage: {str(e)}",
                "top_recommendations": []
            }
    
    def get_optimization_summary(self, result: Dict[str, Any]) -> str:
        """
        Génère un résumé textuel de l'optimisation
        
        Args:
            result: Résultat de l'optimisation
        
        Returns:
            Résumé textuel
        """
        summary_parts = [
            f"Produit: {result['original_product']['name']}",
            f"Stratégie: {result['strategy']}",
            f"\nRemplacements ({len(result['optimized_product']['replacements'])}):"
        ]
        
        for repl in result['optimized_product']['replacements']:
            summary_parts.append(f"  • {repl['original']} → {repl['replacement']}")
        
        metrics = result['metrics']
        summary_parts.extend([
            f"\nMétriques:",
            f"  • Conservation: {metrics['shelf_life']['improvement_percent']:+.1f}%",
            f"  • Nutrition: {metrics['nutrition']['similarity_percent']:.1f}%",
            f"  • Carbone: {metrics['carbon']['reduction_percent']:.1f}%",
            f"  • Goût: {metrics['taste']['overall_score']:.1f}/10",
            f"  • Score total: {metrics['total_score']:.3f}"
        ])
        
        return "\n".join(summary_parts)


# Fonctions utilitaires pour usage direct

def optimize_single_product(name: str, ingredients: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Fonction utilitaire pour optimiser un seul produit
    
    Args:
        name: Nom du produit
        ingredients: Liste des ingrédients
        api_key: Clé API (optionnel)
    
    Returns:
        Résultat de l'optimisation
    """
    optimizer = EnterpriseOptimizer(api_key)
    return optimizer.optimize_product(name, ingredients)


def optimize_from_json_file(filepath: str, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Optimise des produits depuis un fichier JSON
    
    Args:
        filepath: Chemin vers le fichier JSON
        api_key: Clé API (optionnel)
    
    Returns:
        Liste des résultats
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    optimizer = EnterpriseOptimizer(api_key)
    return optimizer.optimize_batch(products)

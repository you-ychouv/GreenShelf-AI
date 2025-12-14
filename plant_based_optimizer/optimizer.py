"""
Main Optimizer - Orchestration des 4 étapes
Coordonne le flux complet d'optimisation
"""

from typing import Dict, List, Any
import json
import copy
from llm_handler import LLMHandler
from data_enrichment import DataEnrichment
from calculations import Calculator
import config


class PlantBasedOptimizer:
    """Optimiseur principal pour la transformation plant-based"""
    
    def __init__(self, api_key: str = None):
        print("🌱 Initialisation du Plant-Based Optimizer...")
        self.llm = LLMHandler(api_key)
        self.data_enrichment = DataEnrichment()
        self.calculator = Calculator()
        print("✓ Optimiseur initialisé\n")
    
    def optimize(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processus complet d'optimisation
        
        Args:
            product: Dict avec 'name' et 'ingredients'
        
        Returns:
            Dict avec la recommandation finale
        """
        print(f"{'='*60}")
        print(f"🎯 OPTIMISATION: {product.get('name', 'Produit')}")
        print(f"{'='*60}\n")
        
        # ÉTAPE 1: LLM - Parsing & Classification
        print("📋 ÉTAPE 1: Parsing et Classification des Ingrédients")
        print("-" * 60)
        parsed_data = self.llm.parse_and_classify_ingredients(product)
        
        if not parsed_data:
            return {"error": "Échec du parsing des ingrédients"}
        
        print(f"✓ Produit: {parsed_data['product_name']}")
        print(f"✓ Stratégie: {parsed_data['strategy']}")
        print(f"✓ Ingrédients non plant-based: {parsed_data['non_plant_based_count']}")
        print(f"✓ Conservateurs/additifs non plant-based: {parsed_data['non_plant_based_additives_count']}\n")
        
        # ÉTAPE 2: Database - Enrichissement
        print("📊 ÉTAPE 2: Enrichissement des Données")
        print("-" * 60)
        enriched_original = self._enrich_ingredients(parsed_data['ingredients'])
        print(f"✓ {len(enriched_original)} ingrédients enrichis\n")
        
        # ÉTAPE 3: Calculs - Génération des candidats
        print("🔬 ÉTAPE 3: Génération et Évaluation des Candidats")
        print("-" * 60)
        candidates = self._generate_candidates(parsed_data, enriched_original)
        
        if not candidates:
            return {"error": "Aucun candidat valide généré"}
        
        print(f"✓ {len(candidates)} candidats générés et évalués\n")
        
        # ÉTAPE 4: LLM - Sélection & Justification
        print("🎓 ÉTAPE 4: Sélection Finale et Justification")
        print("-" * 60)
        selection = self.llm.select_and_justify(candidates, parsed_data)
        
        if not selection:
            return {"error": "Échec de la sélection finale"}
        
        # Construire le résultat final
        selected_idx = selection.get("selected_candidate_id", 1) - 1
        if selected_idx < 0 or selected_idx >= len(candidates):
            selected_idx = 0
        
        selected_candidate = candidates[selected_idx]
        
        result = {
            "original_product": {
                "name": parsed_data["product_name"],
                "ingredients": [ing["name"] for ing in parsed_data["ingredients"]],
                "non_plant_based_ingredients": [
                    ing["name"] for ing in parsed_data["ingredients"] 
                    if not ing["is_plant_based"]
                ]
            },
            "strategy": parsed_data["strategy"],
            "optimized_product": {
                "ingredients": [ing["name"] for ing in selected_candidate["new_ingredients"]],
                "replacements": selected_candidate["replacements"]
            },
            "metrics": {
                "shelf_life": {
                    "original_days": selected_candidate["scores"]["shelf_life"]["original_days"],
                    "new_days": selected_candidate["scores"]["shelf_life"]["new_days"],
                    "improvement_percent": selected_candidate["scores"]["shelf_life"]["improvement_percent"],
                    "score": selected_candidate["scores"]["shelf_life"]["score"]
                },
                "nutrition": {
                    "similarity_percent": selected_candidate["scores"]["nutrition"]["score"] * 100,
                    "original_profile": selected_candidate["scores"]["nutrition"]["original_profile"],
                    "new_profile": selected_candidate["scores"]["nutrition"]["new_profile"],
                    "score": selected_candidate["scores"]["nutrition"]["score"]
                },
                "carbon": {
                    "original_co2_kg": selected_candidate["scores"]["carbon"]["original_co2_kg"],
                    "new_co2_kg": selected_candidate["scores"]["carbon"]["new_co2_kg"],
                    "reduction_percent": selected_candidate["scores"]["carbon"]["reduction_percent"],
                    "score": selected_candidate["scores"]["carbon"]["score"]
                },
                "taste": {
                    "similarity": selected_candidate["scores"]["taste"]["similarity"],
                    "overall_score": selected_candidate["scores"]["taste"]["new_profile"]["overall_score"],
                    "score": selected_candidate["scores"]["taste"]["score"]
                },
                "cost": {
                    "original_cost_eur": selected_candidate["scores"]["cost"]["original_cost_eur"],
                    "new_cost_eur": selected_candidate["scores"]["cost"]["new_cost_eur"],
                    "cost_change_percent": selected_candidate["scores"]["cost"]["cost_change_percent"],
                    "cost_change_eur": selected_candidate["scores"]["cost"]["cost_change_eur"]
                },
                "total_score": selected_candidate["total_score"]
            },
            "justification": selection["justification"],
            "recommendations": selection["recommendations"],
            "confidence_score": selection["confidence_score"],
            "all_candidates": [
                {
                    "id": i + 1,
                    "replacements": c["replacements"],
                    "total_score": c["total_score"]
                }
                for i, c in enumerate(candidates)
            ]
        }
        
        print(f"✓ Candidat sélectionné: #{selected_idx + 1}")
        print(f"✓ Score total: {selected_candidate['total_score']:.3f}")
        print(f"✓ Confiance: {selection['confidence_score']:.1%}\n")
        
        self._print_summary(result)
        
        return result
    
    def _enrich_ingredients(self, ingredients: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrichit tous les ingrédients avec les données"""
        enriched = []
        
        for ing in ingredients:
            enriched_data = self.data_enrichment.enrich_ingredient(
                ing["name"], 
                ing.get("category", "unknown")
            )
            
            enriched.append({
                **ing,
                "enriched_data": enriched_data
            })
        
        return enriched
    
    def _generate_candidates(
        self, 
        parsed_data: Dict[str, Any], 
        enriched_original: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Génère et évalue les candidats selon la stratégie"""
        strategy = parsed_data["strategy"]
        candidates = []
        
        if strategy == "replace_all_additives":
            # Remplacer TOUS les conservateurs/additifs non plant-based
            candidates = self._generate_replace_all_additives_candidates(
                enriched_original, parsed_data
            )
        else:
            # Remplacer UN ingrédient non plant-based
            candidates = self._generate_replace_one_candidates(
                enriched_original, parsed_data
            )
        
        # Évaluer tous les candidats
        evaluated_candidates = []
        for candidate in candidates:
            scores = self._evaluate_candidate(enriched_original, candidate["new_ingredients"])
            total_score = self.calculator.calculate_total_score(scores)
            is_valid, violations = self.calculator.is_valid_candidate(scores)
            
            evaluated_candidates.append({
                **candidate,
                "scores": scores,
                "total_score": total_score,
                "is_valid": is_valid,
                "violations": violations
            })
        
        # Trier par score total (décroissant)
        evaluated_candidates.sort(key=lambda x: x["total_score"], reverse=True)
        
        # Retourner les N meilleurs candidats valides
        valid_candidates = [c for c in evaluated_candidates if c["is_valid"]]
        
        if not valid_candidates:
            print("⚠ Aucun candidat valide trouvé, retour des meilleurs candidats malgré violations")
            return evaluated_candidates[:config.NUM_CANDIDATES]
        
        return valid_candidates[:config.NUM_CANDIDATES]
    
    def _generate_replace_all_additives_candidates(
        self, 
        enriched_original: List[Dict[str, Any]],
        parsed_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des candidats en remplaçant TOUS les additifs non plant-based"""
        # Identifier les additifs non plant-based
        additives_to_replace = [
            ing for ing in enriched_original 
            if ing.get("is_preservative_or_additive", False) and not ing.get("is_plant_based", True)
        ]
        
        if not additives_to_replace:
            print("⚠ Aucun additif non plant-based trouvé, passage à stratégie alternative")
            return self._generate_replace_one_candidates(enriched_original, parsed_data)
        
        print(f"  → {len(additives_to_replace)} additifs à remplacer")
        for additive in additives_to_replace:
            print(f"     • {additive['name']}")
        
        # Générer des combinaisons de remplacement
        candidates = []
        
        # Pour chaque additif, obtenir des alternatives
        all_alternatives = {}
        for additive in additives_to_replace:
            alternatives = self.data_enrichment.get_plant_based_alternatives(
                additive["name"], 
                additive.get("category", "additive")
            )
            all_alternatives[additive["name"]] = alternatives[:3]  # Top 3 alternatives
            print(f"     • {additive['name']}: {len(alternatives)} alternatives trouvées")
        
        # Générer le candidat principal avec les meilleures alternatives pour TOUS les additifs
        new_ingredients = copy.deepcopy(enriched_original)  # COPIE PROFONDE!
        replacements = []
        
        for additive in additives_to_replace:
            alternatives = all_alternatives.get(additive["name"], [])
            if alternatives:
                best_alt = alternatives[0]  # Meilleure alternative
                
                # Remplacer dans la liste
                idx = next(i for i, ing in enumerate(new_ingredients) if ing["name"] == additive["name"])
                new_ingredients[idx] = {
                    "name": best_alt["name"],
                    "is_plant_based": True,
                    "category": additive.get("category", "additive"),
                    "enriched_data": best_alt["enriched_data"]
                }
                
                replacements.append({
                    "original": additive["name"],
                    "replacement": best_alt["name"],
                    "reason": "Remplacement d'additif non plant-based"
                })
        
        if replacements:
            candidates.append({
                "new_ingredients": new_ingredients,
                "replacements": replacements
            })
            print(f"  ✓ Candidat 1: {len(replacements)} remplacements")
        
        # Générer des variantes avec d'autres alternatives
        for i in range(min(3, config.NUM_CANDIDATES - 1)):
            variant_ingredients = copy.deepcopy(enriched_original)  # COPIE PROFONDE!
            variant_replacements = []
            
            for additive in additives_to_replace:
                alternatives = all_alternatives.get(additive["name"], [])
                if len(alternatives) > i + 1:
                    alt = alternatives[i + 1]
                else:
                    alt = alternatives[0] if alternatives else None
                
                if alt:
                    idx = next(j for j, ing in enumerate(variant_ingredients) if ing["name"] == additive["name"])
                    variant_ingredients[idx] = {
                        "name": alt["name"],
                        "is_plant_based": True,
                        "category": additive.get("category", "additive"),
                        "enriched_data": alt["enriched_data"]
                    }
                    
                    variant_replacements.append({
                        "original": additive["name"],
                        "replacement": alt["name"],
                        "reason": "Remplacement d'additif non plant-based (variante)"
                    })
            
            if variant_replacements:
                candidates.append({
                    "new_ingredients": variant_ingredients,
                    "replacements": variant_replacements
                })
                print(f"  ✓ Candidat {i+2}: {len(variant_replacements)} remplacements")
        
        return candidates
    
    def _generate_replace_one_candidates(
        self, 
        enriched_original: List[Dict[str, Any]],
        parsed_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des candidats en remplaçant UN ingrédient non plant-based"""
        # Identifier les ingrédients non plant-based (hors additifs déjà traités)
        non_plant_based = [
            ing for ing in enriched_original 
            if not ing.get("is_plant_based", True)
        ]
        
        if not non_plant_based:
            print("⚠ Aucun ingrédient non plant-based trouvé")
            return []
        
        print(f"  → {len(non_plant_based)} ingrédients non plant-based disponibles")
        
        candidates = []
        
        # Pour chaque ingrédient non plant-based, générer des candidats
        for ing_to_replace in non_plant_based:
            alternatives = self.data_enrichment.get_plant_based_alternatives(
                ing_to_replace["name"], 
                ing_to_replace.get("category", "unknown")
            )
            
            # Générer un candidat pour chaque alternative (top 3)
            for alt in alternatives[:3]:
                new_ingredients = copy.deepcopy(enriched_original)  # COPIE PROFONDE!
                
                # Remplacer l'ingrédient
                idx = next(i for i, ing in enumerate(new_ingredients) if ing["name"] == ing_to_replace["name"])
                new_ingredients[idx] = {
                    "name": alt["name"],
                    "is_plant_based": True,
                    "category": ing_to_replace.get("category", "unknown"),
                    "enriched_data": alt["enriched_data"]
                }
                
                candidates.append({
                    "new_ingredients": new_ingredients,
                    "replacements": [{
                        "original": ing_to_replace["name"],
                        "replacement": alt["name"],
                        "reason": f"Remplacement d'ingrédient non plant-based ({ing_to_replace.get('category', 'unknown')})"
                    }]
                })
                
                # Limiter le nombre de candidats
                if len(candidates) >= config.NUM_CANDIDATES * 2:
                    break
            
            if len(candidates) >= config.NUM_CANDIDATES * 2:
                break
        
        return candidates
    
    def _evaluate_candidate(
        self, 
        original_ingredients: List[Dict[str, Any]], 
        new_ingredients: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Évalue un candidat sur tous les critères"""
        scores = {
            "shelf_life": self.calculator.calculate_shelf_life_score(
                original_ingredients, new_ingredients
            ),
            "nutrition": self.calculator.calculate_nutrition_score(
                original_ingredients, new_ingredients
            ),
            "carbon": self.calculator.calculate_carbon_score(
                original_ingredients, new_ingredients
            ),
            "taste": self.calculator.calculate_taste_score(
                original_ingredients, new_ingredients
            ),
            "cost": self.calculator.calculate_cost_score(
                original_ingredients, new_ingredients
            )
        }
        
        return scores
    
    def _print_summary(self, result: Dict[str, Any]):
        """Affiche un résumé des résultats"""
        print(f"\n{'='*60}")
        print("📊 RÉSUMÉ DE L'OPTIMISATION")
        print(f"{'='*60}\n")
        
        print(f"Produit: {result['original_product']['name']}")
        print(f"Stratégie: {result['strategy']}\n")
        
        print("Remplacements effectués:")
        for repl in result['optimized_product']['replacements']:
            print(f"  • {repl['original']} → {repl['replacement']}")
        
        print(f"\nMétriques:")
        metrics = result['metrics']
        print(f"  • Durée de conservation: {metrics['shelf_life']['original_days']:.1f} → {metrics['shelf_life']['new_days']:.1f} jours ({metrics['shelf_life']['improvement_percent']:+.1f}%)")
        print(f"  • Similarité nutritionnelle: {metrics['nutrition']['similarity_percent']:.1f}%")
        print(f"  • Réduction carbone: {metrics['carbon']['reduction_percent']:.1f}%")
        print(f"  • Score gustatif: {metrics['taste']['overall_score']:.1f}/10")
        print(f"  • Score total: {metrics['total_score']:.3f}")
        
        print(f"\n{'='*60}\n")

"""
Data Enrichment - ÉTAPE 2
Enrichit les données des ingrédients avec:
- Données nutritionnelles (USDA)
- Empreinte carbone (Agribalyse)
- Données biologiques (pH, Aw)
- Alternatives plant-based
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import config
import os


class DataEnrichment:
    """Gestionnaire d'enrichissement des données"""
    
    def __init__(self):
        self.usda_data = None
        self.carbon_data = None
        self.alternatives_data = None
        self.taste_data = None
        self.shelf_life_data = None
        
        self._load_databases()
    
    def _load_databases(self):
        """Charge toutes les bases de données"""
        try:
            if os.path.exists(config.USDA_NUTRITION_PATH):
                self.usda_data = pd.read_csv(config.USDA_NUTRITION_PATH)
                print(f"✓ Base USDA chargée: {len(self.usda_data)} entrées")
            
            if os.path.exists(config.AGRIBALYSE_CARBON_PATH):
                self.carbon_data = pd.read_csv(config.AGRIBALYSE_CARBON_PATH)
                print(f"✓ Base Agribalyse chargée: {len(self.carbon_data)} entrées")
            
            if os.path.exists(config.PLANT_ALTERNATIVES_PATH):
                self.alternatives_data = pd.read_csv(config.PLANT_ALTERNATIVES_PATH)
                print(f"✓ Base alternatives chargée: {len(self.alternatives_data)} entrées")
            
            if os.path.exists(config.TASTE_PROFILES_PATH):
                self.taste_data = pd.read_csv(config.TASTE_PROFILES_PATH)
                print(f"✓ Base goût chargée: {len(self.taste_data)} entrées")
            
            if os.path.exists(config.SHELF_LIFE_PATH):
                self.shelf_life_data = pd.read_csv(config.SHELF_LIFE_PATH)
                print(f"✓ Base durée de conservation chargée: {len(self.shelf_life_data)} entrées")
                
        except Exception as e:
            print(f"⚠ Erreur lors du chargement des bases: {e}")
            print("Les bases de données seront créées avec des données par défaut")
    
    def enrich_ingredient(self, ingredient_name: str, category: str = "unknown") -> Dict[str, Any]:
        """
        Enrichit un ingrédient avec toutes les données disponibles
        
        Args:
            ingredient_name: Nom de l'ingrédient
            category: Catégorie de l'ingrédient
        
        Returns:
            Dict avec toutes les données enrichies
        """
        enriched = {
            "name": ingredient_name,
            "category": category,
            "nutrition": self._get_nutrition_data(ingredient_name),
            "carbon_footprint": self._get_carbon_data(ingredient_name),
            "biological": self._get_biological_data(ingredient_name),
            "taste_profile": self._get_taste_data(ingredient_name)
        }
        
        return enriched
    
    def _get_nutrition_data(self, ingredient_name: str) -> Dict[str, float]:
        """Récupère les données nutritionnelles (USDA)"""
        if self.usda_data is not None:
            # Recherche fuzzy dans la base USDA
            matches = self.usda_data[
                self.usda_data['name'].str.lower().str.contains(ingredient_name.lower(), na=False)
            ]
            
            if not matches.empty:
                row = matches.iloc[0]
                return {
                    "protein_g": float(row.get('protein_g', 0)),
                    "fat_g": float(row.get('fat_g', 0)),
                    "carbs_g": float(row.get('carbs_g', 0)),
                    "fiber_g": float(row.get('fiber_g', 0)),
                    "calories_kcal": float(row.get('calories_kcal', 0)),
                    "water_g": float(row.get('water_g', 0))
                }
        
        # Valeurs par défaut si non trouvé
        return self._get_default_nutrition(ingredient_name)
    
    def _get_default_nutrition(self, ingredient_name: str) -> Dict[str, float]:
        """Valeurs nutritionnelles par défaut basées sur des moyennes"""
        ing_lower = ingredient_name.lower()
        
        # Protéines
        if any(word in ing_lower for word in ["lait", "milk", "yaourt", "yogurt"]):
            return {"protein_g": 3.5, "fat_g": 3.5, "carbs_g": 5.0, "fiber_g": 0, "calories_kcal": 65, "water_g": 87}
        elif any(word in ing_lower for word in ["viande", "meat", "poulet", "chicken"]):
            return {"protein_g": 20.0, "fat_g": 5.0, "carbs_g": 0, "fiber_g": 0, "calories_kcal": 130, "water_g": 70}
        elif any(word in ing_lower for word in ["oeuf", "egg"]):
            return {"protein_g": 13.0, "fat_g": 11.0, "carbs_g": 1.0, "fiber_g": 0, "calories_kcal": 155, "water_g": 75}
        elif any(word in ing_lower for word in ["sucre", "sugar"]):
            return {"protein_g": 0, "fat_g": 0, "carbs_g": 100.0, "fiber_g": 0, "calories_kcal": 400, "water_g": 0}
        elif any(word in ing_lower for word in ["huile", "oil", "beurre", "butter"]):
            return {"protein_g": 0, "fat_g": 100.0, "carbs_g": 0, "fiber_g": 0, "calories_kcal": 900, "water_g": 0}
        else:
            return {"protein_g": 2.0, "fat_g": 1.0, "carbs_g": 10.0, "fiber_g": 2.0, "calories_kcal": 60, "water_g": 80}
    
    def _get_carbon_data(self, ingredient_name: str) -> Dict[str, float]:
        """Récupère l'empreinte carbone (Agribalyse)"""
        if self.carbon_data is not None:
            matches = self.carbon_data[
                self.carbon_data['name'].str.lower().str.contains(ingredient_name.lower(), na=False)
            ]
            
            if not matches.empty:
                row = matches.iloc[0]
                return {
                    "co2_kg_per_kg": float(row.get('co2_kg_per_kg', 0)),
                    "land_use_m2": float(row.get('land_use_m2', 0)),
                    "water_use_l": float(row.get('water_use_l', 0))
                }
        
        return self._get_default_carbon(ingredient_name)
    
    def _get_default_carbon(self, ingredient_name: str) -> Dict[str, float]:
        """Empreinte carbone par défaut (données Agribalyse moyennes)"""
        ing_lower = ingredient_name.lower()
        
        # Produits animaux (haute empreinte)
        if any(word in ing_lower for word in ["boeuf", "beef"]):
            return {"co2_kg_per_kg": 27.0, "land_use_m2": 326, "water_use_l": 15400}
        elif any(word in ing_lower for word in ["lait", "milk", "fromage", "cheese"]):
            return {"co2_kg_per_kg": 3.2, "land_use_m2": 9, "water_use_l": 1050}
        elif any(word in ing_lower for word in ["poulet", "chicken"]):
            return {"co2_kg_per_kg": 6.9, "land_use_m2": 7.2, "water_use_l": 4325}
        elif any(word in ing_lower for word in ["oeuf", "egg"]):
            return {"co2_kg_per_kg": 4.8, "land_use_m2": 5.7, "water_use_l": 3265}
        elif any(word in ing_lower for word in ["poisson", "fish"]):
            return {"co2_kg_per_kg": 5.1, "land_use_m2": 2.5, "water_use_l": 3000}
        
        # Produits végétaux (faible empreinte)
        elif any(word in ing_lower for word in ["soja", "soy", "tofu"]):
            return {"co2_kg_per_kg": 2.0, "land_use_m2": 3.5, "water_use_l": 2145}
        elif any(word in ing_lower for word in ["amande", "almond"]):
            return {"co2_kg_per_kg": 2.3, "land_use_m2": 2.2, "water_use_l": 16095}
        elif any(word in ing_lower for word in ["avoine", "oat"]):
            return {"co2_kg_per_kg": 0.9, "land_use_m2": 1.5, "water_use_l": 482}
        elif any(word in ing_lower for word in ["pois", "pea"]):
            return {"co2_kg_per_kg": 0.9, "land_use_m2": 1.8, "water_use_l": 397}
        else:
            return {"co2_kg_per_kg": 1.5, "land_use_m2": 2.0, "water_use_l": 500}
    
    def _get_biological_data(self, ingredient_name: str) -> Dict[str, float]:
        """Récupère les données biologiques (pH, Aw)"""
        if self.shelf_life_data is not None:
            matches = self.shelf_life_data[
                self.shelf_life_data['name'].str.lower().str.contains(ingredient_name.lower(), na=False)
            ]
            
            if not matches.empty:
                row = matches.iloc[0]
                return {
                    "ph": float(row.get('ph', 6.5)),
                    "water_activity": float(row.get('water_activity', 0.95)),
                    "antimicrobial_score": float(row.get('antimicrobial_score', 0))
                }
        
        return self._get_default_biological(ingredient_name)
    
    def _get_default_biological(self, ingredient_name: str) -> Dict[str, float]:
        """Données biologiques par défaut"""
        ing_lower = ingredient_name.lower()
        
        # Conservateurs naturels
        if any(word in ing_lower for word in ["vinaigre", "vinegar"]):
            return {"ph": 2.5, "water_activity": 0.95, "antimicrobial_score": 8}
        elif any(word in ing_lower for word in ["sel", "salt"]):
            return {"ph": 7.0, "water_activity": 0.75, "antimicrobial_score": 7}
        elif any(word in ing_lower for word in ["sucre", "sugar"]):
            return {"ph": 7.0, "water_activity": 0.85, "antimicrobial_score": 5}
        elif any(word in ing_lower for word in ["citron", "lemon", "acide citrique"]):
            return {"ph": 2.3, "water_activity": 0.95, "antimicrobial_score": 7}
        
        # Produits laitiers
        elif any(word in ing_lower for word in ["lait", "milk", "yaourt"]):
            return {"ph": 6.5, "water_activity": 0.98, "antimicrobial_score": 2}
        
        # Valeur neutre par défaut
        else:
            return {"ph": 6.5, "water_activity": 0.95, "antimicrobial_score": 3}
    
    def _get_taste_data(self, ingredient_name: str) -> Dict[str, Any]:
        """Récupère le profil gustatif"""
        if self.taste_data is not None:
            matches = self.taste_data[
                self.taste_data['name'].str.lower().str.contains(ingredient_name.lower(), na=False)
            ]
            
            if not matches.empty:
                row = matches.iloc[0]
                return {
                    "sweetness": float(row.get('sweetness', 5)),
                    "saltiness": float(row.get('saltiness', 5)),
                    "sourness": float(row.get('sourness', 5)),
                    "bitterness": float(row.get('bitterness', 5)),
                    "umami": float(row.get('umami', 5)),
                    "overall_score": float(row.get('overall_score', 7))
                }
        
        return self._get_default_taste(ingredient_name)
    
    def _get_default_taste(self, ingredient_name: str) -> Dict[str, Any]:
        """Profil gustatif par défaut (échelle 0-10)"""
        return {
            "sweetness": 5,
            "saltiness": 5,
            "sourness": 5,
            "bitterness": 5,
            "umami": 5,
            "overall_score": 7
        }
    
    def get_plant_based_alternatives(self, ingredient_name: str, category: str) -> List[Dict[str, Any]]:
        """
        Trouve des alternatives plant-based pour un ingrédient
        
        Args:
            ingredient_name: Nom de l'ingrédient à remplacer
            category: Catégorie de l'ingrédient
        
        Returns:
            Liste d'alternatives possibles avec leurs données enrichies
        """
        alternatives = []
        
        if self.alternatives_data is not None:
            # Recherche par ingrédient original
            matches = self.alternatives_data[
                self.alternatives_data['original_ingredient'].str.lower().str.contains(
                    ingredient_name.lower(), na=False
                )
            ]
            
            if not matches.empty:
                for _, row in matches.iterrows():
                    alt_name = row['plant_based_alternative']
                    alternatives.append({
                        "name": alt_name,
                        "original": ingredient_name,
                        "compatibility_score": float(row.get('compatibility_score', 0.8)),
                        "enriched_data": self.enrich_ingredient(alt_name, category)
                    })
                
                return alternatives
        
        # Alternatives par défaut basées sur des règles
        return self._get_default_alternatives(ingredient_name, category)
    
    def _get_default_alternatives(self, ingredient_name: str, category: str) -> List[Dict[str, Any]]:
        """Alternatives par défaut basées sur des règles"""
        ing_lower = ingredient_name.lower()
        alternatives = []
        
        # Produits laitiers
        if any(word in ing_lower for word in ["lait", "milk"]) and "coco" not in ing_lower:
            for alt in ["lait de soja", "lait d'avoine", "lait d'amande", "lait de coco"]:
                alternatives.append({
                    "name": alt,
                    "original": ingredient_name,
                    "compatibility_score": 0.85,
                    "enriched_data": self.enrich_ingredient(alt, "protein")
                })
        
        # Œufs
        elif any(word in ing_lower for word in ["oeuf", "egg"]):
            for alt in ["graines de lin moulues", "aquafaba", "compote de pommes", "tofu soyeux"]:
                alternatives.append({
                    "name": alt,
                    "original": ingredient_name,
                    "compatibility_score": 0.75,
                    "enriched_data": self.enrich_ingredient(alt, "protein")
                })
        
        # Gélatine
        elif "gélatine" in ing_lower or "gelatin" in ing_lower:
            for alt in ["agar-agar", "pectine", "carraghénane", "gomme de guar"]:
                alternatives.append({
                    "name": alt,
                    "original": ingredient_name,
                    "compatibility_score": 0.90,
                    "enriched_data": self.enrich_ingredient(alt, "thickener")
                })
        
        # Beurre
        elif any(word in ing_lower for word in ["beurre", "butter"]):
            for alt in ["huile de coco", "margarine végétale", "purée d'amande", "huile d'olive"]:
                alternatives.append({
                    "name": alt,
                    "original": ingredient_name,
                    "compatibility_score": 0.80,
                    "enriched_data": self.enrich_ingredient(alt, "fat")
                })
        
        # Miel
        elif any(word in ing_lower for word in ["miel", "honey"]):
            for alt in ["sirop d'agave", "sirop d'érable", "sirop de dattes"]:
                alternatives.append({
                    "name": alt,
                    "original": ingredient_name,
                    "compatibility_score": 0.85,
                    "enriched_data": self.enrich_ingredient(alt, "sweetener")
                })
        
        # Viande
        elif any(word in ing_lower for word in ["viande", "meat", "poulet", "chicken"]):
            for alt in ["tofu", "tempeh", "seitan", "protéines de soja texturées"]:
                alternatives.append({
                    "name": alt,
                    "original": ingredient_name,
                    "compatibility_score": 0.70,
                    "enriched_data": self.enrich_ingredient(alt, "protein")
                })
        
        return alternatives

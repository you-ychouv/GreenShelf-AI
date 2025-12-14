"""
API Module avec Cache - Version Optimisée
Améliore les performances en mettant en cache les résultats
"""

from typing import Dict, List, Any, Optional
from api import EnterpriseOptimizer
import hashlib
import json
import time


class CachedEnterpriseOptimizer(EnterpriseOptimizer):
    """
    Version optimisée de EnterpriseOptimizer avec cache
    
    Améliore les performances:
    - Résultats en cache: instantané (au lieu de 30-60s)
    - Statistiques de performance
    - Logs de temps détaillés
    """
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        self._cache = {}
        self._stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "total_time_saved": 0.0
        }
    
    def optimize_product(
        self, 
        name: str, 
        ingredients: str,
        return_format: str = "detailed",
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Optimise un produit avec cache
        
        Args:
            name: Nom du produit
            ingredients: Liste des ingrédients
            return_format: Format de retour
            use_cache: Utiliser le cache (True par défaut)
        
        Returns:
            Résultat de l'optimisation (depuis cache ou calcul)
        """
        self._stats["total_requests"] += 1
        
        # Créer une clé de cache unique
        cache_key = self._create_cache_key(name, ingredients, return_format)
        
        # Vérifier le cache si activé
        if use_cache and cache_key in self._cache:
            self._stats["cache_hits"] += 1
            self._stats["total_time_saved"] += 45.0  # Temps moyen économisé
            
            print(f"✅ Résultat trouvé en cache (instantané)")
            print(f"📊 Cache: {self._stats['cache_hits']}/{self._stats['total_requests']} hits")
            print(f"⏱️  Temps économisé: {self._stats['total_time_saved']:.0f}s au total\n")
            
            return self._cache[cache_key]
        
        # Pas en cache, optimiser normalement
        self._stats["cache_misses"] += 1
        
        print(f"🔄 Optimisation en cours (30-60s)...")
        print(f"📊 Cache: {self._stats['cache_hits']}/{self._stats['total_requests']} hits\n")
        
        start_time = time.time()
        
        # Appeler la méthode parent
        result = super().optimize_product(name, ingredients, return_format)
        
        duration = time.time() - start_time
        print(f"\n⏱️  Optimisation terminée en {duration:.1f}s")
        
        # Sauvegarder en cache
        if use_cache:
            self._cache[cache_key] = result
            print(f"💾 Résultat mis en cache")
        
        return result
    
    def optimize_batch(
        self, 
        products: List[Dict[str, str]],
        return_format: str = "detailed",
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Optimise plusieurs produits avec cache
        
        Bénéficie du cache pour les produits déjà optimisés
        """
        print(f"\n🔄 Optimisation de {len(products)} produits...")
        print(f"📊 État du cache: {len(self._cache)} produits en mémoire\n")
        
        results = []
        cached_count = 0
        
        for i, product in enumerate(products):
            print(f"{'='*60}")
            print(f"Produit {i+1}/{len(products)}: {product.get('name', 'Sans nom')}")
            print(f"{'='*60}\n")
            
            try:
                # Vérifier si en cache
                cache_key = self._create_cache_key(
                    product["name"], 
                    product["ingredients"], 
                    return_format
                )
                
                if use_cache and cache_key in self._cache:
                    cached_count += 1
                
                result = self.optimize_product(
                    name=product["name"],
                    ingredients=product["ingredients"],
                    return_format=return_format,
                    use_cache=use_cache
                )
                
                results.append({
                    "success": True,
                    "product_index": i,
                    "product_name": product["name"],
                    "result": result,
                    "from_cache": cache_key in self._cache
                })
                
            except Exception as e:
                results.append({
                    "success": False,
                    "product_index": i,
                    "product_name": product.get("name", "Inconnu"),
                    "error": str(e)
                })
        
        print(f"\n{'='*60}")
        print(f"📊 RÉSUMÉ BATCH")
        print(f"{'='*60}")
        print(f"Total: {len(products)} produits")
        print(f"Depuis cache: {cached_count} produits (instantané)")
        print(f"Optimisés: {len(products) - cached_count} produits")
        print(f"Temps économisé: ~{cached_count * 45}s")
        print(f"{'='*60}\n")
        
        return results
    
    def _create_cache_key(self, name: str, ingredients: str, return_format: str) -> str:
        """Crée une clé de cache unique"""
        data = f"{name.lower().strip()}:{ingredients.lower().strip()}:{return_format}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du cache"""
        hit_rate = 0.0
        if self._stats["total_requests"] > 0:
            hit_rate = (self._stats["cache_hits"] / self._stats["total_requests"]) * 100
        
        return {
            "total_requests": self._stats["total_requests"],
            "cache_hits": self._stats["cache_hits"],
            "cache_misses": self._stats["cache_misses"],
            "hit_rate_percent": hit_rate,
            "cached_products": len(self._cache),
            "total_time_saved_seconds": self._stats["total_time_saved"]
        }
    
    def clear_cache(self):
        """Vide le cache"""
        self._cache.clear()
        print("🗑️  Cache vidé")
    
    def get_cached_products(self) -> List[str]:
        """Retourne la liste des produits en cache"""
        return [
            f"Product {i+1}" 
            for i in range(len(self._cache))
        ]


# Fonction utilitaire pour utilisation directe
def optimize_with_cache(name: str, ingredients: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Fonction utilitaire pour optimiser avec cache
    
    Args:
        name: Nom du produit
        ingredients: Liste des ingrédients
        api_key: Clé API (optionnel)
    
    Returns:
        Résultat de l'optimisation
    """
    optimizer = CachedEnterpriseOptimizer(api_key)
    return optimizer.optimize_product(name, ingredients)

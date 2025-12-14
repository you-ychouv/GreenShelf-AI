"""
API REST - Interface web pour l'optimisation plant-based
Utilise FastAPI pour une intégration facile dans des applications web
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
import uvicorn
from api import EnterpriseOptimizer
import traceback
import numpy as np
import json


# Convertisseur JSON personnalisé pour gérer les types numpy
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)


def convert_numpy_types(obj):
    """Convertit récursivement les types numpy en types Python natifs"""
    if isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    return obj


# ============================================================================
# MODÈLES DE DONNÉES (Pydantic)
# ============================================================================

class ProductInput(BaseModel):
    """Modèle pour un produit à optimiser"""
    name: str = Field(..., min_length=1, max_length=200, description="Nom du produit")
    ingredients: str = Field(..., min_length=1, description="Liste des ingrédients séparés par des virgules")
    
    @validator('name')
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Le nom du produit ne peut pas être vide")
        return v.strip()
    
    @validator('ingredients')
    def ingredients_not_empty(cls, v):
        if not v.strip():
            raise ValueError("La liste des ingrédients ne peut pas être vide")
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Yaourt aux fruits",
                "ingredients": "lait entier, sucre, fraises, gélatine, arômes naturels, colorant E120"
            }
        }


class BatchProductInput(BaseModel):
    """Modèle pour optimisation en lot"""
    products: List[ProductInput] = Field(..., min_items=1, max_items=50, description="Liste de produits à optimiser")
    return_format: Optional[str] = Field("simple", description="Format de retour: 'simple' ou 'detailed'")
    
    class Config:
        schema_extra = {
            "example": {
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
        }


class OptimizationResponse(BaseModel):
    """Modèle de réponse pour une optimisation"""
    success: bool
    product_name: str
    strategy: Optional[str] = None
    replacements: Optional[List[Dict[str, Any]]] = None
    scores: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    recommendations: Optional[List[str]] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Modèle de réponse pour le health check"""
    status: str
    version: str
    message: str


class ValidationResponse(BaseModel):
    """Modèle de réponse pour la validation"""
    valid: bool
    issues: List[str]
    warnings: List[str]
    ingredient_count: int


# ============================================================================
# INITIALISATION DE L'API
# ============================================================================

app = FastAPI(
    title="Plant-Based Optimizer API",
    description="API REST pour l'optimisation de produits alimentaires vers des alternatives plant-based",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS pour permettre les appels depuis une web app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instance globale de l'optimiseur
optimizer = None


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialise l'optimiseur au démarrage de l'API"""
    global optimizer
    try:
        optimizer = EnterpriseOptimizer()
        print("✅ Optimiseur initialisé avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        # L'API démarre quand même, les endpoints retourneront une erreur


@app.get("/", response_model=HealthResponse)
async def root():
    """
    Endpoint racine - Informations sur l'API
    """
    return {
        "status": "online",
        "version": "1.0.0",
        "message": "Plant-Based Optimizer API - Utilisez /docs pour la documentation"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check - Vérifie que l'API fonctionne correctement
    """
    if optimizer is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="L'optimiseur n'est pas initialisé"
        )
    
    return {
        "status": "healthy",
        "version": "1.0.0",
        "message": "API opérationnelle"
    }


@app.post("/optimize", response_model=OptimizationResponse, status_code=status.HTTP_200_OK)
async def optimize_product(product: ProductInput, return_format: str = "simple"):
    """
    Optimise un seul produit
    
    - **name**: Nom du produit
    - **ingredients**: Liste des ingrédients séparés par des virgules
    - **return_format**: Format de retour ('simple' ou 'detailed')
    
    Retourne les recommandations d'optimisation avec les métriques
    """
    if optimizer is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="L'optimiseur n'est pas disponible"
        )
    
    try:
        # Optimiser le produit
        result = optimizer.optimize_product(
            name=product.name,
            ingredients=product.ingredients,
            return_format=return_format
        )
        
        # Convertir les types numpy en types Python natifs AVANT de formater
        result = convert_numpy_types(result)
        
        # Formater la réponse selon le format
        if return_format == "simple":
            response = {
                "success": True,
                "product_name": result.get("product_name", "Produit"),
                "strategy": result.get("strategy", "unknown"),
                "replacements": result.get("replacements", []),
                "scores": result.get("scores", {}),
                "summary": result.get("summary", ""),
                "recommendations": result.get("top_recommendations", [])
            }
        else:
            # Format détaillé - accès sécurisé
            original_product = result.get("original_product", {})
            optimized_product = result.get("optimized_product", {})
            justification = result.get("justification", {})
            
            response = {
                "success": True,
                "product_name": original_product.get("name", "Produit"),
                "strategy": result.get("strategy", "unknown"),
                "replacements": optimized_product.get("replacements", []),
                "scores": result.get("metrics", {}),
                "summary": justification.get("summary", ""),
                "recommendations": result.get("recommendations", [])
            }
        
        # Convertir à nouveau pour être sûr (au cas où il reste des numpy)
        response = convert_numpy_types(response)
        
        return response
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Erreur lors de l'optimisation: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'optimisation: {str(e)}"
        )


@app.post("/optimize/batch", status_code=status.HTTP_200_OK)
async def optimize_batch(batch_input: BatchProductInput):
    """
    Optimise plusieurs produits en lot
    
    - **products**: Liste de produits à optimiser
    - **return_format**: Format de retour ('simple' ou 'detailed')
    
    Retourne une liste de résultats (succès et erreurs)
    """
    if optimizer is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="L'optimiseur n'est pas disponible"
        )
    
    try:
        # Convertir les produits Pydantic en dicts
        products_list = [
            {"name": p.name, "ingredients": p.ingredients}
            for p in batch_input.products
        ]
        
        # Optimiser en lot
        results = optimizer.optimize_batch(
            products=products_list,
            return_format=batch_input.return_format or "simple"
        )
        
        # Convertir les types numpy en types Python natifs
        results = convert_numpy_types(results)
        
        return {
            "success": True,
            "total_products": len(batch_input.products),
            "successful": len([r for r in results if r.get("success", False)]),
            "failed": len([r for r in results if not r.get("success", False)]),
            "results": results
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Erreur lors de l'optimisation en lot: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'optimisation en lot: {str(e)}"
        )


@app.post("/validate", response_model=ValidationResponse)
async def validate_product(product: ProductInput):
    """
    Valide un produit sans l'optimiser
    
    - **name**: Nom du produit
    - **ingredients**: Liste des ingrédients
    
    Retourne le statut de validation avec les problèmes détectés
    """
    if optimizer is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="L'optimiseur n'est pas disponible"
        )
    
    try:
        validation = optimizer.validate_product(
            name=product.name,
            ingredients=product.ingredients
        )
        
        # Convertir les types numpy en types Python natifs
        validation = convert_numpy_types(validation)
        
        return validation
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la validation: {str(e)}"
        )


# ============================================================================
# LANCEMENT DE L'API
# ============================================================================

def start_api(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """
    Démarre l'API REST
    
    Args:
        host: Adresse d'écoute (0.0.0.0 pour toutes les interfaces)
        port: Port d'écoute
        reload: Rechargement automatique en développement
    """
    print("\n" + "="*70)
    print("🌱 PLANT-BASED OPTIMIZER API")
    print("="*70)
    print(f"\n🚀 Démarrage de l'API sur http://{host}:{port}")
    print(f"📚 Documentation: http://{host}:{port}/docs")
    print(f"📖 ReDoc: http://{host}:{port}/redoc")
    print("\n" + "="*70 + "\n")
    
    uvicorn.run(
        "api_rest:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


if __name__ == "__main__":
    # Lancement en mode développement avec port fixe
    import sys
    import os
    
    # Forcer le port 8000
    os.environ['PORT'] = '8000'
    
    print("\n⚠️  IMPORTANT: L'API démarre TOUJOURS sur le port 8000")
    print("   Si le port est occupé, fermez l'autre processus avec:")
    print("   Windows: taskkill /F /IM python.exe")
    print("   Ou changez le port dans cette ligne et dans webapp/app.js\n")
    
    start_api(host="127.0.0.1", port=8000, reload=True)

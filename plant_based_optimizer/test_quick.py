"""
Test rapide du système sans API
Utilise le parsing de secours basé sur des règles
"""

from optimizer import PlantBasedOptimizer
import json


def test_without_api():
    """Test sans clé API - utilise le parsing de secours"""
    print("\n" + "="*70)
    print("🧪 TEST RAPIDE - Sans API (Parsing de secours)")
    print("="*70 + "\n")
    
    # Initialiser sans API
    optimizer = PlantBasedOptimizer(api_key="test_mode")
    
    # Produit de test simple
    product = {
        "name": "Yaourt aux fruits",
        "ingredients": "lait entier, sucre, fraises, gélatine, arômes naturels"
    }
    
    print(f"📦 Produit: {product['name']}")
    print(f"📝 Ingrédients: {product['ingredients']}\n")
    
    try:
        # Optimiser
        result = optimizer.optimize(product)
        
        # Vérifier le résultat
        print("\n✅ TEST RÉUSSI!")
        print(f"\n📊 Résumé:")
        print(f"   • Stratégie: {result['strategy']}")
        print(f"   • Remplacements: {len(result['optimized_product']['replacements'])}")
        print(f"   • Score total: {result['metrics']['total_score']:.3f}")
        
        # Sauvegarder
        with open("test_result.json", 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Résultat sauvegardé dans: test_result.json")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST ÉCHOUÉ: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multiple_products():
    """Test avec plusieurs produits"""
    print("\n" + "="*70)
    print("🧪 TEST MULTIPLE PRODUITS")
    print("="*70 + "\n")
    
    products = [
        {
            "name": "Yaourt nature",
            "ingredients": "lait, ferments lactiques, gélatine"
        },
        {
            "name": "Crème dessert",
            "ingredients": "lait, crème fraîche, sucre, gélatine"
        },
        {
            "name": "Gâteau",
            "ingredients": "farine, sucre, œufs, beurre"
        }
    ]
    
    optimizer = PlantBasedOptimizer(api_key="test_mode")
    
    results = []
    for i, product in enumerate(products, 1):
        print(f"\n{'='*70}")
        print(f"Test {i}/{len(products)}: {product['name']}")
        print(f"{'='*70}")
        
        try:
            result = optimizer.optimize(product)
            results.append({
                "product": product['name'],
                "success": True,
                "score": result['metrics']['total_score']
            })
            print(f"✅ Score: {result['metrics']['total_score']:.3f}")
        except Exception as e:
            results.append({
                "product": product['name'],
                "success": False,
                "error": str(e)
            })
            print(f"❌ Erreur: {e}")
    
    # Résumé
    print(f"\n{'='*70}")
    print("📊 RÉSUMÉ DES TESTS")
    print(f"{'='*70}")
    
    success_count = sum(1 for r in results if r['success'])
    print(f"\nRéussis: {success_count}/{len(results)}")
    
    for r in results:
        status = "✅" if r['success'] else "❌"
        score_str = f"(Score: {r['score']:.3f})" if r['success'] else f"(Erreur: {r.get('error', 'Unknown')})"
        print(f"{status} {r['product']} {score_str}")
    
    return success_count == len(results)


if __name__ == "__main__":
    print("\n🌱 PLANT-BASED OPTIMIZER - Tests Rapides\n")
    
    # Test 1: Simple
    test1_ok = test_without_api()
    
    # Test 2: Multiple
    test2_ok = test_multiple_products()
    
    # Résultat final
    print("\n" + "="*70)
    if test1_ok and test2_ok:
        print("✅ TOUS LES TESTS RÉUSSIS!")
    else:
        print("⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
    print("="*70 + "\n")

"""
Script de test pour l'API REST
Teste les différents endpoints et fonctionnalités
"""

import requests
import json
import time


API_URL = "http://localhost:8000"


def print_section(title):
    """Affiche un titre de section"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def test_health():
    """Test du health check"""
    print_section("TEST 1: Health Check")
    
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {data['status']}")
            print(f"✅ Version: {data['version']}")
            print(f"✅ Message: {data['message']}")
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        print("💡 Assurez-vous que l'API est démarrée: python api_rest.py")
        return False


def test_validate():
    """Test de la validation"""
    print_section("TEST 2: Validation de Produit")
    
    product = {
        "name": "Yaourt aux fruits",
        "ingredients": "lait entier, sucre, fraises, gélatine"
    }
    
    print(f"Produit: {product['name']}")
    print(f"Ingrédients: {product['ingredients']}\n")
    
    try:
        response = requests.post(
            f"{API_URL}/validate",
            json=product
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Validation: {'Valide' if data['valid'] else 'Invalide'}")
            print(f"✅ Nombre d'ingrédients: {data['ingredient_count']}")
            
            if data['issues']:
                print(f"⚠️  Problèmes: {', '.join(data['issues'])}")
            
            if data['warnings']:
                print(f"⚠️  Avertissements: {', '.join(data['warnings'])}")
            
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_optimize_simple():
    """Test d'optimisation simple"""
    print_section("TEST 3: Optimisation Simple")
    
    product = {
        "name": "Yaourt aux fruits",
        "ingredients": "lait entier, sucre, fraises, gélatine, arômes naturels, colorant E120"
    }
    
    print(f"Produit: {product['name']}")
    print(f"Ingrédients: {product['ingredients']}\n")
    print("⏳ Optimisation en cours (cela peut prendre 30-60 secondes)...\n")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{API_URL}/optimize",
            params={"return_format": "simple"},
            json=product,
            timeout=120  # 2 minutes timeout
        )
        
        duration = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Optimisation réussie en {duration:.1f}s\n")
            print(f"Stratégie: {data['strategy']}")
            
            print(f"\nRemplacements ({len(data['replacements'])}):")
            for repl in data['replacements']:
                print(f"  • {repl['original']} → {repl['replacement']}")
            
            print(f"\nScores:")
            scores = data['scores']
            print(f"  • Conservation: {scores['shelf_life_improvement']:+.1f}%")
            print(f"  • Nutrition: {scores['nutrition_similarity']:.1f}%")
            print(f"  • Carbone: {scores['carbon_reduction']:.1f}%")
            print(f"  • Goût: {scores['taste_score']:.1f}/10")
            print(f"  • Score total: {scores['total_score']:.3f}")
            
            print(f"\nRésumé:")
            print(f"  {data['summary']}")
            
            print(f"\nRecommandations:")
            for i, rec in enumerate(data['top_recommendations'], 1):
                print(f"  {i}. {rec}")
            
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"Détails: {response.text}")
            return False
    except requests.Timeout:
        print(f"❌ Timeout après {time.time() - start_time:.1f}s")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_optimize_batch():
    """Test d'optimisation en lot"""
    print_section("TEST 4: Optimisation en Lot")
    
    products = [
        {
            "name": "Yaourt nature",
            "ingredients": "lait entier, ferments lactiques, gélatine"
        },
        {
            "name": "Crème dessert",
            "ingredients": "lait, sucre, crème fraîche, amidon"
        }
    ]
    
    print(f"Nombre de produits: {len(products)}")
    for i, p in enumerate(products, 1):
        print(f"  {i}. {p['name']}")
    
    print("\n⏳ Optimisation en cours...\n")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{API_URL}/optimize/batch",
            json={
                "products": products,
                "return_format": "simple"
            },
            timeout=240  # 4 minutes timeout
        )
        
        duration = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Optimisation réussie en {duration:.1f}s\n")
            print(f"Total: {data['total_products']}")
            print(f"Succès: {data['successful']}")
            print(f"Échecs: {data['failed']}")
            
            print("\nRésultats:")
            for result in data['results']:
                if result['success']:
                    print(f"\n  ✅ {result['product_name']}")
                    print(f"     Score: {result['result']['scores']['total_score']:.3f}")
                    print(f"     Remplacements: {len(result['result']['replacements'])}")
                else:
                    print(f"\n  ❌ {result['product_name']}")
                    print(f"     Erreur: {result['error']}")
            
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"Détails: {response.text}")
            return False
    except requests.Timeout:
        print(f"❌ Timeout après {time.time() - start_time:.1f}s")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_error_handling():
    """Test de la gestion d'erreurs"""
    print_section("TEST 5: Gestion d'Erreurs")
    
    # Test 1: Produit vide
    print("Test 5.1: Produit avec nom vide")
    try:
        response = requests.post(
            f"{API_URL}/optimize",
            json={"name": "", "ingredients": "lait, sucre"}
        )
        if response.status_code == 400:
            print("✅ Erreur 400 correctement retournée")
        else:
            print(f"⚠️  Code inattendu: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test 2: Ingrédients vides
    print("\nTest 5.2: Produit avec ingrédients vides")
    try:
        response = requests.post(
            f"{API_URL}/optimize",
            json={"name": "Test", "ingredients": ""}
        )
        if response.status_code == 400:
            print("✅ Erreur 400 correctement retournée")
        else:
            print(f"⚠️  Code inattendu: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test 3: Format invalide
    print("\nTest 5.3: Format JSON invalide")
    try:
        response = requests.post(
            f"{API_URL}/optimize",
            json={"invalid": "format"}
        )
        if response.status_code == 422:  # Validation error
            print("✅ Erreur 422 correctement retournée")
        else:
            print(f"⚠️  Code inattendu: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    return True


def main():
    """Exécute tous les tests"""
    print("\n" + "="*70)
    print("  🧪 TESTS DE L'API PLANT-BASED OPTIMIZER")
    print("="*70)
    
    results = {
        "Health Check": test_health(),
        "Validation": test_validate(),
        "Optimisation Simple": test_optimize_simple(),
        "Optimisation Batch": test_optimize_batch(),
        "Gestion d'Erreurs": test_error_handling()
    }
    
    # Résumé
    print_section("RÉSUMÉ DES TESTS")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{'='*70}")
    print(f"  Résultat: {passed}/{total} tests réussis")
    print(f"{'='*70}\n")
    
    if passed == total:
        print("🎉 Tous les tests sont passés!")
    else:
        print("⚠️  Certains tests ont échoué")


if __name__ == "__main__":
    main()

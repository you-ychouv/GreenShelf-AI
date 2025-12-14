"""
Point d'entrée principal du Plant-Based Optimizer
"""

import json
import sys
from optimizer import PlantBasedOptimizer
import config


def main():
    """Fonction principale"""
    print("\n" + "="*70)
    print("🌱 PLANT-BASED OPTIMIZER - Hackathon IA Agroalimentaire")
    print("="*70 + "\n")
    
    # Initialiser l'optimiseur
    try:
        optimizer = PlantBasedOptimizer()
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        return
    
    # Exemple de produit à optimiser
    product = {
        "name": "Yaourt aux fruits",
        "ingredients": "lait entier, sucre, fraises, gélatine, arômes naturels, colorant E120"
    }
    
    print("📦 PRODUIT À OPTIMISER:")
    print(f"   Nom: {product['name']}")
    print(f"   Ingrédients: {product['ingredients']}\n")
    
    # Lancer l'optimisation
    try:
        result = optimizer.optimize(product)
        
        # Sauvegarder le résultat
        output_file = "result_optimization.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Résultat sauvegardé dans: {output_file}")
        
        # Afficher le résumé
        print("\n" + "="*70)
        print("📊 RÉSULTAT FINAL")
        print("="*70)
        print(f"\n🎯 Stratégie: {result['strategy']}")
        print(f"\n📝 Remplacements:")
        for repl in result['optimized_product']['replacements']:
            print(f"   • {repl['original']} → {repl['replacement']}")
        
        print(f"\n📈 Métriques:")
        metrics = result['metrics']
        print(f"   • Durée de conservation: {metrics['shelf_life']['improvement_percent']:+.1f}%")
        print(f"   • Similarité nutritionnelle: {metrics['nutrition']['similarity_percent']:.1f}%")
        print(f"   • Réduction carbone: {metrics['carbon']['reduction_percent']:.1f}%")
        print(f"   • Score gustatif: {metrics['taste']['overall_score']:.1f}/10")
        print(f"   • Score total: {metrics['total_score']:.3f}")
        
        print(f"\n💡 Justification:")
        print(f"   {result['justification']['summary']}")
        
        print(f"\n🔬 Recommandations:")
        for i, rec in enumerate(result['recommendations'], 1):
            print(f"   {i}. {rec}")
        
        print("\n" + "="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'optimisation: {e}")
        import traceback
        traceback.print_exc()


def optimize_custom_product():
    """Optimiser un produit personnalisé"""
    print("\n" + "="*70)
    print("🌱 OPTIMISATION PERSONNALISÉE")
    print("="*70 + "\n")
    
    # Demander les informations du produit
    name = input("Nom du produit: ")
    ingredients = input("Liste des ingrédients (séparés par des virgules): ")
    
    product = {
        "name": name,
        "ingredients": ingredients
    }
    
    # Initialiser et optimiser
    optimizer = PlantBasedOptimizer()
    result = optimizer.optimize(product)
    
    # Sauvegarder
    output_file = f"result_{name.replace(' ', '_').lower()}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Résultat sauvegardé dans: {output_file}\n")


def batch_optimize():
    """Optimiser plusieurs produits depuis un fichier JSON"""
    print("\n" + "="*70)
    print("🌱 OPTIMISATION PAR LOT")
    print("="*70 + "\n")
    
    input_file = input("Fichier JSON d'entrée (ex: products.json): ")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            products = json.load(f)
        
        optimizer = PlantBasedOptimizer()
        results = []
        
        for i, product in enumerate(products, 1):
            print(f"\n{'='*70}")
            print(f"Produit {i}/{len(products)}: {product.get('name', 'Sans nom')}")
            print(f"{'='*70}\n")
            
            result = optimizer.optimize(product)
            results.append(result)
        
        # Sauvegarder tous les résultats
        output_file = "results_batch.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Tous les résultats sauvegardés dans: {output_file}\n")
        
    except FileNotFoundError:
        print(f"❌ Fichier {input_file} non trouvé")
    except json.JSONDecodeError:
        print(f"❌ Erreur de format JSON dans {input_file}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == "custom":
            optimize_custom_product()
        elif mode == "batch":
            batch_optimize()
        else:
            print(f"Mode inconnu: {mode}")
            print("Modes disponibles: custom, batch")
    else:
        # Mode par défaut: exemple
        main()

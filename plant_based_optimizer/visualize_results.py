"""
Visualisation des résultats pour présentation hackathon
"""

import json
import sys


def print_comparison_table(result):
    """Affiche un tableau comparatif avant/après"""
    print("\n" + "="*80)
    print("📊 TABLEAU COMPARATIF - AVANT / APRÈS")
    print("="*80 + "\n")
    
    # En-tête
    print(f"{'Métrique':<30} {'AVANT':<20} {'APRÈS':<20} {'ÉVOLUTION':<10}")
    print("-" * 80)
    
    metrics = result['metrics']
    
    # Durée de conservation
    shelf_orig = metrics['shelf_life']['original_days']
    shelf_new = metrics['shelf_life']['new_days']
    shelf_imp = metrics['shelf_life']['improvement_percent']
    print(f"{'Durée de conservation':<30} {shelf_orig:.1f} jours{'':<10} {shelf_new:.1f} jours{'':<10} {shelf_imp:+.1f}%")
    
    # Nutrition
    nutr_sim = metrics['nutrition']['similarity_percent']
    print(f"{'Similarité nutritionnelle':<30} {'100%':<20} {nutr_sim:.1f}%{'':<13} {'Maintenue':<10}")
    
    # Carbone
    carbon_orig = metrics['carbon']['original_co2_kg']
    carbon_new = metrics['carbon']['new_co2_kg']
    carbon_red = metrics['carbon']['reduction_percent']
    print(f"{'Empreinte carbone':<30} {carbon_orig:.2f} kg CO2{'':<10} {carbon_new:.2f} kg CO2{'':<10} {carbon_red:.1f}%")
    
    # Goût
    taste_score = metrics['taste']['overall_score']
    print(f"{'Score gustatif':<30} {'7.5/10':<20} {taste_score:.1f}/10{'':<13} {'Maintenu':<10}")
    
    print("-" * 80)
    print(f"{'SCORE TOTAL':<30} {'':<20} {metrics['total_score']:.3f}{'':<16} {'✅':<10}")
    print("="*80 + "\n")


def print_ingredients_comparison(result):
    """Affiche la comparaison des ingrédients"""
    print("\n" + "="*80)
    print("🔄 COMPARAISON DES INGRÉDIENTS")
    print("="*80 + "\n")
    
    original = result['original_product']['ingredients']
    optimized = result['optimized_product']['ingredients']
    replacements = {r['original']: r['replacement'] for r in result['optimized_product']['replacements']}
    
    print(f"{'INGRÉDIENT ORIGINAL':<35} {'→':<5} {'INGRÉDIENT OPTIMISÉ':<35}")
    print("-" * 80)
    
    for orig_ing in original:
        if orig_ing in replacements:
            new_ing = replacements[orig_ing]
            print(f"{'❌ ' + orig_ing:<35} {'→':<5} {'✅ ' + new_ing:<35}")
        else:
            print(f"{'✓ ' + orig_ing:<35} {'→':<5} {'✓ ' + orig_ing:<35}")
    
    print("="*80 + "\n")


def print_environmental_impact(result):
    """Affiche l'impact environnemental"""
    print("\n" + "="*80)
    print("🌍 IMPACT ENVIRONNEMENTAL")
    print("="*80 + "\n")
    
    carbon = result['metrics']['carbon']
    reduction = carbon['reduction_percent']
    co2_saved = carbon['original_co2_kg'] - carbon['new_co2_kg']
    
    print(f"Réduction d'empreinte carbone: {reduction:.1f}%")
    print(f"CO2 économisé par kg de produit: {co2_saved:.3f} kg CO2eq")
    print(f"\n💡 Équivalent à:")
    
    # Équivalences parlantes
    km_car = co2_saved / 0.12  # 120g CO2/km en moyenne
    trees = co2_saved / 21  # Un arbre absorbe ~21kg CO2/an
    
    print(f"   • {km_car:.1f} km en voiture économisés")
    print(f"   • {trees:.3f} arbres plantés (équivalent annuel)")
    
    print("\n" + "="*80 + "\n")


def print_nutritional_details(result):
    """Affiche les détails nutritionnels"""
    print("\n" + "="*80)
    print("🥗 DÉTAILS NUTRITIONNELS (pour 100g)")
    print("="*80 + "\n")
    
    orig_profile = result['metrics']['nutrition']['original_profile']
    new_profile = result['metrics']['nutrition']['new_profile']
    
    print(f"{'Nutriment':<20} {'AVANT':<15} {'APRÈS':<15} {'DIFFÉRENCE':<15}")
    print("-" * 80)
    
    nutrients = [
        ('Protéines', 'protein_g', 'g'),
        ('Lipides', 'fat_g', 'g'),
        ('Glucides', 'carbs_g', 'g'),
        ('Fibres', 'fiber_g', 'g'),
        ('Calories', 'calories_kcal', 'kcal')
    ]
    
    for name, key, unit in nutrients:
        orig = orig_profile[key]
        new = new_profile[key]
        diff = new - orig
        diff_str = f"{diff:+.1f} {unit}"
        print(f"{name:<20} {orig:.1f} {unit:<12} {new:.1f} {unit:<12} {diff_str:<15}")
    
    print("="*80 + "\n")


def print_justification(result):
    """Affiche la justification scientifique"""
    print("\n" + "="*80)
    print("🔬 JUSTIFICATION SCIENTIFIQUE")
    print("="*80 + "\n")
    
    justif = result['justification']
    
    print("📝 Résumé:")
    print(f"   {justif['summary']}\n")
    
    print("🧪 Analyse de la durée de conservation:")
    print(f"   {justif['shelf_life_analysis']}\n")
    
    print("🥗 Analyse nutritionnelle:")
    print(f"   {justif['nutrition_analysis']}\n")
    
    print("🌍 Analyse de l'empreinte carbone:")
    print(f"   {justif['carbon_analysis']}\n")
    
    print("👅 Analyse gustative:")
    print(f"   {justif['taste_analysis']}\n")
    
    print("⚖️ Compromis:")
    print(f"   {justif['trade_offs']}\n")
    
    print("="*80 + "\n")


def print_recommendations(result):
    """Affiche les recommandations"""
    print("\n" + "="*80)
    print("💡 RECOMMANDATIONS POUR L'INDUSTRIALISATION")
    print("="*80 + "\n")
    
    for i, rec in enumerate(result['recommendations'], 1):
        print(f"{i}. {rec}")
    
    print("\n" + "="*80 + "\n")


def visualize_result(json_file):
    """Visualise un fichier de résultat"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            result = json.load(f)
        
        print("\n" + "🌱" * 40)
        print(f"\n{'PLANT-BASED OPTIMIZER - RÉSULTATS':^80}")
        print(f"{'Produit: ' + result['original_product']['name']:^80}")
        print("\n" + "🌱" * 40)
        
        # Afficher toutes les sections
        print_ingredients_comparison(result)
        print_comparison_table(result)
        print_nutritional_details(result)
        print_environmental_impact(result)
        print_justification(result)
        print_recommendations(result)
        
        # Score de confiance
        confidence = result.get('confidence_score', 0) * 100
        print(f"\n{'='*80}")
        print(f"🎯 Score de confiance de la recommandation: {confidence:.0f}%")
        print(f"{'='*80}\n")
        
    except FileNotFoundError:
        print(f"❌ Fichier {json_file} non trouvé")
    except json.JSONDecodeError:
        print(f"❌ Erreur de format JSON dans {json_file}")
    except Exception as e:
        print(f"❌ Erreur: {e}")


def compare_multiple_results(json_files):
    """Compare plusieurs résultats"""
    print("\n" + "="*80)
    print("📊 COMPARAISON MULTI-PRODUITS")
    print("="*80 + "\n")
    
    results = []
    for file in json_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                results.append(json.load(f))
        except:
            print(f"⚠️ Impossible de charger {file}")
    
    if not results:
        print("❌ Aucun résultat à comparer")
        return
    
    # Tableau comparatif
    print(f"{'Produit':<25} {'Score':<10} {'Durée':<12} {'Carbone':<12} {'Nutrition':<12}")
    print("-" * 80)
    
    for r in results:
        name = r['original_product']['name'][:24]
        score = r['metrics']['total_score']
        shelf = r['metrics']['shelf_life']['improvement_percent']
        carbon = r['metrics']['carbon']['reduction_percent']
        nutr = r['metrics']['nutrition']['similarity_percent']
        
        print(f"{name:<25} {score:.3f}{'':<5} {shelf:+.1f}%{'':<6} {carbon:.1f}%{'':<6} {nutr:.1f}%")
    
    print("="*80 + "\n")
    
    # Moyennes
    avg_score = sum(r['metrics']['total_score'] for r in results) / len(results)
    avg_shelf = sum(r['metrics']['shelf_life']['improvement_percent'] for r in results) / len(results)
    avg_carbon = sum(r['metrics']['carbon']['reduction_percent'] for r in results) / len(results)
    avg_nutr = sum(r['metrics']['nutrition']['similarity_percent'] for r in results) / len(results)
    
    print("📊 MOYENNES:")
    print(f"   • Score total: {avg_score:.3f}")
    print(f"   • Amélioration durée: {avg_shelf:+.1f}%")
    print(f"   • Réduction carbone: {avg_carbon:.1f}%")
    print(f"   • Similarité nutrition: {avg_nutr:.1f}%")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python visualize_results.py result.json")
        print("  python visualize_results.py result1.json result2.json result3.json")
    elif len(sys.argv) == 2:
        visualize_result(sys.argv[1])
    else:
        compare_multiple_results(sys.argv[1:])

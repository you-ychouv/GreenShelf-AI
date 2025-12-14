# 🌱 Guide Final - Plant-Based Optimizer

## ⚠️ IMPORTANT: Format des Ingrédients

**Les ingrédients DOIVENT être séparés par des virgules (,)**

### ✅ Format Correct:
```
lait entier, sucre, fraises, gélatine, arômes naturels, colorant E120
```

### ❌ Format Incorrect:
```
lait entier; sucre; fraises  (point-virgule)
lait entier - sucre - fraises  (tiret)
lait entier / sucre / fraises  (slash)
```

---

## 📋 Liste Complète des Additifs Non Plant-Based Détectés

Le système détecte automatiquement ces additifs d'origine animale:

### E-Numbers d'Origine Animale:

| Code | Nom | Origine |
|------|-----|---------|
| **E120** | Cochenille, Carmin, Acide carminique | Insecte (cochenille) |
| **E441** | Gélatine | Os et peau d'animaux |
| **E542** | Phosphate d'os | Os d'animaux |
| **E901** | Cire d'abeille | Abeilles |
| **E904** | Gomme-laque, Shellac | Insecte (cochenille) |
| **E910** | Esters de cire | Cire d'abeille |
| **E913** | Lanoline | Laine de mouton |
| **E920** | L-cystéine | Plumes, cheveux, poils |
| **E921** | L-cystine | Plumes, cheveux, poils |
| **E322** | Lécithine | Peut être animale (œuf) |
| **E422** | Glycérol, Glycérine | Peut être animale |
| **E471-E483** | Mono/diglycérides | Peuvent être animaux |
| **E1105** | Lysozyme | Protéine d'œuf |

### Variantes Détectées:

Le système reconnaît toutes ces variantes:
- `E120`, `e120`, `E 120`, `e 120`, `E-120`, `e-120`
- `colorant E120`, `colorant e120`, `Colorant E120`
- `cochenille`, `carmin`, `carmines`, `carmine`
- `gélatine`, `gelatine`, `gelatin`
- etc.

---

## 🚀 Utilisation du Système

### Étape 1: Démarrer l'API

```bash
# Ouvrir un terminal
cd Desktop\plant_based_optimizer

# Supprimer le cache (IMPORTANT!)
del /s /q __pycache__

# Lancer l'API
python api_rest.py
```

**Vous devez voir:**
```
⚠️  IMPORTANT: L'API démarre TOUJOURS sur le port 8000
======================================================================
🌱 PLANT-BASED OPTIMIZER API
======================================================================
🚀 Démarrage de l'API sur http://127.0.0.1:8000
✅ Optimiseur initialisé avec succès
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Étape 2: Ouvrir la WebApp

Double-cliquez sur:
```
C:\Users\Fatou SY\Desktop\plant_based_optimizer\webapp\index.html
```

### Étape 3: Utiliser l'Optimiseur

1. **Entrez le nom du produit**
   ```
   Exemple: Yaourt aux fruits
   ```

2. **Entrez les ingrédients (SÉPARÉS PAR DES VIRGULES!)**
   ```
   Exemple: lait entier, sucre, fraises, gélatine, arômes naturels, colorant E120
   ```

3. **Cliquez sur "Optimiser"**

4. **Attendez 10-30 secondes**

---

## ✅ Résultats Attendus

### Pour "Yaourt aux fruits" avec gélatine et colorant E120:

**Dans le Terminal:**
```
📋 ÉTAPE 1: Parsing et Classification des Ingrédients
------------------------------------------------------------
  🔍 DEBUG: Additif animal détecté: 'gélatine' contient 'gélatine'
  🔍 DEBUG: Additif animal détecté: 'colorant E120' contient 'e120'
✓ Produit: Yaourt aux fruits
✓ Stratégie: replace_all_additives
✓ Ingrédients non plant-based: 3
✓ Conservateurs/additifs non plant-based: 2

🔬 ÉTAPE 3: Génération et Évaluation des Candidats
------------------------------------------------------------
  → 2 additifs à remplacer
     • gélatine
     • colorant E120
  ✓ Candidat 1: 2 remplacements
  ✓ Candidat 2: 2 remplacements
  ✓ Candidat 3: 2 remplacements
```

**Dans la WebApp:**
```
Stratégie: Remplacement de tous les additifs non plant-based

Remplacements (2):
• gélatine → agar-agar (ou pectine)
• colorant E120 → extrait de betterave

Scores:
• Conservation: +XX%
• Nutrition: XX%
• Carbone: -XX%
• Goût: X.X/10
```

---

## 🔧 Dépannage

### Problème: Je ne vois qu'1 seul remplacement au lieu de 2

**Solutions:**

1. **Supprimer le cache Python**
   ```bash
   cd Desktop\plant_based_optimizer
   del /s /q __pycache__
   rmdir /s /q __pycache__
   ```

2. **Vérifier le format des ingrédients**
   - ✅ Correct: `gélatine, colorant E120`
   - ❌ Incorrect: `gélatine; colorant E120`

3. **Rafraîchir le navigateur**
   ```
   Ctrl + Shift + R
   ```

4. **Relancer l'API**
   ```bash
   # Arrêter l'API
   Ctrl + C
   
   # Relancer
   python api_rest.py
   ```

### Problème: L'API ne démarre pas sur le port 8000

**Solution:**
```bash
# Tuer tous les processus Python
taskkill /F /IM python.exe

# Relancer
python api_rest.py
```

### Problème: La webapp affiche "API: ✗ Hors ligne"

**Vérifications:**
1. L'API est-elle lancée? (vérifier le terminal)
2. Le port est-il 8000? (vérifier dans le terminal)
3. Rafraîchir la page: `Ctrl + Shift + R`

---

## 📊 Exemples de Produits

### Exemple 1: Yaourt aux fruits
```
Nom: Yaourt aux fruits
Ingrédients: lait entier, sucre, fraises, gélatine, arômes naturels, colorant E120
Résultat: 2 remplacements (gélatine + E120)
```

### Exemple 2: Crème dessert
```
Nom: Crème dessert chocolat
Ingrédients: lait demi-écrémé, sucre, chocolat, crème fraîche, amidon de maïs, gélatine
Résultat: 1 remplacement (gélatine)
```

### Exemple 3: Gâteau
```
Nom: Gâteau marbré
Ingrédients: farine de blé, sucre, œufs, beurre, lait, levure, cacao, arôme vanille
Résultat: 1 remplacement (œufs OU beurre OU lait - stratégie replace_one)
```

### Exemple 4: Bonbons
```
Nom: Bonbons gélifiés
Ingrédients: sirop de glucose, sucre, gélatine, acide citrique, arômes, colorant E120
Résultat: 2 remplacements (gélatine + E120)
```

---

## 🎯 Stratégies de Remplacement

Le système utilise 2 stratégies:

### Stratégie 1: replace_all_additives
**Quand:** Le produit contient des additifs/conservateurs non plant-based
**Action:** Remplace TOUS les additifs non plant-based en même temps
**Exemple:** Yaourt avec gélatine + E120 → Les 2 sont remplacés

### Stratégie 2: replace_one_ingredient
**Quand:** Le produit contient des ingrédients non plant-based mais PAS d'additifs
**Action:** Remplace UN SEUL ingrédient (celui qui optimise le mieux la conservation)
**Exemple:** Gâteau avec œufs + beurre + lait → Un seul est remplacé

---

## 📝 Notes Importantes

1. **Format des ingrédients:** TOUJOURS séparer par des virgules
2. **Majuscules/minuscules:** Pas d'importance (E120 = e120 = E 120)
3. **Espaces:** Pas d'importance (E120 = E 120 = E-120)
4. **Cache:** Toujours supprimer `__pycache__` après modification
5. **Port:** L'API utilise TOUJOURS le port 8000

---

## 🆘 Support

Si vous rencontrez des problèmes:

1. Vérifiez le terminal pour les messages d'erreur
2. Vérifiez que les ingrédients sont séparés par des virgules
3. Supprimez le cache Python
4. Relancez l'API
5. Rafraîchissez le navigateur (Ctrl + Shift + R)

---

## ✅ Checklist Avant Utilisation

- [ ] API lancée (`python api_rest.py`)
- [ ] Terminal affiche "Uvicorn running on http://127.0.0.1:8000"
- [ ] WebApp ouverte (`webapp/index.html`)
- [ ] WebApp affiche "API Status: ✓ En ligne"
- [ ] Ingrédients séparés par des virgules
- [ ] Cache Python supprimé si modifications récentes

---

**Le système est prêt! 🌱✅**

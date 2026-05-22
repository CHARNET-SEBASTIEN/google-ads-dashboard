# 🎨 Refonte complète RAFO - Version 3.0

## ✨ Tout a été repris !

Design professionnel inspiré de RAFO avec attention aux moindres détails.

---

## 🎯 Ce qui a été refait

### 1. **Mode sombre complet** 🌙

**Couleurs exactes de RAFO** :
- Fond : `#0a0a0a` (noir profond)
- Sidebar : `#141414` (gris très foncé)
- Cards : `#1a1a1a` (gris foncé)
- Bordures : `#2a2a2a` (subtiles)
- Texte : `#ffffff` (blanc pur)
- Texte secondaire : `#a0a0a0` (gris)
- Accent : `#f59e0b` (orange/ambre)

### 2. **Sidebar redesignée** 📂

**Style RAFO** :
- Fond gris foncé `#141414`
- Logo Google Ads épuré (48px)
- Titre en gras, letterspacing négatif
- Label "NAVIGATION" en section

**Boutons de navigation** :
- Transparent par défaut
- Bordure gauche orange au hover (3px)
- translateX(2px) au hover
- Espacement réduit (0.125rem)
- Icônes + texte alignés
- Font-weight 500

**Statut connecté** :
- Card verte avec transparence
- Bordure verte subtile
- Style moderne

### 3. **Topbar moderne** 🎚️

**Position fixée** :
- Top : 1rem
- Right : 1.5rem
- Z-index : 1000

**Sélecteur de langue** :
- Fond card `#1a1a1a`
- Bordure `#2a2a2a`
- Border-radius : 0.5rem
- Padding réduit

**Toggle mode** :
- Carré 2.5rem × 2.5rem
- Fond card
- Bordure hover orange
- Icon centré

### 4. **Headers refaits** 📝

**H1** :
- 2rem, font-weight 700
- Letterspacing -0.02em
- Bordure bottom orange (2px)
- Margin-bottom 1.5rem

**H2, H3** :
- Tailles proportionnelles
- Marges optimisées
- Font-weight 700

### 5. **Cards & Métriques** 📊

**Style RAFO complet** :
- Fond `#1a1a1a`
- Bordure `#2a2a2a`
- Border-radius 0.75rem
- Padding 1.5rem
- Shadow subtile
- Hover : bordure orange + translateY(-2px)

**Métriques** :
- Label : 0.75rem, UPPERCASE, letterspacing
- Valeur : 2.25rem, font-weight 700
- Couleur secondaire pour labels
- Blanc pour valeurs

### 6. **Boutons refaits** 🔘

**Primary** :
- Fond orange `#f59e0b`
- Texte noir
- Font-weight 600
- Hover : orange clair + shadow + translateY

**Secondary** :
- Fond card
- Bordure subtile
- Hover : bordure orange

**Tous** :
- Border-radius 0.5rem
- Padding 0.625rem 1.5rem
- Font-size 0.875rem
- Transition 0.15s

### 7. **Tabs redesignés** 📑

**Container** :
- Fond sidebar `#141414`
- Bordure card
- Padding 0.5rem
- Gap 0.5rem

**Tab inactive** :
- Transparent
- Texte gris
- Hover : fond card

**Tab active** :
- Fond orange `#f59e0b`
- Texte noir
- Font-weight 600

### 8. **Tables améliorés** 📋

**Header** :
- Fond sidebar
- Texte uppercase, 0.75rem
- Letterspacing 0.05em
- Font-weight 600
- Padding 1rem

**Rows** :
- Fond card
- Bordure bottom subtile
- Hover : fond sidebar
- Padding 0.875rem 1rem
- Font-size 0.875rem

### 9. **Inputs modernisés** ⌨️

**Tous les inputs** :
- Fond card `#1a1a1a`
- Bordure `#2a2a2a`
- Border-radius 0.5rem
- Padding 0.625rem 0.875rem

**Focus** :
- Bordure orange
- Shadow orange (0.1 opacity)
- Outline none

**Placeholder** :
- Couleur grise secondaire

### 10. **Messages refaits** 💬

**Success** :
- Fond vert transparent (0.1)
- Bordure gauche verte (4px)
- Texte vert `#10b981`

**Warning** :
- Fond orange transparent
- Bordure gauche orange
- Texte orange

**Error** :
- Fond rouge transparent
- Bordure gauche rouge
- Texte rouge `#ef4444`

**Info** :
- Fond bleu transparent
- Bordure gauche bleue
- Texte bleu `#3b82f6`

### 11. **Graphiques Plotly** 📈

**Nouveau fichier** : `utils/plotly_theme.py`

**Thème dark** :
- paper_bgcolor : `#1a1a1a`
- plot_bgcolor : `#1a1a1a`
- Grille : `#2a2a2a`
- Texte : blanc
- Palette de 8 couleurs (orange, bleu, vert, rouge...)

**Fonction** : `apply_rafo_theme(fig, dark_mode=True)`

**Hover** :
- Fond `#141414`
- Bordure orange
- Mode "x unified"

### 12. **Scrollbar custom** 🎚️

- Width : 8px
- Track : fond sidebar
- Thumb : couleur bordure
- Hover : orange

### 13. **Progress bar** ⏳

- Fond : sidebar
- Barre : orange

### 14. **Dividers** ➖

- Couleur : bordure
- Opacity : 1 (pas de transparence)
- Margin : 2rem 0

### 15. **Links** 🔗

- Couleur : orange
- No decoration
- Font-weight 500
- Hover : orange clair + underline

### 16. **File uploader** 📤

- Fond card
- Bordure dashed
- Padding 2rem
- Hover : bordure orange + fond sidebar

### 17. **Captions & Small** 📝

- Couleur : texte secondaire
- Font-size : 0.75rem

### 18. **Responsive** 📱

**Mobile (< 768px)** :
- Padding réduit : 1rem
- H1 : 1.5rem
- Métriques : 1.75rem

---

## 📁 Fichiers créés/modifiés

### Nouveaux fichiers

1. **`/assets/rafo-complete.css`** (15kb)
   - CSS complet RAFO
   - Tous les composants
   - Mode sombre uniquement

2. **`/utils/plotly_theme.py`**
   - Thème Plotly dark/light
   - Fonction `apply_rafo_theme()`
   - Palette de couleurs

3. **`/REFONTE_RAFO.md`**
   - Ce document

### Fichiers modifiés

1. **`/utils/ui_helpers.py`**
   - Charge `rafo-complete.css` au lieu de `custom-dark-rafo.css`

---

## 🎨 Palette de couleurs complète

```css
--rafo-bg: #0a0a0a           /* Fond principal */
--rafo-sidebar: #141414      /* Sidebar */
--rafo-card: #1a1a1a         /* Cards */
--rafo-border: #2a2a2a       /* Bordures */
--rafo-text: #ffffff         /* Texte principal */
--rafo-text-secondary: #a0a0a0  /* Texte secondaire */
--rafo-accent: #f59e0b       /* Orange/Amber */
--rafo-accent-hover: #fbbf24 /* Orange clair */
--rafo-blue: #3b82f6         /* Bleu info */
--rafo-green: #10b981        /* Vert success */
--rafo-red: #ef4444          /* Rouge erreur */
```

---

## 🚀 Utilisation

### Mode sombre automatique

Le CSS RAFO complet s'applique automatiquement quand :
```python
user_prefs.is_dark_mode() == True
```

### Graphiques Plotly

Pour utiliser le thème RAFO sur vos graphiques :

```python
import plotly.graph_objects as go
from utils.plotly_theme import apply_rafo_theme
from utils.preferences import user_prefs

# Créer le graphique
fig = go.Figure(data=[...])

# Appliquer le thème
fig = apply_rafo_theme(fig, dark_mode=user_prefs.is_dark_mode())

# Afficher
st.plotly_chart(fig)
```

---

## 📊 Comparaison versions

| Élément | V2.0 | V3.0 RAFO |
|---------|------|-----------|
| **Fond** | Noir basique | Noir profond #0a0a0a |
| **Sidebar** | Grise | Grise foncée #141414 |
| **Cards** | Basiques | Hover + shadow |
| **Buttons** | Simples | Animations + shadow |
| **Tabs** | Standard | Style RAFO complet |
| **Tables** | Classiques | Headers uppercase |
| **Inputs** | Basiques | Focus orange |
| **Messages** | Simples | Bordure gauche 4px |
| **Graphiques** | Défaut | Thème custom |
| **Scrollbar** | Défaut | Custom orange |

---

## ✅ Pages à tester

Toutes les pages ont le nouveau design :

1. **Accueil** - Cards métriques
2. **Configuration** - Forms et inputs
3. **Vue d'ensemble** - Tableaux
4. **Détail campagne** - Tabs + graphiques
5. **Termes recherche** - Grand tableau
6. **Diagnostic** - Messages colorés

---

## 🎯 Résultat final

Un dashboard **professionnel** avec :
- ✅ Design RAFO complet
- ✅ Mode sombre élégant
- ✅ Animations fluides
- ✅ Hover effects partout
- ✅ Graphiques adaptés
- ✅ Responsive mobile
- ✅ Tous les composants stylisés
- ✅ Cohérence visuelle totale

---

## 🔧 Test avec Playwright

Pour tester :
```bash
node playwright-test.js
```

Captures dans `screenshots/` :
- `app-home-dark.png` - Mode sombre RAFO complet

---

**Version** : 3.0  
**Date** : 22/05/2026  
**Statut** : 🎨 Refonte RAFO complète  
**Design** : Inspiré de rafo-chapters.com

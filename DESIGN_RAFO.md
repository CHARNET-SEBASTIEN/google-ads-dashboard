# 🎨 Design RAFO - Version 2.5

## ✨ Nouveau design inspiré de RAFO

Votre dashboard dispose maintenant de **deux modes** complets :

### 🌞 Mode Clair Moderne
- Fond gris très clair (#fbfbfb)
- Cards blanches avec ombres subtiles
- Texte noir doux pour meilleure lisibilité
- Accents orange/ambre (#f39c12)
- Design épuré et professionnel

### 🌙 Mode Sombre RAFO
- **Fond noir profond** (#0a0a0a) - comme RAFO
- **Sidebar gris foncé** (#141414)
- **Cards gris foncé** (#1a1a1a) avec bordures subtiles
- Texte blanc pur pour contraste maximum
- **Accent orange/ambre** (#f39c12) - signature RAFO
- Design élégant et moderne

---

## 🎯 Éléments clés du design RAFO

### 1. Palette de couleurs

**Mode Sombre** :
```css
Background: #0a0a0a (noir profond)
Sidebar: #141414 (gris très foncé)
Cards: #1a1a1a (gris foncé)
Texte: #fafafa (blanc)
Accent: #f39c12 (orange/ambre)
Bordures: #2d2d2d (gris subtil)
```

**Mode Clair** :
```css
Background: #fbfbfb (gris très clair)
Sidebar: #fcfcfc (blanc cassé)
Cards: #ffffff (blanc pur)
Texte: #1a1a1a (noir doux)
Accent: #f39c12 (orange/ambre)
Bordures: #e6e6e6 (gris clair)
```

### 2. Typographie

- **Font principale** : Roboto (corps de texte)
- **Font titres** : Manjari (headings)
- **Font-weight** : 400-700
- **Hiérarchie claire** : Grands chiffres dans les métriques

### 3. Composants stylisés

#### Métriques (Cards)
- **Padding généreux** : 1.5rem
- **Bordures** : 1px solid (subtiles)
- **Border-radius** : 0.75rem
- **Labels** : UPPERCASE, letterspacing, gris 60%
- **Valeurs** : 2rem, font-weight 700, blanc/noir selon mode
- **Shadow** : Douce en clair, prononcée en sombre

#### Boutons
- **Style** : Moderne avec transitions
- **Hover** : translateY(-1px) + shadow
- **Primary** : Accent orange/ambre
- **Secondary** : Fond card avec bordure
- **Border-radius** : 0.5rem

#### Sidebar Navigation
- **Items** : Transparent avec bordure gauche au hover
- **Bordure accent** : 3px solid orange au hover
- **Animation** : translateX(2px)
- **Padding** : 0.875rem 1rem
- **Espacement** : 0.25rem entre items

#### Tables
- **Header** : Fond sidebar-bg, texte blanc/noir
- **Rows** : Alternance subtile
- **Hover** : Fond muted
- **Bordures** : 1px entre les lignes

#### Tabs
- **Container** : Fond sidebar-bg avec padding
- **Tab active** : Accent orange, font-weight 600
- **Tab hover** : Fond card-bg
- **Border-radius** : 0.5rem

---

## 📁 Fichiers créés

### CSS
1. **`/assets/custom.css`** (Mode Clair)
   - Variables CSS modernes
   - Tous les composants stylisés
   - Palette claire

2. **`/assets/custom-dark-rafo.css`** (Mode Sombre RAFO)
   - Fond noir profond
   - Sidebar grise foncée
   - Toutes les composants adaptés
   - Style RAFO complet

### Components
- **`/components/topbar.py`** - Barre de contrôles en haut à droite
- **`/components/sidebar.py`** - Navigation latérale améliorée

### Utilities
- **`/utils/preferences.py`** - Système de persistance

---

## 🚀 Comment ça marche

### Chargement du CSS

1. **Au démarrage** de chaque page :
   ```python
   load_custom_css()  # Charge custom.css (mode clair)
   ```

2. **Si mode sombre activé** :
   ```python
   # Charge EN PLUS custom-dark-rafo.css
   # Qui override les variables CSS
   ```

3. **Résultat** :
   - Mode clair : Seulement `custom.css`
   - Mode sombre : `custom.css` + `custom-dark-rafo.css`

### Persistance

Les préférences sont sauvegardées automatiquement :
```json
{
  "language": "fr",
  "dark_mode": true,
  "last_campaign_id": null
}
```

Fichier : `.user_preferences.json`

---

## 🎨 Comparaison visuelle

### Sidebar

**RAFO** :
```
┌────────────────────┐
│  [Logo RAFO]       │
│                    │
│  Search company... │
│                    │
├────────────────────┤
│  📊 Tableau        │ ← Accent orange si actif
│  🔍 Identification │
│  📋 Activités      │
│  📰 Actualités     │
│  👥 Gestion users  │ ← Actif
└────────────────────┘
```

**Notre Dashboard** :
```
┌────────────────────┐
│  [Logo Google Ads] │
│                    │
│   Google Ads       │
│    Dashboard       │
│                    │
│  ✅ Connecté       │
├────────────────────┤
│   NAVIGATION       │
│                    │
│  🏠  Accueil       │
│  ⚙️  Configuration │
│  📊  Vue ensemble  │
│  🎯  Détail        │
│  🔍  Recherche     │
│  ⚕️  Diagnostic    │
├────────────────────┤
│  ▼ 💾 Cache        │
└────────────────────┘
```

### Cards Métriques

**Style RAFO** (nos cards maintenant) :
```
┌─────────────────────────┐
│ IMPRESSIONS             │  ← Label uppercase gris
│                         │
│ 25,718                  │  ← Valeur grande et bold
│                         │
└─────────────────────────┘
  ↑ Fond sombre + bordure
```

### Boutons

**Avant** :
```
[ Bouton normal ]
```

**Maintenant** :
```
[ Bouton RAFO ]  ← Hover: bordure orange + translateY
```

---

## 🎯 Différences avec RAFO original

### ✅ Similitudes

- Fond noir profond
- Sidebar grise foncée
- Cards avec bordures subtiles
- Accent orange/ambre
- Grands chiffres dans métriques
- Navigation avec bordure au hover
- Typographie claire et moderne

### 🔄 Adaptations

| Élément | RAFO | Notre Dashboard |
|---------|------|----------------|
| **Logo** | RAFO 🇹🇷 | Google Ads (SVG) |
| **Barre recherche** | En haut | Pas encore (TODO) |
| **Métriques** | 4 cards horizontales | Flexibles selon page |
| **Heatmap** | Grille colorée | Tableaux classiques |
| **Sidebar width** | ~250px | ~280px (Streamlit) |
| **Topbar** | Icônes à droite | Langue + Mode à droite |

---

## 📊 Métriques de design

### Espacements
- **Padding cards** : 1.5rem
- **Gap entre éléments** : 0.75rem - 1rem
- **Margin sections** : 2rem
- **Padding sidebar items** : 0.875rem 1rem

### Border-radius
- **Cards** : 0.75rem
- **Boutons** : 0.5rem
- **Inputs** : 0.5rem
- **Tabs** : 0.5rem

### Transitions
- **Durée** : 0.2s
- **Easing** : ease
- **Transform** : translateY(-1px) ou translateX(2px)

### Shadows

**Mode Clair** :
```css
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
```

**Mode Sombre** :
```css
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
```

---

## 🔧 Personnalisation

### Changer l'accent

Éditez `/assets/custom-dark-rafo.css` :
```css
--accent: 45 100% 51%;  /* Orange/Amber */
```

Options :
- Rouge : `0 84% 60%`
- Bleu : `220 80% 55%`
- Vert : `142 76% 45%`
- Violet : `247 54% 50%`

### Ajuster le fond sombre

```css
--background: 0 0% 4%;  /* Plus clair : augmenter % */
```

### Modifier la sidebar

```css
--sidebar-bg: 0 0% 8%;  /* Plus clair : augmenter % */
```

---

## 🚀 Test et utilisation

### Tester les deux modes

1. **Ouvrir** : http://localhost:8501
2. **En haut à droite** : Cliquer sur 🌙 (mode sombre) ou ☀️ (mode clair)
3. **Observer** : Tous les composants changent instantanément

### Comparer avec RAFO

**RAFO** : Fond noir profond avec sidebar grise  
**Nous** : Pareil ! + Navigation améliorée + Métriques stylées

### Pages à tester

- ✅ Accueil - Cards avec métriques
- ✅ Vue d'ensemble - Tableau de campagnes
- ✅ Détail campagne - Onglets + Graphiques
- ✅ Termes recherche - Tableau complet
- ✅ Configuration - Forms et inputs

---

## 📋 TODO / Améliorations futures

### Court terme
- [ ] Ajouter barre de recherche en haut (comme RAFO)
- [ ] Améliorer les graphiques Plotly en mode sombre
- [ ] Ajouter animations de transition plus fluides
- [ ] Optimiser les performances du toggle

### Moyen terme
- [ ] Créer des micro-animations
- [ ] Ajouter plus d'icônes personnalisées
- [ ] Améliorer le responsive design
- [ ] Créer des tooltips stylisés

### Long terme
- [ ] Thème personnalisable par l'utilisateur
- [ ] Plus d'options d'accent colors
- [ ] Mode "auto" (suit le système)
- [ ] Animations de page transitions

---

## 🎉 Résultat

Vous avez maintenant un dashboard Google Ads avec :

✅ **Deux modes** (clair + sombre RAFO)  
✅ **Design moderne** inspiré de RAFO  
✅ **Persistance** des préférences  
✅ **Navigation améliorée** avec topbar  
✅ **Composants stylisés** (cards, buttons, tables)  
✅ **Sidebar professionnelle** avec logo Google Ads  
✅ **Transitions fluides** entre les modes  

**Profitez de votre nouveau design ! 🚀**

---

**Version** : 2.5  
**Date** : 22/05/2026  
**Inspiré de** : RAFO - rafo-chapters.com  
**Status** : ✅ Déployé

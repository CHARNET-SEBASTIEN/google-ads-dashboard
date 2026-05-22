# 🎨 Dashboard Google Ads - Version 2.0

## ✨ Nouvelles fonctionnalités

### 1. 🌍 Multilingue (FR/EN/DE)

L'application supporte maintenant **3 langues** :
- 🇫🇷 **Français** (par défaut)
- 🇬🇧 **Anglais**
- 🇩🇪 **Allemand**

**Comment changer de langue ?**
- Dans la sidebar → Section "Paramètres" → Sélecteur de langue

**Traduction complète** :
- Navigation
- Labels et métriques
- Messages d'erreur
- Boutons et actions
- Dates et périodes

---

### 2. 🌓 Mode sombre

Le dashboard dispose maintenant d'un **mode sombre** complet !

**Comment activer le mode sombre ?**
- Dans la sidebar → Section "Paramètres" → Toggle "Mode sombre"

**Caractéristiques** :
- Couleurs adaptées pour réduire la fatigue oculaire
- Contraste optimisé pour la lisibilité
- Graphiques et tableaux ajustés
- Transition fluide entre les deux modes

---

### 3. 🎨 Nouvelle sidebar personnalisée

La sidebar a été **complètement redessinée** :

**✅ Améliorations** :
- Logo Silao en haut de la sidebar
- Navigation simplifiée avec boutons clairs
- Sélecteur de langue intégré
- Toggle dark mode intégré
- Statut de connexion affiché
- Cache info en expander
- **Plus d'arborescence de pages Streamlit** (cachée)

**Navigation** :
- 🏠 Accueil
- ⚙️ Configuration
- 📊 Vue d'ensemble
- 🎯 Détail campagne
- 🔍 Termes de recherche
- ⚕️ Diagnostic

---

### 4. 🖼️ Icônes et images Silao

**Nouveau** :
- Logo Silao affiché dans la sidebar
- Favicon Silao (96x96)
- Cohérence visuelle avec le site Silao-treehouse

**Emplacement des assets** :
- `/assets/logo-silao.png` - Logo principal
- `/assets/favicon-96x96.png` - Favicon

---

## 📁 Fichiers créés/modifiés

### Nouveaux fichiers

1. **`/config/i18n.py`** (280+ lignes)
   - Système d'internationalisation complet
   - Dictionnaires de traductions FR/EN/DE
   - Fonctions `t()`, `set_language()`, `get_language()`

2. **`/assets/custom-dark.css`** (200+ lignes)
   - CSS spécifique pour le mode sombre
   - Couleurs ajustées pour dark mode
   - Styles pour tous les composants

3. **`/components/sidebar.py`** (200+ lignes)
   - Sidebar personnalisée avec logo
   - Navigation intégrée
   - Sélecteurs langue et thème
   - Cache de la nav Streamlit par défaut

4. **`/assets/logo-silao.png`**
   - Logo Silao copié depuis silao-treehouse

5. **`/assets/favicon-96x96.png`**
   - Favicon Silao

### Fichiers modifiés

1. **`/utils/ui_helpers.py`**
   - Ajout de `init_theme()`, `get_theme()`, `toggle_theme()`
   - Chargement conditionnel du CSS dark mode

2. **`/app.py`**
   - Import i18n et thème
   - Utilisation de `render_custom_sidebar()`
   - Cache de la navigation par défaut

3. **Toutes les pages** (`/pages/*.py`)
   - Ajout imports i18n et thème
   - Utilisation de `render_custom_sidebar()`
   - Suppression des anciennes sidebars

---

## 🚀 Utilisation

### Changer de langue

1. Ouvrez l'application
2. Dans la sidebar, section "⚙️ Paramètres"
3. Sélectionnez votre langue (🇫🇷/🇬🇧/🇩🇪)
4. L'interface se met à jour automatiquement

### Activer le mode sombre

1. Dans la sidebar, section "⚙️ Paramètres"
2. Activez le toggle "Mode sombre"
3. Les couleurs s'ajustent immédiatement

### Navigation

Utilisez les **boutons de navigation** dans la sidebar :
- Plus besoin de l'arborescence Streamlit par défaut
- Navigation intuitive avec icônes
- Un clic pour changer de page

---

## 🎯 Architecture technique

### Système i18n

```python
from config.i18n import t

# Utiliser une traduction
titre = t("home")  # "Accueil" (FR), "Home" (EN), "Startseite" (DE)
```

**Toutes les clés disponibles** :
- Navigation (home, config, overview, etc.)
- Métriques (impressions, clicks, ctr, etc.)
- Actions (refresh, export, import, etc.)
- Statuts (enabled, paused, removed, etc.)
- Messages (success, error, warning, etc.)

### Système de thème

```python
from utils.ui_helpers import get_theme, toggle_theme

# Obtenir le thème actuel
theme = get_theme()  # "dark" ou "light"

# Basculer le thème
toggle_theme()
```

### Sidebar personnalisée

```python
from components.sidebar import render_custom_sidebar, hide_default_navigation

# Cacher la navigation par défaut
hide_default_navigation()

# Afficher la sidebar personnalisée
render_custom_sidebar()
```

---

## 🎨 Design

### Mode clair (défaut)
- Fond blanc/gris clair
- Texte sombre
- Boutons bleus
- Bordures sketch

### Mode sombre
- Fond noir/gris foncé
- Texte clair
- Boutons bleus plus lumineux
- Bordures adaptées

---

## 📊 Comparaison versions

| Fonctionnalité | Version 1.0 | Version 2.0 |
|----------------|-------------|-------------|
| Langues | FR uniquement | FR/EN/DE |
| Thème | Clair uniquement | Clair + Sombre |
| Sidebar | Streamlit par défaut | Personnalisée Silao |
| Logo | ❌ Non | ✅ Oui (Silao) |
| Navigation | Arborescence | Boutons directs |
| Paramètres | Dispersés | Centralisés sidebar |

---

## 🔧 Personnalisation

### Ajouter une langue

Éditez `/config/i18n.py` :

```python
TRANSLATIONS = {
    "fr": { ... },
    "en": { ... },
    "de": { ... },
    "es": {  # Nouvelle langue
        "home": "Inicio",
        "config": "Configuración",
        # ... etc
    }
}
```

### Modifier les couleurs dark mode

Éditez `/assets/custom-dark.css` :

```css
:root {
  --primary: 220 80% 50%;  /* Votre couleur */
  --background: 222 47% 11%;  /* Fond sombre */
  /* ... */
}
```

---

## 🎉 Prochaines étapes

1. **Tester l'application** en mode clair et sombre
2. **Essayer les 3 langues** pour vérifier les traductions
3. **Naviguer** avec la nouvelle sidebar
4. **Donner du feedback** sur l'UX

---

## ❓ FAQ

### Comment revenir à l'ancienne sidebar ?

Commentez l'appel dans chaque page :
```python
# render_custom_sidebar()
```

### Puis-je personnaliser les traductions ?

Oui, éditez `/config/i18n.py` et modifiez les dictionnaires `TRANSLATIONS`.

### Le mode sombre fonctionne-t-il sur mobile ?

Oui ! Le mode sombre est responsive et fonctionne sur tous les appareils.

### Comment cacher le logo Silao ?

Dans `/components/sidebar.py`, commentez la section "Logo Silao".

---

**Version** : 2.0.0  
**Date** : 22/05/2026  
**Développé avec** ❤️ **par Silao**

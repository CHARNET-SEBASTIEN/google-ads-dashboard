# 🔧 Guide de dépannage

## ❓ "Rien ne fonctionne"

### Vérifications de base

#### 1. L'application est-elle accessible ?

Ouvrez : **http://localhost:8501**

**Si la page ne charge pas** :
```bash
# Vérifier que le container tourne
docker-compose ps

# Voir les logs
docker-compose logs google-ads-dashboard

# Redémarrer
docker-compose restart
```

#### 2. Le design ne s'applique pas ?

**Symptômes** :
- Pas de logo Google Ads
- Couleurs par défaut Streamlit (rouge/blanc)
- Pas de mode sombre
- Topbar absente

**Solution** :
1. **Vider le cache du navigateur** : Cmd+Shift+R (Mac) ou Ctrl+Shift+R (Windows)
2. **Vider le cache Streamlit** : Dans l'app, sidebar → Cache → Vider
3. **Rebuild complet** :
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

#### 3. Les contrôles ne fonctionnent pas ?

**Topbar (langue/mode) absente** :
- Vérifiez en haut à DROITE de la page
- Les contrôles sont dans des colonnes Streamlit
- Peut être invisible sur petit écran

**Mode sombre ne s'active pas** :
- Cliquez sur 🌙 en haut à droite
- Attendez 2-3 secondes (rechargement)
- La page doit devenir noire

**Changement de langue** :
- Selectbox en haut à droite
- Après changement, la page recharge
- Tout le texte doit changer

---

## 🐛 Problèmes connus et solutions

### Problème 1: Page blanche

**Cause** : Erreur Python non capturée

**Solution** :
```bash
# Voir les logs d'erreur
docker-compose logs google-ads-dashboard --tail=100

# Chercher "Error" ou "Traceback"
docker-compose logs google-ads-dashboard | grep -i error
```

### Problème 2: CSS non chargé

**Cause** : Fichiers CSS absents ou chemin incorrect

**Vérification** :
```bash
# Dans le container
docker exec google-ads-dashboard ls -la /app/assets/

# Doit afficher :
# custom.css
# custom-dark-rafo.css
# google-ads-logo.svg
```

**Solution si absents** :
```bash
# Rebuild
docker-compose down
docker-compose up -d --build
```

### Problème 3: Imports Python échouent

**Symptôme** : Page d'erreur Streamlit

**Solution** :
```bash
# Tester les imports
docker exec google-ads-dashboard python -c "from components.topbar import render_topbar; print('OK')"

# Si erreur, vérifier les fichiers
docker exec google-ads-dashboard ls -la /app/components/
docker exec google-ads-dashboard ls -la /app/utils/
```

### Problème 4: Préférences non sauvegardées

**Symptôme** : Langue/mode réinitalisés à chaque ouverture

**Cause** : Fichier .user_preferences.json non créé/accessible

**Solution** :
```bash
# Vérifier les permissions
docker exec google-ads-dashboard ls -la /app/.user_preferences.json

# Si absent, tester la création
docker exec google-ads-dashboard python -c "from utils.preferences import user_prefs; user_prefs.set_language('fr'); print('OK')"
```

### Problème 5: Topbar invisible

**Cause** : CSS non chargé ou positionnement incorrect

**Solution** :
1. Rafraîchir avec Cmd+Shift+R
2. Vérifier dans le code source (navigateur) si le CSS est présent
3. Ouvrir DevTools (F12) → Console → Chercher erreurs CSS

---

## 🔍 Tests manuels

### Test 1: Accès de base

1. Ouvrir http://localhost:8501
2. Attendre chargement (spinner Streamlit)
3. Doit afficher : "Google Ads Configuration Dashboard"

✅ **Succès** : Page d'accueil visible  
❌ **Échec** : Page blanche ou erreur → Voir logs Docker

### Test 2: Sidebar

1. Regarder à gauche
2. Doit voir :
   - Logo Google Ads (cercle bleu)
   - Titre "Google Ads Dashboard"
   - Statut de connexion
   - Boutons de navigation

✅ **Succès** : Sidebar complète visible  
❌ **Échec** : Sidebar vide/manquante → CSS non chargé

### Test 3: Topbar

1. Regarder en HAUT À DROITE
2. Doit voir :
   - Sélecteur de langue (🇫🇷 Français)
   - Bouton mode (🌙 ou ☀️)

✅ **Succès** : Contrôles visibles  
❌ **Échec** : Rien en haut à droite → Topbar non rendue

### Test 4: Mode sombre

1. Cliquer sur 🌙 en haut à droite
2. Page doit recharger
3. Fond doit devenir NOIR (#0a0a0a)
4. Sidebar doit devenir grise foncée
5. Texte doit devenir blanc

✅ **Succès** : Mode sombre complet  
❌ **Échec** : Rien ne change → CSS dark non chargé

### Test 5: Changement langue

1. Cliquer sur selectbox langue
2. Choisir English ou Deutsch
3. Page recharge
4. Texte navigation change

✅ **Succès** : Traductions appliquées  
❌ **Échec** : Texte inchangé → i18n non fonctionnel

---

## 📸 Captures d'écran attendues

### Mode Clair
```
┌────────────────────────────────────────┐
│  [🇫🇷 Français] [🌙]         (topbar)  │
├────────────────────────────────────────┤
│ ┌─────┐  │  Google Ads Configuration  │
│ │Logo │  │  Dashboard                 │
│ │ Ads │  │                            │
│ └─────┘  │  👋 Bienvenue !           │
│          │                            │
│ NAVIGAT. │  Cette application...     │
│ 🏠 Home  │                            │
│ ⚙️ Config│                            │
│          │                            │
└──────────┴────────────────────────────┘
   Sidebar     Contenu principal
```

### Mode Sombre RAFO
```
┌────────────────────────────────────────┐
│  [🇫🇷 Français] [☀️]         (topbar)  │
├────────────────────────────────────────┤
█ ┌─────┐  █  Google Ads Configuration  █
█ │Logo │  █  Dashboard                 █
█ │ Ads │  █                            █
█ └─────┘  █  👋 Bienvenue !           █
█          █                            █
█ NAVIGAT. █  Cette application...     █
█ 🏠 Home  █                            █
█ ⚙️ Config█                            █
█          █                            █
└──────────┴────────────────────────────┘
   Fond noir #0a0a0a partout
   Sidebar grise #141414
```

---

## 🚨 Si RIEN ne fonctionne

### Solution radicale : Rebuild complet

```bash
# 1. Arrêter et supprimer tout
docker-compose down -v

# 2. Supprimer l'image
docker rmi googe_ads_perso-google-ads-dashboard

# 3. Rebuild from scratch
docker-compose build --no-cache

# 4. Relancer
docker-compose up -d

# 5. Attendre 10 secondes
sleep 10

# 6. Vérifier les logs
docker-compose logs google-ads-dashboard --tail=50

# 7. Ouvrir navigateur
open http://localhost:8501
```

### Vérifier les fichiers locaux

```bash
# Lister les fichiers critiques
ls -la assets/custom*.css
ls -la components/*.py
ls -la utils/*.py
ls -la config/i18n.py

# Vérifier la syntaxe Python
python3 -m py_compile app.py
python3 -m py_compile components/sidebar.py
python3 -m py_compile components/topbar.py
```

---

## 📞 Informations de debug à fournir

Si rien ne fonctionne, fournissez :

1. **Logs Docker** :
```bash
docker-compose logs google-ads-dashboard > /tmp/logs.txt
```

2. **Capture d'écran** de ce que vous voyez

3. **Console navigateur** (F12 → Console tab)

4. **Version de Docker** :
```bash
docker --version
docker-compose --version
```

5. **Système d'exploitation** : macOS / Windows / Linux

---

## ✅ Checklist de fonctionnement

Cochez ce qui fonctionne :

- [ ] Application accessible sur http://localhost:8501
- [ ] Logo Google Ads visible dans sidebar
- [ ] Titre "Google Ads Dashboard" visible
- [ ] Boutons de navigation visibles
- [ ] Topbar en haut à droite visible
- [ ] Sélecteur de langue fonctionne
- [ ] Mode sombre s'active (fond noir)
- [ ] Mode clair s'active (fond blanc)
- [ ] Préférences sauvegardées entre sessions
- [ ] Navigation entre pages fonctionne

**Si TOUT est coché** : ✅ Application OK  
**Si certains manquent** : Voir sections correspondantes ci-dessus

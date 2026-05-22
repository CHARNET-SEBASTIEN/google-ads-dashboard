# 🚀 Démarrage rapide — 5 minutes

## 📋 Checklist avant de commencer

- [ ] Python 3.11+ installé
- [ ] Un compte Google Ads actif
- [ ] 5 minutes devant vous

---

## Étape 1 : Google Cloud Console (2 minutes)

### 1.1 Créer un projet

1. Allez sur https://console.cloud.google.com/
2. **Créer un projet** → Nom : `Google-Ads-Dashboard`
3. Sélectionnez le projet

### 1.2 Activer l'API Google Ads

1. Menu ☰ → **APIs & Services** → **Library**
2. Recherchez : `Google Ads API`
3. Cliquez sur **Enable**

### 1.3 Créer des credentials OAuth

1. Menu ☰ → **APIs & Services** → **Credentials**
2. **+ CREATE CREDENTIALS** → **OAuth client ID**
3. Type : **Desktop app**
4. Nom : `Google Ads Dashboard`
5. **CREATE**
6. **⬇️ DOWNLOAD JSON**
7. Renommez le fichier téléchargé : `client_secret.json`
8. **Placez-le à la racine de ce projet**

---

## Étape 2 : Google Ads (1 minute)

### 2.1 Récupérer le Developer Token

1. Connectez-vous à https://ads.google.com/
2. **Outils** (🔧) → **Configuration** → **Centre API**
3. Notez votre **Developer Token** (commence par `_` en mode test)

### 2.2 Récupérer le Customer ID

1. En haut à droite de Google Ads
2. Notez le numéro de compte (ex : `123-456-7890`)

---

## Étape 3 : Lancer l'application (2 minutes)

### Option A — Avec Docker (recommandé)

```bash
# Assurez-vous que client_secret.json est à la racine
ls client_secret.json

# Lancer l'application
docker-compose up --build

# Ouvrir dans le navigateur
open http://localhost:8501
```

### Option B — Sans Docker

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer Streamlit
streamlit run app.py

# Ouvrir dans le navigateur
# (s'ouvre automatiquement à http://localhost:8501)
```

---

## Étape 4 : Configuration dans l'application (1 minute)

1. Cliquez sur **🔧 Configuration** dans le menu latéral
2. Saisissez :
   - **Developer Token** (récupéré à l'étape 2.1)
   - **Customer ID** (récupéré à l'étape 2.2, sans tirets : `1234567890`)
3. Cliquez sur **🔐 Autoriser avec Google**
4. Une fenêtre de navigateur s'ouvre → connectez-vous
5. Autorisez l'accès
6. ✅ **C'est terminé !**

---

## ✅ Vérification

Si tout fonctionne, vous devriez voir :
- ✅ Connexion réussie au compte
- Le nom de votre compte affiché
- Le bouton "📊 Aller à la vue d'ensemble" actif

---

## 🐛 Problèmes courants

### "Fichier client_secret.json introuvable"
➡️ Vérifiez qu'il est bien à la racine du projet (même niveau que `app.py`)

### "DEVELOPER_TOKEN_NOT_APPROVED"
➡️ Normal en mode test — vous pouvez uniquement accéder à votre propre compte

### "Port 8501 déjà utilisé"
➡️ Changez le port : `streamlit run app.py --server.port 8502`

### "Module X not found"
➡️ Réinstallez les dépendances : `pip install -r requirements.txt --force-reinstall`

---

## 📚 Prochaines étapes

Une fois connecté :
1. 📊 **Vue d'ensemble** — Explorez toutes vos campagnes
2. 🎯 **Détail campagne** — Analysez la configuration d'une campagne
3. 🔍 **Termes de recherche** — Identifiez les requêtes hors-cible
4. ⚕️ **Diagnostic** — Obtenez des recommandations automatiques

---

**Besoin d'aide ?** Consultez le [README.md](README.md) complet.

# 📊 Google Ads Dashboard

Dashboard professionnel pour visualiser et analyser vos campagnes Google Ads avec un design inspiré de RAFO.

## ✨ Fonctionnalités

- 📈 Vue d'ensemble des campagnes
- 🎯 Analyse détaillée par campagne
- 🔍 Termes de recherche réels
- ⚕️ Diagnostic automatique
- 💾 Mode hors-ligne avec cache
- 🌓 Mode clair/sombre RAFO authentique
- 🌍 Multilingue (FR/EN/DE)

## 🎨 Design

Interface inspirée de [RAFO](https://rafo-chapters.com) avec:
- Mode clair: tons beiges/neutres chauds
- Mode sombre: tons bruns sophistiqués
- Design épuré et minimaliste
- Typographie Inter

## 🚀 Installation

### Prérequis

- Docker & Docker Compose
- Compte Google Ads avec accès API
- `client_secret.json` depuis Google Cloud Console

### Lancement

```bash
# Cloner le repo
git clone <repo-url>
cd google-ads-dashboard

# Lancer avec Docker
docker-compose up -d

# Ouvrir http://localhost:8501
```

## 📁 Structure

```
.
├── app.py                 # Application principale
├── pages/                 # Pages Streamlit
├── components/            # Composants UI (sidebar, topbar)
├── modules/              # Logique métier (API, cache)
├── utils/                # Helpers (UI, préférences)
├── config/               # Configuration (i18n, settings)
├── assets/               # CSS et ressources
└── docker-compose.yml    # Configuration Docker
```

## 🔧 Configuration

1. **API Google Ads**:
   - Créez un projet sur [Google Cloud Console](https://console.cloud.google.com)
   - Activez l'API Google Ads
   - Créez des credentials OAuth 2.0
   - Téléchargez `client_secret.json` et placez-le à la racine

2. **Google Ads Scripts** (optionnel):
   - Exportez vos données via Google Ads Scripts
   - Importez le fichier JSON dans l'application

## 🌐 Langues

- 🇫🇷 Français
- 🇬🇧 English
- 🇩🇪 Deutsch

## 📄 Licence

Propriétaire - Tous droits réservés

## 👤 Auteur

Sebastien Charnet

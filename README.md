# 📊 Dashboard Google Ads - Application Full Stack

Application moderne de gestion et d'analyse de campagnes Google Ads avec architecture full stack **FastAPI** (backend) et **Angular 17** (frontend).

## 🎯 Vue d'ensemble

Cette application permet de :
- 📈 Visualiser et analyser les performances de vos campagnes Google Ads
- 🔍 Détecter automatiquement les termes de recherche suspects
- ⚕️ Diagnostiquer les problèmes de campagnes avec 7 règles intelligentes
- 📊 Consulter des graphiques interactifs de performance
- 🌍 Utiliser l'interface en français, anglais ou allemand
- 🎨 Profiter d'un thème moderne avec mode sombre/clair

## 🏗️ Architecture

### Backend - FastAPI
- API REST avec authentification JWT
- OAuth2 Google Ads integration
- Import de données depuis JSON ou Google Drive
- 7 règles de diagnostic automatique
- Export CSV des données

### Frontend - Angular 17
- Application SPA moderne avec standalone components
- 6 pages principales (Home, Config, Campaigns, Detail, Search Terms, Diagnostic)
- Composants réutilisables (metric-card, chart, alert, etc.)
- Internationalisation (FR/EN/DE)
- Thème moderne adaptatif avec mode sombre/clair
- Charts Plotly.js

## 📦 Installation

### Prérequis
- **Node.js** 18+ et npm
- **Python** 3.9+
- **Compte Google Ads** avec API activée

### Installation Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configuration
cp .env.example .env
# Éditer .env avec vos credentials Google Ads
```

### Installation Frontend

```bash
cd frontend
npm install
```

## 🚀 Lancement

### Développement

**Option 1 : Script automatique (recommandé)**
```bash
# Démarrer backend + frontend
./start-dev.sh

# Arrêter tous les services
./stop.sh

# Arrêter uniquement le backend
./stop.sh backend

# Arrêter uniquement le frontend
./stop.sh frontend
```

**Option 2 : Lancement manuel**

Terminal 1 - Backend :
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Terminal 2 - Frontend :
```bash
cd frontend
npm start
```

Accéder à l'application : **http://localhost:4201**

### Production

```bash
# Backend
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run build
# Servir dist/frontend/ avec Nginx, Apache, etc.
```

## 📁 Structure du projet

```
.
├── backend/                  # API FastAPI
│   ├── app/
│   │   ├── api/             # Endpoints REST
│   │   ├── core/            # Config, sécurité, DB
│   │   ├── models/          # Modèles Pydantic
│   │   ├── services/        # Logique métier
│   │   └── main.py          # Point d'entrée
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                 # Application Angular
│   ├── src/
│   │   ├── app/
│   │   │   ├── core/       # Services core
│   │   │   ├── features/   # Pages
│   │   │   └── shared/     # Composants réutilisables
│   │   ├── assets/
│   │   └── environments/
│   ├── package.json
│   └── README.md
│
├── .credentials/            # Credentials Google (gitignored)
├── data/                    # Données importées (gitignored)
└── README.md               # Ce fichier
```

## 🔐 Configuration

### Backend (.env)

```bash
# Application
APP_NAME="Google Ads Dashboard"
DEBUG=True

# API
API_PREFIX=/api

# CORS (comma-separated)
CORS_ORIGINS=http://localhost:4200,http://localhost:3000

# JWT
SECRET_KEY=your-secret-key-change-in-production-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Google Ads API
GOOGLE_ADS_API_VERSION=v16

# Cache
CACHE_TTL=3600

# AI / LLM (pour le diagnostic IA)
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

### Frontend (environment.ts)

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

## 🎨 Interface moderne

L'interface propose :
- **Design** : Interface épurée et professionnelle
- **Typography** : Inter, system-ui
- **Mode sombre/clair** : Toggle automatique avec persistance
- **Composants** : Cards, buttons, badges, snackbar notifications
- **Responsive** : Adapté mobile, tablette et desktop

## 📊 Fonctionnalités principales

### 1. Vue d'ensemble des campagnes
- Liste complète avec filtres (statut, recherche)
- Métriques globales (impressions, clics, coût)
- Cartes interactives par campagne

### 2. Détail campagne
- **Overview** : Budget, conversions, CPC moyen
- **Keywords** : Liste des mots-clés avec performances
- **Ads** : Annonces avec headlines et descriptions
- **Performance** : Graphiques temporels interactifs

### 3. Termes de recherche
- Analyse complète des search terms
- Détection automatique des termes suspects
- Export CSV
- Filtres et recherche

### 4. Diagnostic IA
- **Analyse intelligente** avec Claude AI (Anthropic)
- Détection automatique des problèmes de campagnes
- Recommandations personnalisées par campagne
- Vue rapport (table triable ou markdown)
- Vue échéancier avec suivi de progression
- Export Excel des recommandations

### 5. Configuration
- Import JSON (format Google Ads export)
- Import depuis Google Drive (URL ou ID)
- Statut des données importées
- Authentification OAuth2 Google

## 🔌 API Endpoints

### Authentification
```
POST   /api/auth/login          # Connexion
GET    /api/auth/status         # Statut session
POST   /api/auth/logout         # Déconnexion
GET    /api/auth/google         # OAuth2 start
GET    /api/auth/callback       # OAuth2 callback
```

### Données
```
POST   /api/data/import-json    # Import JSON
POST   /api/data/import-drive   # Import Google Drive
GET    /api/data/status         # Statut données
```

### Campagnes
```
GET    /api/campaigns            # Liste campagnes
GET    /api/campaigns/:id        # Détail campagne
GET    /api/campaigns/:id/keywords      # Mots-clés
GET    /api/campaigns/:id/ads           # Annonces
GET    /api/campaigns/:id/performance   # Performance
```

### Search Terms
```
GET    /api/search-terms         # Tous les termes
GET    /api/search-terms/suspects # Termes suspects
GET    /api/search-terms/export  # Export CSV
```

### Diagnostics
```
POST   /api/diagnostics/ai-analysis        # Lancer analyse IA
GET    /api/diagnostics/ai-analysis/cached # Récupérer analyse en cache
```

## 🧪 Tests

### Backend
```bash
cd backend
pytest
pytest --cov=app tests/
```

### Frontend
```bash
cd frontend
npm test
npm run test:coverage
npm run e2e
```

## 📝 Documentation

- **Backend API** : http://localhost:8000/docs (Swagger UI)
- **Frontend README** : `frontend/README.md`
- **Backend README** : `backend/README.md`

## 🔧 Technologies utilisées

### Backend
- **FastAPI** - Framework web moderne
- **Pydantic** - Validation de données
- **SQLAlchemy** - ORM
- **JWT** - Authentification
- **Google Ads API** - Intégration Google
- **Pandas** - Manipulation de données

### Frontend
- **Angular 17** - Framework frontend
- **TypeScript** - Langage typé
- **RxJS** - Programmation réactive
- **Angular Material** - Composants UI
- **TailwindCSS** - Styling utilitaire
- **Plotly.js** - Visualisations
- **Transloco** - Internationalisation

## 🚀 Roadmap

- [ ] Tests E2E complets
- [ ] CI/CD pipeline
- [ ] Docker multi-stage optimisé
- [ ] Monitoring et logs centralisés
- [ ] Plus de règles de diagnostic
- [ ] Recommandations IA
- [ ] Export vers Google Ads
- [ ] Alertes email/Slack
- [ ] Tableau de bord temps réel

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'feat: Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

MIT License - voir LICENSE pour plus de détails

## 👤 Développement

Réalisé avec Claude Code

## 🙏 Remerciements

- Google Ads API
- Anthropic Claude AI
- Communautés Angular et FastAPI
- Contributeurs open source

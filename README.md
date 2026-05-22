# 📊 Dashboard Google Ads - Application Full Stack

Application moderne de gestion et d'analyse de campagnes Google Ads, migrée depuis Streamlit vers une architecture full stack avec **FastAPI** (backend) et **Angular 17** (frontend).

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
- Thème RAFO adaptatif
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

Accéder à l'application : **http://localhost:4200**

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
├── docker-compose.yml       # Orchestration Docker
└── README.md               # Ce fichier
```

## 🔐 Configuration

### Backend (.env)

```bash
# Database
DATABASE_URL=sqlite:///./google_ads.db

# JWT
SECRET_KEY=your-secret-key-change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Google Ads API
GOOGLE_ADS_DEVELOPER_TOKEN=your-developer-token
GOOGLE_ADS_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_ADS_CLIENT_SECRET=your-client-secret
GOOGLE_ADS_REDIRECT_URI=http://localhost:8000/api/auth/callback

# CORS
CORS_ORIGINS=["http://localhost:4200"]
```

### Frontend (environment.ts)

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

## 🎨 Thème RAFO

Le thème authentique RAFO est intégré avec :
- **Couleur primaire** : Orange RAFO (#FF6B35)
- **Typography** : Inter, system-ui
- **Mode sombre/clair** : Toggle automatique
- **Composants** : Cards, buttons, badges stylisés

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

### 4. Diagnostic
- 7 règles d'analyse automatique :
  1. Campagne en pause
  2. Budget limité
  3. Aucune conversion
  4. CTR faible
  5. CPA élevé
  6. Impressions faibles
  7. Taux de conversion faible
- Filtres par gravité (Critical, High, Medium, Low)
- Filtres par catégorie
- Recommandations et impacts détaillés

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
GET    /api/diagnostics          # Liste diagnostics
POST   /api/diagnostics/run      # Lancer analyse
GET    /api/diagnostics/export   # Export CSV
```

## 🐳 Docker

```bash
# Lancer avec Docker Compose
docker-compose up -d

# Accéder à l'application
# Frontend: http://localhost:4200
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
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

## 👤 Auteur

Développé avec ❤️ et Claude Code

## 🙏 Remerciements

- Google Ads API
- Communautés Angular et FastAPI
- Contributeurs open source

---

**Note** : Ce projet a été migré depuis une application Streamlit vers une architecture full stack moderne pour améliorer les performances, la scalabilité et l'expérience utilisateur.

# AdsPilot - Backend API

FastAPI backend for AdsPilot Google Ads intelligence platform.

## Installation

```bash
# Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer dépendances
pip install -r requirements.txt

# Copier et configurer .env
cp .env.example .env
# Éditer .env avec vos valeurs
```

## Configuration

Créer un fichier `.env` basé sur `.env.example` :

```env
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:4200
DEBUG=True
```

## Lancement

```bash
# Mode développement (auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Mode production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

L'API sera disponible sur `http://localhost:8000`

## Documentation

- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## Structure

```
backend/
├── app/
│   ├── api/              # Routes API
│   ├── config/           # Configuration
│   ├── core/             # Auth, security
│   ├── models/           # Pydantic schemas
│   ├── services/         # Logique métier
│   └── utils/            # Utilitaires
├── requirements.txt
└── .env
```

## Endpoints

### Authentication
- `POST /api/auth/google-oauth` - Démarre OAuth flow
- `POST /api/auth/google-callback` - Callback OAuth
- `GET /api/auth/status` - État authentification
- `POST /api/auth/logout` - Déconnexion

### Data Import
- `POST /api/data/import-json` - Upload JSON
- `POST /api/data/import-google-drive` - Import Google Drive
- `GET /api/data/status` - État des données

### Campaigns
- `GET /api/campaigns` - Liste campagnes
- `GET /api/campaigns/{id}` - Détail campagne
- `GET /api/campaigns/{id}/keywords` - Mots-clés
- `GET /api/campaigns/{id}/ads` - Annonces
- `GET /api/campaigns/{id}/performance` - Performances

### Search Terms
- `GET /api/search-terms` - Termes de recherche
- `GET /api/search-terms/suspects` - Termes suspects

### Diagnostics
- `GET /api/diagnostics` - Analyse complète
- `GET /api/diagnostics/summary` - Résumé
- `GET /api/diagnostics/rules` - Liste règles

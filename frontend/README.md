# AdsPilot - Frontend Angular

Modern Angular 17 application for managing and analyzing Google Ads campaigns.

## 🚀 Caractéristiques

### Architecture
- **Angular 17** avec standalone components (pas de NgModules)
- **TypeScript** avec typage strict
- **RxJS** pour la gestion d'état réactive
- **Angular Material 17** pour les composants UI
- **TailwindCSS** pour le styling utilitaire
- **Plotly.js** pour les visualisations de données

### Fonctionnalités
- 📊 Dashboard complet avec métriques en temps réel
- 🎯 Vue détaillée des campagnes avec onglets (overview, keywords, ads, performance)
- 🔍 Analyse des termes de recherche avec détection automatique des suspects
- ⚕️ Diagnostic intelligent avec 7 règles d'analyse
- 🌍 Support multilingue (FR, EN, DE) via Transloco
- 🎨 Thème RAFO avec mode sombre/clair
- 📈 Graphiques interactifs Plotly.js
- 🔐 Authentification JWT avec OAuth2 Google

## 📦 Installation

```bash
npm install
```

## 🛠️ Développement

```bash
# Démarrer le serveur de développement
npm start

# L'application sera accessible sur http://localhost:4200
```

## 🏗️ Build

```bash
# Build de production
npm run build

# Les fichiers seront générés dans dist/frontend/
```

## 🧪 Tests

```bash
# Tests unitaires
npm test

# Tests E2E
npm run e2e

# Coverage
npm run test:coverage
```

## 📁 Structure du projet

```
src/
├── app/
│   ├── core/                    # Services et intercepteurs core
│   │   ├── services/
│   │   │   ├── api.service.ts           # Service HTTP wrapper
│   │   │   ├── auth.service.ts          # Gestion authentification
│   │   │   ├── theme.service.ts         # Gestion thème dark/light
│   │   │   └── campaign.service.ts      # API campagnes
│   │   └── interceptors/
│   │       └── auth.interceptor.ts      # Injection JWT
│   │
│   ├── features/                # Pages de l'application
│   │   ├── home/                        # Page d'accueil
│   │   ├── configuration/               # Import données
│   │   ├── campaigns/
│   │   │   ├── overview/               # Liste campagnes
│   │   │   └── detail/                 # Détail campagne
│   │   ├── search-terms/               # Termes de recherche
│   │   └── diagnostic/                 # Analyse diagnostic
│   │
│   ├── shared/                  # Composants réutilisables
│   │   └── components/
│   │       ├── sidebar/                # Navigation latérale
│   │       ├── topbar/                 # Barre supérieure
│   │       ├── metric-card/            # Card métriques
│   │       ├── campaign-card/          # Card campagne
│   │       ├── chart/                  # Wrapper Plotly.js
│   │       ├── loading-spinner/        # Spinner chargement
│   │       ├── empty-state/            # État vide
│   │       └── alert/                  # Notifications
│   │
│   ├── app.component.ts         # Composant racine
│   ├── app.routes.ts            # Configuration routing
│   └── app.config.ts            # Configuration app
│
├── assets/
│   └── i18n/                    # Fichiers de traductions
│       ├── fr.json
│       ├── en.json
│       └── de.json
│
├── environments/                # Configuration environnements
│   ├── environment.ts           # Développement
│   └── environment.prod.ts      # Production
│
└── styles.scss                  # Styles globaux + thème RAFO
```

## 🎨 Thème RAFO

Le thème RAFO est intégré via CSS variables pour supporter le mode sombre/clair :

```scss
// Variables principales
--primary-color: #FF6B35
--background: #FFFFFF / #1A1A1A
--text-primary: #1F2937 / #F9FAFB
--surface-primary: #FFFFFF / #262626
```

### Changer de thème

```typescript
// Dans un composant
constructor(private themeService: ThemeService) {}

toggleTheme() {
  this.themeService.toggleTheme();
}
```

## 🌍 Internationalisation

Le projet utilise Transloco pour le support multilingue.

### Ajouter une traduction

1. Ajouter la clé dans `assets/i18n/fr.json`, `en.json`, `de.json`
2. Utiliser dans le template :

```html
<h1>{{ 'nav.home' | transloco }}</h1>
```

### Changer de langue

```typescript
constructor(private translocoService: TranslocoService) {}

changeLanguage(lang: string) {
  this.translocoService.setActiveLang(lang);
}
```

## 📊 Utilisation des composants

### MetricCard

```html
<app-metric-card
  label="Impressions"
  [value]="12500"
  icon="👁️"
  [trend]="5.2"
  color="green"
></app-metric-card>
```

### Chart

```typescript
chartData: ChartData[] = [{
  x: ['2024-01', '2024-02', '2024-03'],
  y: [100, 150, 200],
  type: 'scatter',
  mode: 'lines+markers',
  name: 'Impressions'
}];

chartLayout: ChartLayout = {
  title: 'Performance',
  height: 400
};
```

```html
<app-chart
  [data]="chartData"
  [layout]="chartLayout"
></app-chart>
```

### Alert

```html
<app-alert
  type="success"
  title="Succès"
  message="Données importées avec succès"
  [dismissible]="true"
></app-alert>
```

### LoadingSpinner

```html
<app-loading-spinner
  [size]="50"
  message="Chargement en cours..."
  [fullscreen]="true"
></app-loading-spinner>
```

### EmptyState

```html
<app-empty-state
  icon="📭"
  title="Aucune campagne"
  message="Importez vos données pour commencer"
>
  <button>Importer</button>
</app-empty-state>
```

## 🔌 API Backend

L'application se connecte au backend FastAPI :

- **URL par défaut** : `http://localhost:8000/api`
- Configurable dans `environments/environment.ts`

### Endpoints principaux

```typescript
GET  /api/campaigns              // Liste des campagnes
GET  /api/campaigns/:id          // Détail campagne
GET  /api/campaigns/:id/keywords // Mots-clés
GET  /api/campaigns/:id/ads      // Annonces
GET  /api/campaigns/:id/performance // Performance
GET  /api/search-terms           // Termes de recherche
GET  /api/search-terms/suspects  // Termes suspects
GET  /api/diagnostics            // Diagnostic
POST /api/data/import-json       // Import JSON
POST /api/auth/login             // Connexion
```

## 🔒 Authentification

Le système d'authentification utilise JWT :

1. L'utilisateur se connecte via OAuth2 Google ou login/password
2. Le backend retourne un token JWT
3. L'intercepteur ajoute automatiquement le token aux requêtes
4. Le token est stocké dans localStorage

```typescript
// Vérifier si connecté
this.authService.isAuthenticated$.subscribe(isAuth => {
  console.log('Authenticated:', isAuth);
});

// Se déconnecter
this.authService.logout();
```

## 🚢 Déploiement

### Build de production

```bash
npm run build
```

### Variables d'environnement

Créer `environment.prod.ts` :

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://api.votre-domaine.com/api'
};
```

### Servir l'application

Les fichiers statiques dans `dist/frontend/` peuvent être servis par :
- **Nginx**
- **Apache**
- **Firebase Hosting**
- **Vercel**
- **Netlify**

Configuration Nginx exemple :

```nginx
server {
  listen 80;
  server_name votre-domaine.com;
  root /var/www/frontend/dist/frontend;
  index index.html;

  location / {
    try_files $uri $uri/ /index.html;
  }
}
```

## 📝 Conventions de code

- **Composants** : PascalCase (`CampaignCardComponent`)
- **Services** : PascalCase avec suffix Service (`ApiService`)
- **Fichiers** : kebab-case (`campaign-card.component.ts`)
- **CSS classes** : kebab-case (`campaign-card`)
- **Variables** : camelCase (`campaignId`)
- **Constantes** : UPPER_SNAKE_CASE (`API_URL`)

## 🐛 Debugging

### Angular DevTools

Installer l'extension Chrome "Angular DevTools" pour :
- Inspecter la hiérarchie des composants
- Voir les propriétés et bindings
- Profiler les performances

### Console logs

```typescript
// En développement
if (!environment.production) {
  console.log('Debug info:', data);
}
```

## 📚 Ressources

- [Documentation Angular](https://angular.io/docs)
- [Angular Material](https://material.angular.io)
- [TailwindCSS](https://tailwindcss.com)
- [Plotly.js](https://plotly.com/javascript/)
- [Transloco](https://ngneat.github.io/transloco/)

## 🤝 Contribution

1. Créer une branche : `git checkout -b feature/ma-fonctionnalite`
2. Commiter : `git commit -m 'feat: Ajouter fonctionnalité'`
3. Push : `git push origin feature/ma-fonctionnalite`
4. Créer une Pull Request

## 📄 Licence

MIT

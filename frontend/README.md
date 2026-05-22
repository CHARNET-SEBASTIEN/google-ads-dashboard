# Google Ads Dashboard - Frontend

Frontend Angular 17 pour le dashboard Google Ads.

## Technologies

- **Angular 17** - Framework frontend
- **Angular Material** - Components UI
- **TailwindCSS** - Utility-first CSS
- **Transloco** - Internationalisation (FR/EN/DE)
- **Plotly.js** - Graphiques interactifs
- **TypeScript** - Langage typé

## Installation

\`\`\`bash
# Installer dépendances
npm install

# Lancer en développement
npm start
# ou
ng serve

# Ouvrir http://localhost:4200
\`\`\`

## Configuration

### API Backend

Modifier \`src/environments/environment.ts\` :

\`\`\`typescript
export const environment = {
  apiUrl: 'http://localhost:8000/api'
};
\`\`\`

## Structure

- \`src/app/core/\` - Services globaux, guards, interceptors
- \`src/app/features/\` - Pages fonctionnelles
- \`src/app/shared/\` - Composants réutilisables
- \`src/assets/i18n/\` - Traductions FR/EN/DE

## Développement

\`\`\`bash
npm start      # Dev server
npm run build  # Build production
npm test       # Tests
\`\`\`

## Thème RAFO

Variables CSS light/dark mode dans \`src/styles.scss\`

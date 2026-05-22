# 🚀 Migration Streamlit → Angular - Prochaines Étapes

## ✅ Progrès Actuel : 60%

### Backend : 75% ✅
- Infrastructure complète
- Authentification OAuth + JWT
- Tous les endpoints API (15 routes)
- Services métier (GoogleAds, DataLoader, Diagnostics)

### Frontend : 60% ✅
- Infrastructure + setup
- Layout complet (Sidebar + Topbar)
- Services core (API, Auth, Theme)
- Routing configuré
- Home page complète
- Composant metric-card
- Thème RAFO fonctionnel (dark/light)

---

## 📝 Tâches Restantes

### Phase 5 : Pages & Composants (40% - EN COURS)

#### Composants à créer (14)
- [ ] campaign-card
- [ ] keyword-card
- [ ] search-term-card
- [ ] diagnostic-issue-card
- [ ] chart-wrapper (Plotly.js integration)
- [ ] data-table (avec tri/filtre/pagination)
- [ ] filter-bar
- [ ] file-upload (drag & drop)
- [ ] status-badge
- [ ] alert-banner
- [ ] empty-state
- [ ] loading-spinner
- [ ] confirm-dialog
- [ ] stats-overview

#### Pages à compléter (5)
- [ ] Configuration page
  - Upload JSON
  - Google Drive import
  - Statistiques données
- [ ] Campaigns Overview page
  - Liste campagnes
  - Filtres (statut, recherche)
  - Export CSV
- [ ] Campaign Detail page
  - Sélecteur campagne
  - Tabs (overview, keywords, performance, config)
  - Charts Plotly
- [ ] Search Terms page
  - Liste termes
  - Détection suspects
  - Filtres
- [ ] Diagnostic page
  - Liste issues par sévérité
  - Filtres
  - Recommandations

### Phase 6 : Thème & i18n (20% - PARTIEL)

#### Thème RAFO
- ✅ Variables CSS créées
- ✅ Dark/light toggle fonctionnel
- [ ] Appliquer sur tous les composants
- [ ] Responsive mobile/tablet complet
- [ ] Animations et transitions avancées

#### Internationalisation
- ✅ Transloco configuré (FR/EN/DE)
- ✅ Fichiers i18n de base
- [ ] Compléter toutes les traductions
- [ ] Pipe de formatage (dates, devises)

### Phase 7 : Tests (0%)
- [ ] Tests unitaires backend (pytest)
- [ ] Tests unitaires frontend (Jest)
- [ ] Tests e2e (Playwright)

### Phase 8 : Déploiement (0%)
- [ ] Dockerfile backend
- [ ] Dockerfile frontend  
- [ ] docker-compose.yml
- [ ] CI/CD GitHub Actions
- [ ] Documentation

---

## 🎯 Objectif Prochain : Pages Fonctionnelles

### Priorité 1 : Configuration Page
Créer page d'upload/import données pour connecter frontend au backend.

**Fichier** : `frontend/src/app/features/configuration/configuration.component.ts`

**Fonctionnalités** :
- Upload fichier JSON (via ApiService)
- Import Google Drive (avec file_id)
- Affichage statut données
- Stats (nb campagnes, keywords, ads)

### Priorité 2 : Campaigns Overview Page
Afficher liste des campagnes depuis l'API.

**Fichier** : `frontend/src/app/features/campaigns/overview/overview.component.ts`

**Fonctionnalités** :
- Appel GET /api/campaigns
- Affichage campaign-cards
- Filtres (statut, recherche)
- Pagination

### Priorité 3 : Chart Wrapper
Intégrer Plotly.js pour les graphiques.

**Fichier** : `frontend/src/app/shared/components/chart-wrapper/chart-wrapper.component.ts`

**Fonctionnalités** :
- Input data/layout/config
- Render Plotly chart
- Responsive
- Dark mode support

---

## 💡 Commandes Utiles

### Générer un composant
```bash
cd frontend
ng generate component shared/components/campaign-card --skip-tests
```

### Générer un service
```bash
ng generate service core/services/campaign
```

### Lancer le dev
```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend
cd frontend
npm start
```

### Tester l'API
```bash
curl http://localhost:8000/api/health
curl http://localhost:8000/api/docs  # Swagger UI
```

---

## 📊 Metrics

| Phase | Progression | Temps estimé restant |
|-------|-------------|---------------------|
| Phase 1-3 (Backend) | ✅ 100% | 0h |
| Phase 4 (Layout) | ✅ 100% | 0h |
| Phase 5 (Components) | ⏳ 40% | ~8h |
| Phase 6 (Theme) | ⏳ 60% | ~3h |
| Phase 7 (Tests) | ⏳ 0% | ~6h |
| Phase 8 (Deploy) | ⏳ 0% | ~3h |
| **TOTAL** | **60%** | **~20h** |

---

## 🎨 Captures d'écran Attendues

### Home Page
- [x] Hero avec titre/description
- [x] Status pills si authentifié
- [x] Cards fonctionnalités
- [x] Quick links vers pages

### Sidebar
- [x] Logo + titre
- [x] Navigation 6 items
- [x] Active state
- [x] Footer version

### Topbar
- [x] Sélecteur langue FR/EN/DE
- [x] Toggle dark/light
- [x] User info + logout

---

## 🔧 Debug

### Backend ne démarre pas
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend erreurs TypeScript
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Routes ne fonctionnent pas
Vérifier `app.routes.ts` et imports des composants lazy-loaded.

---

**Dernière mise à jour** : $(date)
**Backend** : 75% ✅
**Frontend** : 60% ⏳
**Global** : 60% ⏳

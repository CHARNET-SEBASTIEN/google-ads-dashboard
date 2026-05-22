import { Routes } from '@angular/router';
import { HomeComponent } from './features/home/home.component';
import { ConfigurationComponent } from './features/configuration/configuration.component';
import { OverviewComponent } from './features/campaigns/overview/overview.component';

export const routes: Routes = [
  {
    path: '',
    component: HomeComponent
  },
  {
    path: 'configuration',
    component: ConfigurationComponent
  },
  {
    path: 'campaigns',
    component: OverviewComponent
  },
  {
    path: 'campaign-detail',
    loadComponent: () => import('./features/campaigns/detail/detail.component').then(m => m.DetailComponent)
  },
  {
    path: 'search-terms',
    loadComponent: () => import('./features/search-terms/search-terms.component').then(m => m.SearchTermsComponent)
  },
  {
    path: 'diagnostic',
    loadComponent: () => import('./features/diagnostic/diagnostic.component').then(m => m.DiagnosticComponent)
  },
  {
    path: '**',
    redirectTo: ''
  }
];

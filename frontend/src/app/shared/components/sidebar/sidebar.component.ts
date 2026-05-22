import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { TranslocoModule } from '@jsverse/transloco';

interface MenuItem {
  icon: string;
  label: string;
  route: string;
  translationKey: string;
}

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule, TranslocoModule],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.scss'
})
export class SidebarComponent {
  menuItems: MenuItem[] = [
    { icon: '🏠', label: 'Accueil', route: '/', translationKey: 'nav.home' },
    { icon: '⚙️', label: 'Configuration', route: '/configuration', translationKey: 'nav.config' },
    { icon: '📊', label: 'Vue d\'ensemble', route: '/campaigns', translationKey: 'nav.overview' },
    { icon: '🎯', label: 'Détail campagne', route: '/campaign-detail', translationKey: 'nav.campaign_detail' },
    { icon: '🔍', label: 'Termes recherche', route: '/search-terms', translationKey: 'nav.search_terms' },
    { icon: '⚕️', label: 'Diagnostic', route: '/diagnostic', translationKey: 'nav.diagnostic' }
  ];

  constructor(public router: Router) {}
}

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { TranslocoModule, TranslocoService } from '@jsverse/transloco';
import { ThemeService } from '../../../core/services/theme.service';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-topbar',
  standalone: true,
  imports: [CommonModule, TranslocoModule],
  templateUrl: './topbar.component.html',
  styleUrl: './topbar.component.scss'
})
export class TopbarComponent implements OnInit {
  pageTitle: string = '';
  pageTitleKey: string = 'app.title';
  isDarkMode = false;
  currentLang = 'fr';
  isAuthenticated = false;
  customerName?: string;

  languages = [
    { code: 'fr', label: '🇫🇷 FR' },
    { code: 'en', label: '🇬🇧 EN' },
    { code: 'de', label: '🇩🇪 DE' }
  ];

  constructor(
    private themeService: ThemeService,
    private translocoService: TranslocoService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit() {
    // Subscribe to theme changes
    this.themeService.getTheme().subscribe(theme => {
      this.isDarkMode = theme === 'dark';
    });

    // Get current language
    this.currentLang = this.translocoService.getActiveLang();

    // Subscribe to auth status
    this.authService.getAuthStatus().subscribe(status => {
      this.isAuthenticated = status.authenticated;
      this.customerName = status.customer_name;
    });

    // Update page title on route change
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe(() => {
      this.updatePageTitle();
    });

    // Set initial title
    this.updatePageTitle();
  }

  private updatePageTitle() {
    const route = this.router.url;
    if (route === '/' || route === '/home') {
      this.pageTitleKey = 'nav.home';
    } else if (route.includes('/configuration')) {
      this.pageTitleKey = 'nav.config';
    } else if (route.includes('/campaign-detail')) {
      this.pageTitleKey = 'nav.campaign_detail';
    } else if (route.includes('/campaigns')) {
      this.pageTitleKey = 'nav.overview';
    } else if (route.includes('/search-terms')) {
      this.pageTitleKey = 'nav.search_terms';
    } else if (route.includes('/diagnostic')) {
      this.pageTitleKey = 'nav.diagnostic';
    } else {
      this.pageTitleKey = 'app.title';
    }
  }

  toggleTheme() {
    this.themeService.toggleTheme();
  }

  changeLanguage(lang: string) {
    this.currentLang = lang;
    this.translocoService.setActiveLang(lang);
  }

  logout() {
    this.authService.logout().subscribe();
  }
}

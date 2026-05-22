import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { TranslocoModule, TranslocoService } from '@jsverse/transloco';
import { ThemeService } from '../../../core/services/theme.service';
import { AuthService } from '../../../core/services/auth.service';
import { ApiService } from '../../../core/services/api.service';
import { DiagnosticService } from '../../../core/services/diagnostic.service';
import { SnackbarService } from '../../../core/services/snackbar.service';

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
  showHelp = false;
  isDriveConfigured = false;

  languages = [
    { code: 'fr', label: '🇫🇷 FR' },
    { code: 'en', label: '🇬🇧 EN' },
    { code: 'de', label: '🇩🇪 DE' }
  ];

  constructor(
    private themeService: ThemeService,
    private translocoService: TranslocoService,
    private authService: AuthService,
    private router: Router,
    private api: ApiService,
    private diagnosticService: DiagnosticService,
    private snackbar: SnackbarService
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

    // Load Drive configuration status
    this.checkDriveConfiguration();

    // Subscribe to Drive configuration status changes
    this.diagnosticService.driveConfigured$.subscribe(configured => {
      this.isDriveConfigured = configured;
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

  toggleHelp() {
    this.showHelp = !this.showHelp;
  }

  refreshData() {
    // Call API directly to refresh from Drive
    this.api.post('data/refresh-from-drive', {}).subscribe({
      next: (response: any) => {
        console.log('Data refreshed successfully:', response);
        // Trigger event for components to reload
        this.diagnosticService.triggerRefresh();
        // Show success notification
        this.snackbar.success(`Données rafraîchies ! ${response.stats?.campaigns || 0} campagnes importées`);
      },
      error: (err) => {
        console.error('Failed to refresh data:', err);
        this.snackbar.error('Erreur lors du rafraîchissement : ' + (err.error?.detail || err.message));
      }
    });
  }

  private checkDriveConfiguration() {
    this.api.get<any>('data/status').subscribe({
      next: (status) => {
        const isDriveConfigured = !!(status.drive_config?.file_id);
        this.diagnosticService.setDriveConfigured(isDriveConfigured);
      },
      error: (err) => {
        console.log('Could not load data status');
      }
    });
  }
}

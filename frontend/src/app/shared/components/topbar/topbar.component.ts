import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
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
    private authService: AuthService
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

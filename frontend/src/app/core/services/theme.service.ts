import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export type Theme = 'light' | 'dark';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  private readonly THEME_KEY = 'gads_theme';
  private theme$ = new BehaviorSubject<Theme>('light');

  constructor() {
    this.loadTheme();
  }

  getTheme(): Observable<Theme> {
    return this.theme$.asObservable();
  }

  getCurrentTheme(): Theme {
    return this.theme$.value;
  }

  toggleTheme(): void {
    const newTheme: Theme = this.theme$.value === 'light' ? 'dark' : 'light';
    this.setTheme(newTheme);
  }

  setTheme(theme: Theme): void {
    this.theme$.next(theme);
    this.saveTheme(theme);
    this.applyTheme(theme);
  }

  private loadTheme(): void {
    const saved = localStorage.getItem(this.THEME_KEY) as Theme;
    const theme = saved || 'light';
    this.setTheme(theme);
  }

  private saveTheme(theme: Theme): void {
    localStorage.setItem(this.THEME_KEY, theme);
  }

  private applyTheme(theme: Theme): void {
    const body = document.body;

    if (theme === 'dark') {
      body.classList.add('dark');
    } else {
      body.classList.remove('dark');
    }
  }
}

import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject, tap } from 'rxjs';
import { ApiService } from './api.service';

export interface AuthStatus {
  authenticated: boolean;
  customer_id?: string;
  customer_name?: string;
  customer_currency?: string;
}

export interface LoginRequest {
  developer_token: string;
  client_id: string;
  client_secret: string;
  refresh_token: string;
  customer_id: string;
  login_customer_id?: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly TOKEN_KEY = 'gads_token';
  private authStatus$ = new BehaviorSubject<AuthStatus>({ authenticated: false });

  constructor(private api: ApiService) {
    this.checkAuthStatus();
  }

  getAuthStatus(): Observable<AuthStatus> {
    return this.authStatus$.asObservable();
  }

  isAuthenticated(): boolean {
    return this.authStatus$.value.authenticated;
  }

  login(credentials: LoginRequest): Observable<TokenResponse> {
    return this.api.post<TokenResponse>('auth/login', credentials).pipe(
      tap(response => {
        this.saveToken(response.access_token);
        this.checkAuthStatus();
      })
    );
  }

  logout(): Observable<any> {
    return this.api.post('auth/logout', {}).pipe(
      tap(() => {
        this.clearToken();
        this.authStatus$.next({ authenticated: false });
      })
    );
  }

  checkAuthStatus(): void {
    if (!this.getToken()) {
      this.authStatus$.next({ authenticated: false });
      return;
    }

    this.api.get<AuthStatus>('auth/status').subscribe({
      next: (status) => {
        this.authStatus$.next(status);
      },
      error: () => {
        this.authStatus$.next({ authenticated: false });
      }
    });
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  private saveToken(token: string): void {
    localStorage.setItem(this.TOKEN_KEY, token);
  }

  private clearToken(): void {
    localStorage.removeItem(this.TOKEN_KEY);
  }
}

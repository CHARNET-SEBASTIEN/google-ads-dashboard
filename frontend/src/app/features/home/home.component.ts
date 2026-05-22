import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { TranslocoModule } from '@jsverse/transloco';
import { MetricCardComponent } from '../../shared/components/metric-card/metric-card.component';
import { AuthService } from '../../core/services/auth.service';
import { ApiService } from '../../core/services/api.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule, TranslocoModule, MetricCardComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent implements OnInit {
  isAuthenticated = false;
  customerName?: string;

  constructor(
    private authService: AuthService,
    private api: ApiService,
    private router: Router
  ) {}

  ngOnInit() {
    // Check if data exists and redirect accordingly
    this.api.get<{ data_exists: boolean }>('data-import/status').subscribe({
      next: (response) => {
        if (response.data_exists) {
          // Data exists, redirect to campaigns
          this.router.navigate(['/campaigns']);
        } else {
          // No data, redirect to configuration
          this.router.navigate(['/configuration']);
        }
      },
      error: () => {
        // On error, redirect to configuration to be safe
        this.router.navigate(['/configuration']);
      }
    });

    this.authService.getAuthStatus().subscribe(status => {
      this.isAuthenticated = status.authenticated;
      this.customerName = status.customer_name;
    });
  }
}

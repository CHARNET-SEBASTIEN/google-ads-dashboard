import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { TranslocoModule } from '@jsverse/transloco';
import { MetricCardComponent } from '../../shared/components/metric-card/metric-card.component';
import { AuthService } from '../../core/services/auth.service';

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

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.authService.getAuthStatus().subscribe(status => {
      this.isAuthenticated = status.authenticated;
      this.customerName = status.customer_name;
    });
  }
}

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { TranslocoModule } from '@jsverse/transloco';
import { ApiService } from '../../../core/services/api.service';
import { CampaignCardComponent, Campaign } from '../../../shared/components/campaign-card/campaign-card.component';
import { MetricCardComponent } from '../../../shared/components/metric-card/metric-card.component';

interface CampaignsResponse {
  campaigns: Campaign[];
  total: number;
}

@Component({
  selector: 'app-overview',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    TranslocoModule,
    CampaignCardComponent,
    MetricCardComponent
  ],
  templateUrl: './overview.component.html',
  styleUrl: './overview.component.scss'
})
export class OverviewComponent implements OnInit {
  campaigns: Campaign[] = [];
  filteredCampaigns: Campaign[] = [];
  loading = false;

  // Filters
  searchText = '';
  selectedStatus: string[] = [];
  statusOptions = [
    { value: 'ENABLED', label: 'Activées' },
    { value: 'PAUSED', label: 'En pause' },
    { value: 'REMOVED', label: 'Supprimées' }
  ];

  // Stats
  totalCampaigns = 0;
  totalImpressions = 0;
  totalClicks = 0;
  totalCost = 0;

  constructor(
    private api: ApiService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadCampaigns();
  }

  loadCampaigns() {
    this.loading = true;

    const params: any = {};
    if (this.selectedStatus.length > 0) {
      params.status = this.selectedStatus;
    }
    if (this.searchText) {
      params.search = this.searchText;
    }

    this.api.get<CampaignsResponse>('campaigns', params).subscribe({
      next: (response) => {
        this.campaigns = response.campaigns;
        this.filteredCampaigns = response.campaigns;
        this.totalCampaigns = response.total;
        this.calculateStats();
        this.loading = false;
      },
      error: (err) => {
        console.error('Failed to load campaigns:', err);
        this.loading = false;
      }
    });
  }

  calculateStats() {
    this.totalImpressions = this.campaigns.reduce((sum, c) => sum + (c.impressions || 0), 0);
    this.totalClicks = this.campaigns.reduce((sum, c) => sum + (c.clicks || 0), 0);
    this.totalCost = this.campaigns.reduce((sum, c) => sum + (c.cost || 0), 0);
  }

  onSearch() {
    this.loadCampaigns();
  }

  toggleStatus(status: string) {
    const index = this.selectedStatus.indexOf(status);
    if (index > -1) {
      this.selectedStatus.splice(index, 1);
    } else {
      this.selectedStatus.push(status);
    }
    this.loadCampaigns();
  }

  clearFilters() {
    this.searchText = '';
    this.selectedStatus = [];
    this.loadCampaigns();
  }

  onViewCampaignDetails(campaignId: string) {
    this.router.navigate(['/campaign-detail'], { queryParams: { id: campaignId } });
  }

  exportCsv() {
    // TODO: Implement CSV export
    alert('Export CSV : fonctionnalité à venir');
  }
}

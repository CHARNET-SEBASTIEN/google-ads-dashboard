import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { TranslocoModule, TranslocoService } from '@jsverse/transloco';
import { ApiService } from '../../../core/services/api.service';
import { CampaignCardComponent, Campaign } from '../../../shared/components/campaign-card/campaign-card.component';
import { MetricCardComponent } from '../../../shared/components/metric-card/metric-card.component';
import { NumberFormatPipe } from '../../../shared/pipes/number-format.pipe';
import * as XLSX from 'xlsx';

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
    MetricCardComponent,
    NumberFormatPipe
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
  statusOptions: { value: string; label: string }[] = [];

  // Sorting
  sortField: keyof Campaign | '' = '';
  sortDirection: 'asc' | 'desc' = 'asc';

  // Stats
  totalCampaigns = 0;
  totalImpressions = 0;
  totalClicks = 0;
  totalCost = 0;

  constructor(
    private api: ApiService,
    private router: Router,
    private translocoService: TranslocoService
  ) {}

  ngOnInit() {
    // Initialize status options with translations
    this.translocoService.selectTranslate('campaign.enabled_plural').subscribe(label => {
      this.statusOptions = [
        { value: 'ENABLED', label: this.translocoService.translate('campaign.enabled_plural') },
        { value: 'PAUSED', label: this.translocoService.translate('campaign.paused_plural') },
        { value: 'REMOVED', label: this.translocoService.translate('campaign.removed_plural') }
      ];
    });

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
    this.sortField = '';
    this.sortDirection = 'asc';
    this.loadCampaigns();
  }

  onViewCampaignDetails(campaignId: string) {
    this.router.navigate(['/campaign-detail'], { queryParams: { id: campaignId } });
  }

  getStatusKey(status: string): string {
    const upperStatus = status?.toUpperCase() || '';
    const keys: { [key: string]: string } = {
      'ENABLED': 'campaign.enabled',
      'PAUSED': 'campaign.paused',
      'REMOVED': 'campaign.removed'
    };
    return keys[upperStatus] || status;
  }

  sortBy(field: keyof Campaign) {
    if (this.sortField === field) {
      this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortField = field;
      this.sortDirection = 'asc';
    }
    this.applySorting();
  }

  applySorting() {
    if (!this.sortField) return;

    this.filteredCampaigns.sort((a, b) => {
      const aValue = a[this.sortField as keyof Campaign];
      const bValue = b[this.sortField as keyof Campaign];

      if (aValue === null || aValue === undefined) return 1;
      if (bValue === null || bValue === undefined) return -1;

      let comparison = 0;
      if (typeof aValue === 'string' && typeof bValue === 'string') {
        comparison = aValue.localeCompare(bValue);
      } else if (typeof aValue === 'number' && typeof bValue === 'number') {
        comparison = aValue - bValue;
      }

      return this.sortDirection === 'asc' ? comparison : -comparison;
    });
  }

  exportExcel() {
    // Préparer les données pour l'export
    const data = this.filteredCampaigns.map(campaign => ({
      'Nom': campaign.name,
      'Statut': campaign.status,
      'Budget': campaign.budget,
      'Impressions': campaign.impressions || 0,
      'Clics': campaign.clicks || 0,
      'CTR (%)': campaign.ctr ? campaign.ctr.toFixed(2) : '0.00',
      'CPC (€)': campaign.cpc ? campaign.cpc.toFixed(2) : '0.00',
      'Coût (€)': campaign.cost ? campaign.cost.toFixed(2) : '0.00',
      'Conversions': campaign.conversions || 0
    }));

    // Créer un workbook et une worksheet
    const ws: XLSX.WorkSheet = XLSX.utils.json_to_sheet(data);
    const wb: XLSX.WorkBook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Campagnes');

    // Ajuster la largeur des colonnes
    const colWidths = [
      { wch: 40 }, // Nom
      { wch: 12 }, // Statut
      { wch: 12 }, // Budget
      { wch: 15 }, // Impressions
      { wch: 10 }, // Clics
      { wch: 10 }, // CTR
      { wch: 10 }, // CPC
      { wch: 12 }, // Coût
      { wch: 12 }  // Conversions
    ];
    ws['!cols'] = colWidths;

    // Générer et télécharger le fichier
    const fileName = `campaigns_${new Date().toISOString().split('T')[0]}.xlsx`;
    XLSX.writeFile(wb, fileName);
  }
}

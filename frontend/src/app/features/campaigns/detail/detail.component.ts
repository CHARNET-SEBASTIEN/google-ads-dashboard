import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { TranslocoModule } from '@jsverse/transloco';
import { CampaignService, Keyword, Ad, Performance } from '../../../core/services/campaign.service';
import { Campaign } from '../../../shared/components/campaign-card/campaign-card.component';
import { MetricCardComponent } from '../../../shared/components/metric-card/metric-card.component';
import { ChartComponent, ChartData, ChartLayout } from '../../../shared/components/chart/chart.component';
import { NumberFormatPipe } from '../../../shared/pipes/number-format.pipe';
import * as XLSX from 'xlsx';

@Component({
  selector: 'app-detail',
  standalone: true,
  imports: [CommonModule, TranslocoModule, MetricCardComponent, ChartComponent, NumberFormatPipe],
  templateUrl: './detail.component.html',
  styleUrl: './detail.component.scss'
})
export class DetailComponent implements OnInit {
  campaignId: string | null = null;
  campaign: Campaign | null = null;
  keywords: Keyword[] = [];
  ads: Ad[] = [];
  performance: Performance[] = [];

  activeTab: 'overview' | 'keywords' | 'ads' | 'performance' = 'overview';
  loading = false;

  // Sorting for keywords
  sortField: keyof Keyword | '' = '';
  sortDirection: 'asc' | 'desc' = 'asc';

  // Chart data
  performanceChartData: ChartData[] = [];
  performanceChartLayout: ChartLayout = {
    title: 'Performance au fil du temps',
    height: 400,
    showlegend: true
  };

  constructor(
    private route: ActivatedRoute,
    private campaignService: CampaignService
  ) {}

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      this.campaignId = params['id'];
      if (this.campaignId) {
        this.loadCampaign();
        this.loadKeywords();
        this.loadAds();
      }
    });
  }

  loadCampaign() {
    if (!this.campaignId) return;

    this.loading = true;
    this.campaignService.getCampaign(this.campaignId).subscribe({
      next: (campaign) => {
        this.campaign = campaign;
        this.loading = false;
      },
      error: (err) => {
        console.error('Failed to load campaign:', err);
        this.loading = false;
      }
    });
  }

  loadKeywords() {
    if (!this.campaignId) return;

    this.campaignService.getCampaignKeywords(this.campaignId).subscribe({
      next: (response) => {
        this.keywords = response.keywords;
      },
      error: (err) => {
        console.error('Failed to load keywords:', err);
      }
    });
  }

  loadAds() {
    if (!this.campaignId) return;

    this.campaignService.getCampaignAds(this.campaignId).subscribe({
      next: (response) => {
        this.ads = response.ads;
      },
      error: (err) => {
        console.error('Failed to load ads:', err);
      }
    });
  }

  loadPerformance() {
    if (!this.campaignId || this.performance.length > 0) return;

    this.campaignService.getCampaignPerformance(this.campaignId).subscribe({
      next: (response) => {
        this.performance = response.performance;
        this.prepareChartData();
      },
      error: (err) => {
        console.error('Failed to load performance:', err);
      }
    });
  }

  prepareChartData() {
    if (this.performance.length === 0) return;

    const dates = this.performance.map(p => p.date);
    const impressions = this.performance.map(p => p.impressions);
    const clicks = this.performance.map(p => p.clicks);
    const conversions = this.performance.map(p => p.conversions);
    const cost = this.performance.map(p => p.cost);

    this.performanceChartData = [
      {
        x: dates,
        y: impressions,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Impressions',
        line: { color: '#3B82F6', width: 2 },
        marker: { size: 6 }
      },
      {
        x: dates,
        y: clicks,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Clics',
        line: { color: '#10B981', width: 2 },
        marker: { size: 6 }
      },
      {
        x: dates,
        y: conversions,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Conversions',
        line: { color: '#F59E0B', width: 2 },
        marker: { size: 6 },
        yaxis: 'y2'
      }
    ];

    this.performanceChartLayout = {
      title: 'Performance au fil du temps',
      height: 400,
      showlegend: true,
      yaxis: {
        title: 'Impressions / Clics'
      },
      yaxis2: {
        title: 'Conversions',
        overlaying: 'y',
        side: 'right'
      }
    };
  }

  setActiveTab(tab: 'overview' | 'keywords' | 'ads' | 'performance') {
    this.activeTab = tab;

    if (tab === 'performance' && this.performance.length === 0) {
      this.loadPerformance();
    }
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

  getMatchTypeKey(type: string): string {
    const keys: { [key: string]: string } = {
      'EXACT': 'detail.match_exact',
      'PHRASE': 'detail.match_phrase',
      'BROAD': 'detail.match_broad'
    };
    return keys[type] || type;
  }

  getAdTypeKey(type: string): string {
    const keys: { [key: string]: string } = {
      'RESPONSIVE_SEARCH_AD': 'detail.ad_rsa',
      'EXPANDED_TEXT_AD': 'detail.ad_eta',
      'TEXT_AD': 'detail.ad_text',
      'UNKNOWN': 'detail.ad_unknown'
    };
    return keys[type] || type;
  }

  sortBy(field: keyof Keyword) {
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

    this.keywords.sort((a, b) => {
      const aValue = a[this.sortField as keyof Keyword];
      const bValue = b[this.sortField as keyof Keyword];

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

  exportKeywordsExcel() {
    const data = this.keywords.map(keyword => ({
      'Mot-clé': keyword.text || 'N/A',
      'Type': keyword.match_type || 'N/A',
      'Statut': keyword.status || 'N/A',
      'Impressions': keyword.impressions || 0,
      'Clics': keyword.clicks || 0,
      'CTR (%)': keyword.ctr ? keyword.ctr.toFixed(2) : '0.00',
      'Coût (€)': keyword.cost ? keyword.cost.toFixed(2) : '0.00'
    }));

    const ws: XLSX.WorkSheet = XLSX.utils.json_to_sheet(data);
    const wb: XLSX.WorkBook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Mots-clés');

    const colWidths = [
      { wch: 40 }, // Mot-clé
      { wch: 15 }, // Type
      { wch: 12 }, // Statut
      { wch: 15 }, // Impressions
      { wch: 10 }, // Clics
      { wch: 10 }, // CTR
      { wch: 12 }  // Coût
    ];
    ws['!cols'] = colWidths;

    const fileName = `keywords_${this.campaign?.name || 'campaign'}_${new Date().toISOString().split('T')[0]}.xlsx`;
    XLSX.writeFile(wb, fileName);
  }
}

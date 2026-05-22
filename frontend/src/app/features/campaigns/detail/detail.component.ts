import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { TranslocoModule } from '@jsverse/transloco';
import { CampaignService, Keyword, Ad, Performance } from '../../../core/services/campaign.service';
import { Campaign } from '../../../shared/components/campaign-card/campaign-card.component';
import { MetricCardComponent } from '../../../shared/components/metric-card/metric-card.component';
import { ChartComponent, ChartData, ChartLayout } from '../../../shared/components/chart/chart.component';

@Component({
  selector: 'app-detail',
  standalone: true,
  imports: [CommonModule, TranslocoModule, MetricCardComponent, ChartComponent],
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

  getStatusLabel(status: string): string {
    const upperStatus = status?.toUpperCase() || '';
    const labels: { [key: string]: string } = {
      'ENABLED': 'Activée',
      'PAUSED': 'En pause',
      'REMOVED': 'Supprimée'
    };
    return labels[upperStatus] || status;
  }

  getMatchTypeLabel(type: string): string {
    const labels: { [key: string]: string } = {
      'EXACT': 'Exact',
      'PHRASE': 'Expression',
      'BROAD': 'Large'
    };
    return labels[type] || type;
  }

  getAdTypeLabel(type: string): string {
    const labels: { [key: string]: string } = {
      'RESPONSIVE_SEARCH_AD': 'Annonce adaptative',
      'EXPANDED_TEXT_AD': 'Annonce textuelle',
      'TEXT_AD': 'Annonce texte',
      'UNKNOWN': 'Type inconnu'
    };
    return labels[type] || type;
  }
}

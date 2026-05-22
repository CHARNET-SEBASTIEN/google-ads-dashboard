import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { TranslocoModule } from '@jsverse/transloco';
import { CampaignService, Keyword, Ad, Performance } from '../../../core/services/campaign.service';
import { Campaign } from '../../../shared/components/campaign-card/campaign-card.component';
import { MetricCardComponent } from '../../../shared/components/metric-card/metric-card.component';

@Component({
  selector: 'app-detail',
  standalone: true,
  imports: [CommonModule, TranslocoModule, MetricCardComponent],
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
      },
      error: (err) => {
        console.error('Failed to load performance:', err);
      }
    });
  }

  setActiveTab(tab: 'overview' | 'keywords' | 'ads' | 'performance') {
    this.activeTab = tab;

    if (tab === 'performance' && this.performance.length === 0) {
      this.loadPerformance();
    }
  }

  getStatusLabel(status: string): string {
    const labels: { [key: string]: string } = {
      'ENABLED': 'Activée',
      'PAUSED': 'En pause',
      'REMOVED': 'Supprimée'
    };
    return labels[status] || status;
  }

  getMatchTypeLabel(type: string): string {
    const labels: { [key: string]: string } = {
      'EXACT': 'Exact',
      'PHRASE': 'Expression',
      'BROAD': 'Large'
    };
    return labels[type] || type;
  }
}

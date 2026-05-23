import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { TranslocoModule } from '@jsverse/transloco';
import { CampaignService, Keyword, Ad, Performance, DevicePerformance, DayOfWeekPerformance } from '../../../core/services/campaign.service';
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

  activeTab: 'overview' | 'keywords' | 'ads' | 'performance' | 'analytics' = 'overview';
  loading = false;

  // Analytics data
  devicePerformance: DevicePerformance[] = [];
  dayOfWeekPerformance: DayOfWeekPerformance[] = [];
  deviceChartData: ChartData[] = [];
  dayOfWeekChartData: ChartData[] = [];

  // Sorting for device
  sortFieldDevice: keyof DevicePerformance | '' = '';
  sortDirectionDevice: 'asc' | 'desc' = 'asc';

  // Sorting for day of week
  sortFieldDay: keyof DayOfWeekPerformance | '' = '';
  sortDirectionDay: 'asc' | 'desc' = 'asc';

  // Sorting for keywords
  sortField: keyof Keyword | '' = '';
  sortDirection: 'asc' | 'desc' = 'asc';

  // Sorting for performance
  sortFieldPerf: keyof Performance | '' = 'date';
  sortDirectionPerf: 'asc' | 'desc' = 'desc';

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
        // Calculate CTR and CPC for each performance entry
        this.performance = response.performance.map(p => ({
          ...p,
          ctr: p.impressions > 0 ? (p.clicks / p.impressions) * 100 : 0,
          cpc: p.clicks > 0 ? p.cost / p.clicks : 0
        }));
        this.applyPerformanceSorting();
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
    const ctr = this.performance.map(p => p.ctr || 0);
    const cost = this.performance.map(p => p.cost);

    // Use brighter colors that work better in dark mode
    this.performanceChartData = [
      {
        x: dates,
        y: impressions,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Impressions',
        line: { color: '#60A5FA', width: 2 },
        marker: { size: 6, color: '#60A5FA' }
      },
      {
        x: dates,
        y: clicks,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Clics',
        line: { color: '#34D399', width: 2 },
        marker: { size: 6, color: '#34D399' }
      },
      {
        x: dates,
        y: ctr,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'CTR (%)',
        line: { color: '#F97316', width: 2 },
        marker: { size: 6, color: '#F97316' },
        yaxis: 'y2'
      },
      {
        x: dates,
        y: conversions,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Conversions',
        line: { color: '#FBBF24', width: 2 },
        marker: { size: 6, color: '#FBBF24' },
        yaxis: 'y3'
      }
    ];

    this.performanceChartLayout = {
      title: 'Performance au fil du temps',
      height: 450,
      showlegend: true,
      yaxis: {
        title: 'Impressions / Clics',
        gridcolor: 'rgba(148, 163, 184, 0.2)',
        zerolinecolor: 'rgba(148, 163, 184, 0.3)'
      },
      yaxis2: {
        title: 'CTR (%)',
        overlaying: 'y',
        side: 'right',
        gridcolor: 'rgba(148, 163, 184, 0.1)',
        zerolinecolor: 'rgba(148, 163, 184, 0.3)'
      },
      yaxis3: {
        title: 'Conversions',
        anchor: 'free',
        overlaying: 'y',
        side: 'right',
        position: 0.95,
        gridcolor: 'rgba(148, 163, 184, 0.05)',
        zerolinecolor: 'rgba(148, 163, 184, 0.3)'
      }
    };
  }

  setActiveTab(tab: 'overview' | 'keywords' | 'ads' | 'performance' | 'analytics') {
    this.activeTab = tab;

    if (tab === 'performance' && this.performance.length === 0) {
      this.loadPerformance();
    }

    if (tab === 'analytics' && this.devicePerformance.length === 0) {
      this.loadAnalytics();
    }
  }

  loadAnalytics() {
    if (!this.campaignId) return;

    // Load device performance
    this.campaignService.getCampaignPerformanceByDevice(this.campaignId).subscribe({
      next: (response) => {
        this.devicePerformance = response.devices;
        this.prepareDeviceChart();
      },
      error: (err) => {
        console.error('Failed to load device performance:', err);
      }
    });

    // Load day of week performance
    this.campaignService.getCampaignPerformanceByDayOfWeek(this.campaignId).subscribe({
      next: (response) => {
        this.dayOfWeekPerformance = response.days;
        this.prepareDayOfWeekChart();
      },
      error: (err) => {
        console.error('Failed to load day of week performance:', err);
      }
    });
  }

  prepareDeviceChart() {
    if (this.devicePerformance.length === 0) return;

    const devices = this.devicePerformance.map(d => d.device);
    const impressions = this.devicePerformance.map(d => d.impressions);
    const clicks = this.devicePerformance.map(d => d.clicks);
    const conversions = this.devicePerformance.map(d => d.conversions);

    this.deviceChartData = [
      {
        x: devices,
        y: impressions,
        type: 'bar',
        name: 'Impressions',
        marker: { color: '#60A5FA' }
      },
      {
        x: devices,
        y: clicks,
        type: 'bar',
        name: 'Clics',
        marker: { color: '#34D399' }
      },
      {
        x: devices,
        y: conversions,
        type: 'bar',
        name: 'Conversions',
        marker: { color: '#FBBF24' },
        yaxis: 'y2'
      }
    ];
  }

  prepareDayOfWeekChart() {
    if (this.dayOfWeekPerformance.length === 0) return;

    const days = this.dayOfWeekPerformance.map(d => d.day_of_week);
    const impressions = this.dayOfWeekPerformance.map(d => d.impressions);
    const clicks = this.dayOfWeekPerformance.map(d => d.clicks);
    const ctr = this.dayOfWeekPerformance.map(d => d.ctr);

    this.dayOfWeekChartData = [
      {
        x: days,
        y: impressions,
        type: 'bar',
        name: 'Impressions',
        marker: { color: '#60A5FA' }
      },
      {
        x: days,
        y: clicks,
        type: 'bar',
        name: 'Clics',
        marker: { color: '#34D399' }
      },
      {
        x: days,
        y: ctr,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'CTR (%)',
        line: { color: '#F97316', width: 3 },
        marker: { size: 8, color: '#F97316' },
        yaxis: 'y2'
      }
    ];
  }

  exportDeviceExcel() {
    const data = this.devicePerformance.map(device => ({
      'Appareil': device.device,
      'Impressions': device.impressions,
      'Clics': device.clicks,
      'CTR (%)': device.ctr.toFixed(2),
      'CPC (€)': device.cpc.toFixed(2),
      'Coût (€)': device.cost.toFixed(2),
      'Conversions': device.conversions.toFixed(1)
    }));

    const ws: XLSX.WorkSheet = XLSX.utils.json_to_sheet(data);
    const wb: XLSX.WorkBook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Par Appareil');

    const fileName = `device_${this.campaign?.name || 'campaign'}_${new Date().toISOString().split('T')[0]}.xlsx`;
    XLSX.writeFile(wb, fileName);
  }

  exportDayOfWeekExcel() {
    const data = this.dayOfWeekPerformance.map(day => ({
      'Jour': day.day_of_week,
      'Impressions': day.impressions,
      'Clics': day.clicks,
      'CTR (%)': day.ctr.toFixed(2),
      'CPC (€)': day.cpc.toFixed(2),
      'Coût (€)': day.cost.toFixed(2),
      'Conversions': day.conversions.toFixed(1)
    }));

    const ws: XLSX.WorkSheet = XLSX.utils.json_to_sheet(data);
    const wb: XLSX.WorkBook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Par Jour');

    const fileName = `day_of_week_${this.campaign?.name || 'campaign'}_${new Date().toISOString().split('T')[0]}.xlsx`;
    XLSX.writeFile(wb, fileName);
  }

  sortDeviceBy(field: keyof DevicePerformance) {
    if (this.sortFieldDevice === field) {
      this.sortDirectionDevice = this.sortDirectionDevice === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortFieldDevice = field;
      this.sortDirectionDevice = 'asc';
    }
    this.applyDeviceSorting();
  }

  applyDeviceSorting() {
    if (!this.sortFieldDevice) return;

    this.devicePerformance.sort((a, b) => {
      const aValue = a[this.sortFieldDevice as keyof DevicePerformance];
      const bValue = b[this.sortFieldDevice as keyof DevicePerformance];

      if (aValue === null || aValue === undefined) return 1;
      if (bValue === null || bValue === undefined) return -1;

      let comparison = 0;
      if (typeof aValue === 'string' && typeof bValue === 'string') {
        comparison = aValue.localeCompare(bValue);
      } else if (typeof aValue === 'number' && typeof bValue === 'number') {
        comparison = aValue - bValue;
      }

      return this.sortDirectionDevice === 'asc' ? comparison : -comparison;
    });
  }

  sortDayBy(field: keyof DayOfWeekPerformance) {
    if (this.sortFieldDay === field) {
      this.sortDirectionDay = this.sortDirectionDay === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortFieldDay = field;
      this.sortDirectionDay = 'asc';
    }
    this.applyDaySorting();
  }

  applyDaySorting() {
    if (!this.sortFieldDay) return;

    this.dayOfWeekPerformance.sort((a, b) => {
      const aValue = a[this.sortFieldDay as keyof DayOfWeekPerformance];
      const bValue = b[this.sortFieldDay as keyof DayOfWeekPerformance];

      if (aValue === null || aValue === undefined) return 1;
      if (bValue === null || bValue === undefined) return -1;

      let comparison = 0;
      if (typeof aValue === 'string' && typeof bValue === 'string') {
        comparison = aValue.localeCompare(bValue);
      } else if (typeof aValue === 'number' && typeof bValue === 'number') {
        comparison = aValue - bValue;
      }

      return this.sortDirectionDay === 'asc' ? comparison : -comparison;
    });
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

  sortPerformanceBy(field: keyof Performance) {
    if (this.sortFieldPerf === field) {
      this.sortDirectionPerf = this.sortDirectionPerf === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortFieldPerf = field;
      this.sortDirectionPerf = 'asc';
    }
    this.applyPerformanceSorting();
  }

  applyPerformanceSorting() {
    if (!this.sortFieldPerf) return;

    this.performance.sort((a, b) => {
      const aValue = a[this.sortFieldPerf as keyof Performance];
      const bValue = b[this.sortFieldPerf as keyof Performance];

      if (aValue === null || aValue === undefined) return 1;
      if (bValue === null || bValue === undefined) return -1;

      let comparison = 0;
      if (typeof aValue === 'string' && typeof bValue === 'string') {
        comparison = aValue.localeCompare(bValue);
      } else if (typeof aValue === 'number' && typeof bValue === 'number') {
        comparison = aValue - bValue;
      }

      return this.sortDirectionPerf === 'asc' ? comparison : -comparison;
    });
  }

  exportPerformanceExcel() {
    const data = this.performance.map(perf => ({
      'Date': perf.date || 'N/A',
      'Impressions': perf.impressions || 0,
      'Clics': perf.clicks || 0,
      'CTR (%)': perf.ctr ? perf.ctr.toFixed(2) : '0.00',
      'CPC (€)': perf.cpc ? perf.cpc.toFixed(2) : '0.00',
      'Coût (€)': perf.cost ? perf.cost.toFixed(2) : '0.00',
      'Conversions': perf.conversions ? perf.conversions.toFixed(1) : '0.0'
    }));

    const ws: XLSX.WorkSheet = XLSX.utils.json_to_sheet(data);
    const wb: XLSX.WorkBook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Performance');

    const colWidths = [
      { wch: 12 }, // Date
      { wch: 15 }, // Impressions
      { wch: 12 }, // Clics
      { wch: 12 }, // CTR
      { wch: 12 }, // CPC
      { wch: 12 }, // Coût
      { wch: 15 }  // Conversions
    ];
    ws['!cols'] = colWidths;

    const fileName = `performance_${this.campaign?.name || 'campaign'}_${new Date().toISOString().split('T')[0]}.xlsx`;
    XLSX.writeFile(wb, fileName);
  }
}

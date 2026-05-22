import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslocoModule } from '@jsverse/transloco';

export interface Campaign {
  id: string;
  name: string;
  status: string;
  budget?: number;
  impressions?: number;
  clicks?: number;
  ctr?: number;
  cpc?: number;
  cost?: number;
  conversions?: number;
}

@Component({
  selector: 'app-campaign-card',
  standalone: true,
  imports: [CommonModule, TranslocoModule],
  templateUrl: './campaign-card.component.html',
  styleUrl: './campaign-card.component.scss'
})
export class CampaignCardComponent {
  @Input() campaign!: Campaign;
  @Output() viewDetails = new EventEmitter<string>();

  getStatusClass(status: string): string {
    const statusMap: { [key: string]: string } = {
      'ENABLED': 'status-enabled',
      'PAUSED': 'status-paused',
      'REMOVED': 'status-removed'
    };
    return statusMap[status] || 'status-unknown';
  }

  getStatusKey(status: string): string {
    const keyMap: { [key: string]: string } = {
      'ENABLED': 'campaign.enabled',
      'PAUSED': 'campaign.paused',
      'REMOVED': 'campaign.removed'
    };
    return keyMap[status] || status;
  }

  onViewDetails() {
    this.viewDetails.emit(this.campaign.id);
  }
}

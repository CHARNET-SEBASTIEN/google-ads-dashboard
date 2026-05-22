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

  getStatusLabel(status: string): string {
    const labelMap: { [key: string]: string } = {
      'ENABLED': 'Activée',
      'PAUSED': 'En pause',
      'REMOVED': 'Supprimée'
    };
    return labelMap[status] || status;
  }

  onViewDetails() {
    this.viewDetails.emit(this.campaign.id);
  }
}

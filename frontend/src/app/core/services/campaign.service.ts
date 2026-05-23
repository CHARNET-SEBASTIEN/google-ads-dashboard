import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { Campaign } from '../../shared/components/campaign-card/campaign-card.component';

export interface Keyword {
  id: string;
  campaign_id: string;
  text: string;
  match_type: string;
  status: string;
  impressions: number;
  clicks: number;
  ctr: number;
  cpc: number;
  cost: number;
}

export interface Ad {
  id: string;
  campaign_id: string;
  type: string;
  status: string;
  headline1?: string;
  headline2?: string;
  description?: string;
  impressions: number;
  clicks: number;
}

export interface Performance {
  date: string;
  impressions: number;
  clicks: number;
  cost: number;
  conversions: number;
  ctr?: number;
  cpc?: number;
}

@Injectable({
  providedIn: 'root'
})
export class CampaignService {

  constructor(private api: ApiService) { }

  getCampaigns(params?: any): Observable<{ campaigns: Campaign[], total: number }> {
    return this.api.get('campaigns', params);
  }

  getCampaign(id: string): Observable<Campaign> {
    return this.api.get(`campaigns/${id}`);
  }

  getCampaignKeywords(id: string, params?: any): Observable<{ keywords: Keyword[], total: number }> {
    return this.api.get(`campaigns/${id}/keywords`, params);
  }

  getCampaignAds(id: string): Observable<{ ads: Ad[], total: number }> {
    return this.api.get(`campaigns/${id}/ads`);
  }

  getCampaignPerformance(id: string, params?: any): Observable<{ performance: Performance[] }> {
    return this.api.get(`campaigns/${id}/performance`, params);
  }
}

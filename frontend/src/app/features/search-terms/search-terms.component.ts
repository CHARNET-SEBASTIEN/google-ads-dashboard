import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TranslocoModule } from '@jsverse/transloco';
import { ApiService } from '../../core/services/api.service';

interface SearchTerm {
  id: string;
  campaign_id: string;
  campaign_name?: string;
  query: string;
  impressions: number;
  clicks: number;
  ctr: number;
  cost: number;
  conversions: number;
  is_suspect: boolean;
}

@Component({
  selector: 'app-search-terms',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslocoModule],
  templateUrl: './search-terms.component.html',
  styleUrl: './search-terms.component.scss'
})
export class SearchTermsComponent implements OnInit {
  searchTerms: SearchTerm[] = [];
  loading = false;
  searchText = '';
  showOnlySuspects = false;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadSearchTerms();
  }

  loadSearchTerms() {
    this.loading = true;

    const endpoint = this.showOnlySuspects ? 'search-terms/suspects' : 'search-terms';
    const params: any = {};

    if (this.searchText && !this.showOnlySuspects) {
      params.search = this.searchText;
    }

    this.api.get<any>(endpoint, params).subscribe({
      next: (response) => {
        this.searchTerms = this.showOnlySuspects ? response.suspects : response.search_terms;
        this.loading = false;
      },
      error: (err) => {
        console.error('Failed to load search terms:', err);
        this.loading = false;
      }
    });
  }

  toggleSuspects() {
    this.showOnlySuspects = !this.showOnlySuspects;
    this.loadSearchTerms();
  }

  exportCsv() {
    window.open('http://localhost:8000/api/search-terms/export', '_blank');
  }
}

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TranslocoModule } from '@jsverse/transloco';
import { ApiService } from '../../core/services/api.service';
import { NumberFormatPipe } from '../../shared/pipes/number-format.pipe';
import * as XLSX from 'xlsx';

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
  imports: [CommonModule, FormsModule, TranslocoModule, NumberFormatPipe],
  templateUrl: './search-terms.component.html',
  styleUrl: './search-terms.component.scss'
})
export class SearchTermsComponent implements OnInit {
  searchTerms: SearchTerm[] = [];
  loading = false;
  searchText = '';
  showOnlySuspects = false;

  // Sorting
  sortField: keyof SearchTerm | '' = '';
  sortDirection: 'asc' | 'desc' = 'asc';

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

  sortBy(field: keyof SearchTerm) {
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

    this.searchTerms.sort((a, b) => {
      const aValue = a[this.sortField as keyof SearchTerm];
      const bValue = b[this.sortField as keyof SearchTerm];

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
    const data = this.searchTerms.map(term => ({
      'Requête': term.query,
      'Campagne': term.campaign_name || 'N/A',
      'Impressions': term.impressions || 0,
      'Clics': term.clicks || 0,
      'CTR (%)': term.ctr ? term.ctr.toFixed(2) : '0.00',
      'Coût (€)': term.cost ? term.cost.toFixed(2) : '0.00',
      'Conversions': term.conversions || 0,
      'Suspect': term.is_suspect ? 'Oui' : 'Non'
    }));

    const ws: XLSX.WorkSheet = XLSX.utils.json_to_sheet(data);
    const wb: XLSX.WorkBook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Termes de recherche');

    const colWidths = [
      { wch: 50 }, // Requête
      { wch: 30 }, // Campagne
      { wch: 15 }, // Impressions
      { wch: 10 }, // Clics
      { wch: 10 }, // CTR
      { wch: 12 }, // Coût
      { wch: 12 }, // Conversions
      { wch: 10 }  // Suspect
    ];
    ws['!cols'] = colWidths;

    const fileName = `search_terms_${new Date().toISOString().split('T')[0]}.xlsx`;
    XLSX.writeFile(wb, fileName);
  }
}

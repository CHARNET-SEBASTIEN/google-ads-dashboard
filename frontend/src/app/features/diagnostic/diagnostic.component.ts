import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { TranslocoModule } from '@jsverse/transloco';
import { ApiService } from '../../core/services/api.service';
import { MetricCardComponent } from '../../shared/components/metric-card/metric-card.component';

interface DiagnosticIssue {
  id: string;
  campaign_id: string;
  campaign_name: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  category: string;
  title: string;
  message: string;
  recommendation?: string;
  impact?: string;
  created_at: string;
}

interface DiagnosticResponse {
  issues: DiagnosticIssue[];
  summary: {
    total: number;
    by_severity: {
      critical: number;
      high: number;
      medium: number;
      low: number;
    };
    by_category: { [key: string]: number };
  };
}

@Component({
  selector: 'app-diagnostic',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule, TranslocoModule, MetricCardComponent],
  templateUrl: './diagnostic.component.html',
  styleUrl: './diagnostic.component.scss'
})
export class DiagnosticComponent implements OnInit {
  issues: DiagnosticIssue[] = [];
  loading = false;
  
  // Filters
  selectedSeverities: string[] = [];
  selectedCategories: string[] = [];
  
  severityOptions = [
    { value: 'critical', label: 'Critique', color: '#EF4444' },
    { value: 'high', label: 'Élevé', color: '#F97316' },
    { value: 'medium', label: 'Moyen', color: '#EAB308' },
    { value: 'low', label: 'Faible', color: '#3B82F6' }
  ];
  
  categoryOptions: { value: string; label: string }[] = [];
  
  // Summary
  totalIssues = 0;
  criticalCount = 0;
  highCount = 0;
  mediumCount = 0;
  lowCount = 0;
  
  expandedIssues = new Set<string>();

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadDiagnostics();
  }

  loadDiagnostics() {
    this.loading = true;

    const params: any = {};
    if (this.selectedSeverities.length > 0) {
      params.severity = this.selectedSeverities;
    }
    if (this.selectedCategories.length > 0) {
      params.category = this.selectedCategories;
    }

    this.api.get<DiagnosticResponse>('diagnostics', params).subscribe({
      next: (response) => {
        this.issues = response.issues;
        this.totalIssues = response.summary.total;
        this.criticalCount = response.summary.by_severity.critical;
        this.highCount = response.summary.by_severity.high;
        this.mediumCount = response.summary.by_severity.medium;
        this.lowCount = response.summary.by_severity.low;
        
        // Build category options from response
        this.categoryOptions = Object.keys(response.summary.by_category).map(cat => ({
          value: cat,
          label: this.getCategoryLabel(cat)
        }));
        
        this.loading = false;
      },
      error: (err) => {
        console.error('Failed to load diagnostics:', err);
        this.loading = false;
      }
    });
  }

  toggleSeverity(severity: string) {
    const index = this.selectedSeverities.indexOf(severity);
    if (index > -1) {
      this.selectedSeverities.splice(index, 1);
    } else {
      this.selectedSeverities.push(severity);
    }
    this.loadDiagnostics();
  }

  toggleCategory(category: string) {
    const index = this.selectedCategories.indexOf(category);
    if (index > -1) {
      this.selectedCategories.splice(index, 1);
    } else {
      this.selectedCategories.push(category);
    }
    this.loadDiagnostics();
  }

  clearFilters() {
    this.selectedSeverities = [];
    this.selectedCategories = [];
    this.loadDiagnostics();
  }

  toggleIssue(issueId: string) {
    if (this.expandedIssues.has(issueId)) {
      this.expandedIssues.delete(issueId);
    } else {
      this.expandedIssues.add(issueId);
    }
  }

  isExpanded(issueId: string): boolean {
    return this.expandedIssues.has(issueId);
  }

  getSeverityClass(severity: string): string {
    const classMap: { [key: string]: string } = {
      'critical': 'severity-critical',
      'high': 'severity-high',
      'medium': 'severity-medium',
      'low': 'severity-low'
    };
    return classMap[severity] || 'severity-low';
  }

  getSeverityLabel(severity: string): string {
    const labelMap: { [key: string]: string } = {
      'critical': 'Critique',
      'high': 'Élevé',
      'medium': 'Moyen',
      'low': 'Faible'
    };
    return labelMap[severity] || severity;
  }

  getCategoryLabel(category: string): string {
    const labelMap: { [key: string]: string } = {
      'budget': 'Budget',
      'performance': 'Performance',
      'configuration': 'Configuration',
      'optimization': 'Optimisation',
      'status': 'Statut'
    };
    return labelMap[category] || category;
  }

  exportCsv() {
    window.open('http://localhost:8000/api/diagnostics/export', '_blank');
  }

  runDiagnostics() {
    this.loading = true;
    this.api.post<DiagnosticResponse>('diagnostics/run', {}).subscribe({
      next: (response) => {
        this.loadDiagnostics();
      },
      error: (err) => {
        console.error('Failed to run diagnostics:', err);
        this.loading = false;
      }
    });
  }
}

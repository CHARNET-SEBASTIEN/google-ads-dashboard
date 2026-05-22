import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { TranslocoService, TranslocoModule } from '@jsverse/transloco';
import { ApiService } from '../../core/services/api.service';
import { marked } from 'marked';
import * as XLSX from 'xlsx';

interface Recommendation {
  campaign: string;
  issue: string;
  severity: string;
  impact: string;
  recommendation: string;
}

@Component({
  selector: 'app-diagnostic',
  standalone: true,
  imports: [CommonModule, TranslocoModule],
  templateUrl: './diagnostic.component.html',
  styleUrl: './diagnostic.component.scss'
})
export class DiagnosticComponent implements OnInit {
  // AI Analysis
  loadingAi = false;
  aiAnalysis: string | null = null;
  aiError: string | null = null;

  // Recommendations table
  recommendations: Recommendation[] = [];
  sortField: keyof Recommendation | '' = '';
  sortDirection: 'asc' | 'desc' = 'asc';

  // Main view toggle
  mainView: 'report' | 'schedule' = 'report';

  // Report sub-view (table or markdown)
  reportView: 'table' | 'markdown' = 'table';

  // Checklist state (persisted in localStorage)
  completedTasks: Set<number> = new Set();

  private translocoService = inject(TranslocoService);
  private sanitizer = inject(DomSanitizer);

  constructor(private api: ApiService) {
    // Configure marked options for better rendering
    marked.setOptions({
      breaks: true,
      gfm: true
    });
  }

  ngOnInit() {
    // Charger l'analyse en cache si disponible
    this.loadCachedAnalysis();

    // Load completed tasks from localStorage
    this.loadCompletedTasks();
  }

  loadCachedAnalysis() {
    this.api.get<{ success: boolean; analysis?: string; timestamp?: string }>('diagnostics/ai-analysis/cached').subscribe({
      next: (response) => {
        if (response.success && response.analysis) {
          this.aiAnalysis = response.analysis;
          this.parseRecommendations();
        }
      },
      error: (err) => {
        // Pas de cache disponible, c'est normal
        console.log('No cached analysis available');
      }
    });
  }

  runAiAnalysis() {
    this.loadingAi = true;
    this.aiError = null;
    this.aiAnalysis = null;

    // Récupérer la langue active
    const currentLang = this.translocoService.getActiveLang();

    this.api.post<{ success: boolean; analysis?: string; error?: string }>(
      `diagnostics/ai-analysis?language=${currentLang}`,
      {}
    ).subscribe({
      next: (response) => {
        this.loadingAi = false;
        if (response.success && response.analysis) {
          this.aiAnalysis = response.analysis;
          this.parseRecommendations();
        } else {
          this.aiError = response.error || 'Erreur lors de l\'analyse IA';
        }
      },
      error: (err) => {
        console.error('Failed to run AI analysis:', err);
        this.loadingAi = false;
        this.aiError = err.error?.message || err.error?.detail || 'Erreur lors de l\'analyse IA. Vérifiez que la clé API Anthropic est configurée dans le backend.';
      }
    });
  }

  downloadAiReport() {
    if (!this.aiAnalysis) return;

    const blob = new Blob([this.aiAnalysis], { type: 'text/markdown;charset=utf-8' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `diagnostic-ia-${new Date().toISOString().split('T')[0]}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }

  getFormattedAnalysis(): SafeHtml {
    if (!this.aiAnalysis) return '';

    try {
      const html = marked.parse(this.aiAnalysis);
      return this.sanitizer.sanitize(1, html) || '';
    } catch (error) {
      console.error('Error parsing markdown:', error);
      return this.aiAnalysis;
    }
  }

  parseRecommendations() {
    if (!this.aiAnalysis) {
      this.recommendations = [];
      return;
    }

    console.log('=== PARSING AI ANALYSIS ===');
    console.log('First 500 chars:', this.aiAnalysis.substring(0, 500));

    const recommendations: Recommendation[] = [];

    // Split by campaign sections (### headers for campaigns)
    const campaignSections = this.aiAnalysis.split(/^###\s+/m).filter(s => s.trim());
    console.log('Found campaign sections:', campaignSections.length);

    for (const section of campaignSections) {
      console.log('--- Raw section ---');
      console.log(section.substring(0, 300));
      console.log('--- End raw section ---');

      const lines = section.split('\n').map(l => l.trim()).filter(l => l);
      if (lines.length === 0) continue;

      // First line is campaign name
      let campaignName = lines[0].replace(/[*_#\[\]]/g, '').trim();
      console.log('Processing campaign:', campaignName);

      // Skip if this is not a campaign section
      if (campaignName.match(/résumé|summary|zusammenfassung|conclusion|actions|opportunités|opportunities/i)) {
        console.log('Skipping non-campaign section:', campaignName);
        continue;
      }

      let currentSeverity = 'Medium';
      let issueText = '';
      let impactText = '';
      let recommendationText = '';
      let currentSection = '';

      console.log(`  → Parsing ${lines.length} lines for campaign`);

      for (let i = 1; i < lines.length; i++) {
        const line = lines[i];
        console.log(`    Line ${i}: "${line.substring(0, 60)}..." | Section: ${currentSection}`);

        // Detect severity line
        if (line.match(/^\*\*Gravité:|^\*\*Severity:/i)) {
          console.log(`    → Found severity marker`);
          const severityMatch = line.match(/Critical|High|Medium|Low|Critique|Élevé|Moyen|Faible/i);
          if (severityMatch) {
            const sev = severityMatch[0].toLowerCase();
            if (sev.match(/critical|critique/)) currentSeverity = 'Critical';
            else if (sev.match(/high|élevé/)) currentSeverity = 'High';
            else if (sev.match(/medium|moyen/)) currentSeverity = 'Medium';
            else if (sev.match(/low|faible/)) currentSeverity = 'Low';
          }
          continue;
        }

        // Detect section headers
        if (line.match(/^\*\*Problème détecté:|^\*\*Problem detected:/i)) {
          console.log(`    → Switched to 'issue' section`);
          currentSection = 'issue';
          continue;
        }
        if (line.match(/^\*\*Impact:/i)) {
          console.log(`    → Switched to 'impact' section`);
          currentSection = 'impact';
          continue;
        }
        if (line.match(/^\*\*Recommandation:|^\*\*Recommendation:/i)) {
          console.log(`    → Switched to 'recommendation' section`);
          currentSection = 'recommendation';
          continue;
        }

        // Stop at next campaign or major section
        if (line.startsWith('###') || line.startsWith('##')) {
          break;
        }

        // Collect content based on current section
        if (line.startsWith('- ') || line.startsWith('* ')) {
          const text = line.replace(/^[*-]\s*/, '').replace(/\*\*/g, '').trim();
          console.log(`    → Bullet point found, adding to ${currentSection}: "${text.substring(0, 40)}..."`);

          if (currentSection === 'issue') {
            issueText += (issueText ? ' ' : '') + text;
          } else if (currentSection === 'impact') {
            impactText += (impactText ? ' ' : '') + text;
          } else if (currentSection === 'recommendation') {
            recommendationText += (recommendationText ? ' ' : '') + text;
          }
        } else if (currentSection && !line.startsWith('**')) {
          // Continue collecting text for current section
          console.log(`    → Continuing text for ${currentSection}: "${line.substring(0, 40)}..."`);
          if (currentSection === 'issue') {
            issueText += (issueText ? ' ' : '') + line;
          } else if (currentSection === 'impact') {
            impactText += (impactText ? ' ' : '') + line;
          } else if (currentSection === 'recommendation') {
            recommendationText += (recommendationText ? ' ' : '') + line;
          }
        }
      }

      // Create recommendation if we have at least an issue
      if (issueText || impactText || recommendationText) {
        console.log(`Creating recommendation for ${campaignName}:`, {
          issue: issueText,
          impact: impactText,
          recommendation: recommendationText,
          severity: currentSeverity
        });
        recommendations.push({
          campaign: campaignName,
          issue: issueText || 'N/A',
          severity: currentSeverity,
          impact: impactText || 'N/A',
          recommendation: recommendationText || 'N/A'
        });
      } else {
        console.log(`No content found for campaign ${campaignName}`);
      }
    }

    this.recommendations = recommendations;
    console.log('Total parsed recommendations:', this.recommendations.length);
    console.log('Parsed recommendations:', this.recommendations);
  }

  sortBy(field: keyof Recommendation) {
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

    this.recommendations.sort((a, b) => {
      const aValue = a[this.sortField as keyof Recommendation];
      const bValue = b[this.sortField as keyof Recommendation];

      if (aValue === null || aValue === undefined) return 1;
      if (bValue === null || bValue === undefined) return -1;

      let comparison = 0;
      if (typeof aValue === 'string' && typeof bValue === 'string') {
        comparison = aValue.localeCompare(bValue);
      }

      return this.sortDirection === 'asc' ? comparison : -comparison;
    });
  }

  getSeverityClass(severity: string): string {
    const lower = severity.toLowerCase();
    if (lower.includes('critical') || lower.includes('critique') || lower.includes('kritisch')) {
      return 'severity-critical';
    } else if (lower.includes('high') || lower.includes('élevé') || lower.includes('hoch')) {
      return 'severity-high';
    } else if (lower.includes('medium') || lower.includes('moyen') || lower.includes('mittel')) {
      return 'severity-medium';
    }
    return 'severity-low';
  }

  exportExcel() {
    const data = this.recommendations.map(rec => ({
      'Campagne': rec.campaign,
      'Problème': rec.issue,
      'Gravité': rec.severity,
      'Impact': rec.impact,
      'Recommandation': rec.recommendation
    }));

    const ws: XLSX.WorkSheet = XLSX.utils.json_to_sheet(data);
    const wb: XLSX.WorkBook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Diagnostic IA');

    const colWidths = [
      { wch: 30 }, // Campagne
      { wch: 50 }, // Problème
      { wch: 12 }, // Gravité
      { wch: 40 }, // Impact
      { wch: 50 }  // Recommandation
    ];
    ws['!cols'] = colWidths;

    const fileName = `diagnostic_ia_${new Date().toISOString().split('T')[0]}.xlsx`;
    XLSX.writeFile(wb, fileName);
  }

  toggleMainView() {
    this.mainView = this.mainView === 'report' ? 'schedule' : 'report';
  }

  toggleReportView() {
    this.reportView = this.reportView === 'table' ? 'markdown' : 'table';
  }

  getSuggestedDeadline(severity: string, index: number): string {
    const today = new Date();
    let daysToAdd = 0;

    // Deadline based on severity
    switch (severity.toLowerCase()) {
      case 'critical':
        daysToAdd = 1; // Immediate
        break;
      case 'high':
        daysToAdd = 3; // 3 days
        break;
      case 'medium':
        daysToAdd = 7; // 1 week
        break;
      case 'low':
        daysToAdd = 14; // 2 weeks
        break;
      default:
        daysToAdd = 7;
    }

    const deadline = new Date(today);
    deadline.setDate(today.getDate() + daysToAdd);

    return deadline.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' });
  }

  getUrgencyLabel(severity: string): string {
    const labels: { [key: string]: string } = {
      'critical': 'URGENT',
      'high': 'Prioritaire',
      'medium': 'Normal',
      'low': 'À prévoir'
    };
    return labels[severity.toLowerCase()] || 'Normal';
  }

  toggleTaskComplete(index: number) {
    if (this.completedTasks.has(index)) {
      this.completedTasks.delete(index);
    } else {
      this.completedTasks.add(index);
    }
    this.saveCompletedTasks();
  }

  isTaskCompleted(index: number): boolean {
    return this.completedTasks.has(index);
  }

  getScheduledRecommendations(): Recommendation[] {
    // Sort by severity priority
    const severityOrder: { [key: string]: number } = {
      'critical': 0,
      'high': 1,
      'medium': 2,
      'low': 3
    };

    return [...this.recommendations].sort((a, b) => {
      const aPriority = severityOrder[a.severity.toLowerCase()] ?? 99;
      const bPriority = severityOrder[b.severity.toLowerCase()] ?? 99;
      return aPriority - bPriority;
    });
  }

  getCompletionPercentage(): number {
    if (this.recommendations.length === 0) return 0;
    return Math.round((this.completedTasks.size / this.recommendations.length) * 100);
  }

  private loadCompletedTasks() {
    try {
      const saved = localStorage.getItem('diagnostic_completed_tasks');
      if (saved) {
        this.completedTasks = new Set(JSON.parse(saved));
      }
    } catch (e) {
      console.error('Error loading completed tasks:', e);
    }
  }

  private saveCompletedTasks() {
    try {
      localStorage.setItem('diagnostic_completed_tasks', JSON.stringify(Array.from(this.completedTasks)));
    } catch (e) {
      console.error('Error saving completed tasks:', e);
    }
  }

  clearCompletedTasks() {
    this.completedTasks.clear();
    this.saveCompletedTasks();
  }
}

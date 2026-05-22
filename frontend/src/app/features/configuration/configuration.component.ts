import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TranslocoModule } from '@jsverse/transloco';
import { ApiService } from '../../core/services/api.service';
import { MetricCardComponent } from '../../shared/components/metric-card/metric-card.component';

interface DataStatus {
  data_exists: boolean;
  last_update: string | null;
  account_info: any;
  stats: {
    campaigns: number;
    keywords: number;
    ads: number;
    search_terms: number;
  };
}

@Component({
  selector: 'app-configuration',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslocoModule, MetricCardComponent],
  templateUrl: './configuration.component.html',
  styleUrl: './configuration.component.scss'
})
export class ConfigurationComponent implements OnInit {
  dataStatus: DataStatus | null = null;
  loading = false;
  uploadProgress = false;
  googleDriveFileId = '';
  selectedFile: File | null = null;
  message: string | null = null;
  messageType: 'success' | 'error' | 'info' = 'info';

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadDataStatus();
  }

  loadDataStatus() {
    this.loading = true;
    this.api.get<DataStatus>('data/status').subscribe({
      next: (status) => {
        this.dataStatus = status;
        this.loading = false;
      },
      error: (err) => {
        console.error('Failed to load data status:', err);
        this.loading = false;
      }
    });
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];

      // Validate JSON file
      if (!this.selectedFile.name.endsWith('.json')) {
        this.showMessage('Veuillez sélectionner un fichier JSON', 'error');
        this.selectedFile = null;
      }
    }
  }

  uploadJson() {
    if (!this.selectedFile) {
      this.showMessage('Veuillez sélectionner un fichier', 'error');
      return;
    }

    this.uploadProgress = true;
    this.api.upload('data/import-json', this.selectedFile).subscribe({
      next: (response: any) => {
        this.showMessage(
          `✅ Import réussi ! ${response.stats.campaigns} campagnes, ${response.stats.keywords} mots-clés`,
          'success'
        );
        this.loadDataStatus();
        this.selectedFile = null;
        this.uploadProgress = false;
      },
      error: (err) => {
        this.showMessage('❌ Erreur lors de l\'import : ' + (err.error?.detail || err.message), 'error');
        this.uploadProgress = false;
      }
    });
  }

  importFromGoogleDrive() {
    if (!this.googleDriveFileId.trim()) {
      this.showMessage('Veuillez saisir l\'ID du fichier Google Drive', 'error');
      return;
    }

    // Extract file ID if full URL
    const fileId = this.extractGoogleDriveFileId(this.googleDriveFileId);

    this.uploadProgress = true;
    this.api.post('data/import-google-drive', { file_id: fileId }).subscribe({
      next: (response: any) => {
        this.showMessage(
          `✅ Import Google Drive réussi ! ${response.stats.campaigns} campagnes`,
          'success'
        );
        this.loadDataStatus();
        this.googleDriveFileId = '';
        this.uploadProgress = false;
      },
      error: (err) => {
        this.showMessage('❌ Erreur Google Drive : ' + (err.error?.detail || err.message), 'error');
        this.uploadProgress = false;
      }
    });
  }

  extractGoogleDriveFileId(input: string): string {
    const cleaned = input.trim();

    // Check if it's a URL
    if (cleaned.includes('drive.google.com')) {
      const match = cleaned.match(/\/(?:file\/d|document\/d|spreadsheets\/d)\/([^/?#]+)/);
      if (match) {
        return match[1];
      }
    }

    return cleaned;
  }

  clearData() {
    if (!confirm('Êtes-vous sûr de vouloir supprimer toutes les données ?')) {
      return;
    }

    this.api.delete('data/clear').subscribe({
      next: () => {
        this.showMessage('✅ Données supprimées', 'success');
        this.loadDataStatus();
      },
      error: (err) => {
        this.showMessage('❌ Erreur : ' + err.message, 'error');
      }
    });
  }

  showMessage(text: string, type: 'success' | 'error' | 'info') {
    this.message = text;
    this.messageType = type;

    // Auto-hide after 5 seconds
    setTimeout(() => {
      this.message = null;
    }, 5000);
  }
}

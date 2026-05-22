import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

export type AlertType = 'success' | 'error' | 'warning' | 'info';

@Component({
  selector: 'app-alert',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="alert" [class]="'alert-' + type" *ngIf="visible">
      <div class="alert-icon">{{ getIcon() }}</div>
      <div class="alert-content">
        <h4 *ngIf="title" class="alert-title">{{ title }}</h4>
        <p class="alert-message">{{ message }}</p>
      </div>
      <button *ngIf="dismissible" class="alert-close" (click)="onClose()">×</button>
    </div>
  `,
  styles: [`
    .alert {
      display: flex;
      align-items: flex-start;
      gap: 1rem;
      padding: 1rem 1.25rem;
      border-radius: var(--radius-md);
      border-left: 4px solid;
      margin-bottom: 1rem;
    }

    .alert-icon {
      font-size: 1.5rem;
      line-height: 1;
      flex-shrink: 0;
    }

    .alert-content {
      flex: 1;
    }

    .alert-title {
      font-size: 1rem;
      font-weight: 600;
      margin: 0 0 0.25rem 0;
    }

    .alert-message {
      font-size: 0.875rem;
      margin: 0;
    }

    .alert-close {
      background: none;
      border: none;
      font-size: 1.5rem;
      line-height: 1;
      cursor: pointer;
      opacity: 0.6;
      transition: opacity 0.2s;
      padding: 0;
      width: 1.5rem;
      height: 1.5rem;
      flex-shrink: 0;

      &:hover {
        opacity: 1;
      }
    }

    .alert-success {
      background: #D1FAE5;
      border-color: #10B981;
      color: #065F46;

      .alert-close {
        color: #065F46;
      }
    }

    .alert-error {
      background: #FEE2E2;
      border-color: #EF4444;
      color: #991B1B;

      .alert-close {
        color: #991B1B;
      }
    }

    .alert-warning {
      background: #FEF3C7;
      border-color: #F59E0B;
      color: #854D0E;

      .alert-close {
        color: #854D0E;
      }
    }

    .alert-info {
      background: #DBEAFE;
      border-color: #3B82F6;
      color: #1E40AF;

      .alert-close {
        color: #1E40AF;
      }
    }
  `]
})
export class AlertComponent {
  @Input() type: AlertType = 'info';
  @Input() title?: string;
  @Input() message: string = '';
  @Input() dismissible: boolean = true;
  @Input() visible: boolean = true;

  @Output() close = new EventEmitter<void>();

  getIcon(): string {
    const icons: Record<AlertType, string> = {
      success: '✅',
      error: '❌',
      warning: '⚠️',
      info: 'ℹ️'
    };
    return icons[this.type];
  }

  onClose() {
    this.visible = false;
    this.close.emit();
  }
}

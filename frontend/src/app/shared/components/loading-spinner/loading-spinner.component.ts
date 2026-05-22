import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-loading-spinner',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="loading-spinner" [class.fullscreen]="fullscreen">
      <div class="spinner" [style.width.px]="size" [style.height.px]="size"></div>
      <p *ngIf="message" class="message">{{ message }}</p>
    </div>
  `,
  styles: [`
    .loading-spinner {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 2rem;

      &.fullscreen {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 9999;
        backdrop-filter: blur(4px);
      }
    }

    .spinner {
      border: 4px solid var(--surface-secondary);
      border-top-color: var(--primary-color);
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }

    .message {
      margin-top: 1rem;
      color: var(--text-primary);
      font-size: 1rem;
      text-align: center;
    }

    .fullscreen .message {
      color: white;
    }

    @keyframes spin {
      to {
        transform: rotate(360deg);
      }
    }
  `]
})
export class LoadingSpinnerComponent {
  @Input() size: number = 50;
  @Input() message?: string;
  @Input() fullscreen: boolean = false;
}

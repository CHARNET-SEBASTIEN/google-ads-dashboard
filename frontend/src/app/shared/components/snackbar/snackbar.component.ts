import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { SnackbarService, SnackbarMessage } from '../../../core/services/snackbar.service';

@Component({
  selector: 'app-snackbar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './snackbar.component.html',
  styleUrl: './snackbar.component.scss'
})
export class SnackbarComponent implements OnInit, OnDestroy {
  messages: Array<SnackbarMessage & { id: number; visible: boolean }> = [];
  private subscription?: Subscription;
  private nextId = 0;

  constructor(private snackbarService: SnackbarService) {}

  ngOnInit() {
    this.subscription = this.snackbarService.snackbar$.subscribe(message => {
      this.addMessage(message);
    });
  }

  ngOnDestroy() {
    this.subscription?.unsubscribe();
  }

  private addMessage(message: SnackbarMessage) {
    const id = this.nextId++;
    const item = { ...message, id, visible: false };

    this.messages.push(item);

    // Trigger animation
    setTimeout(() => {
      const index = this.messages.findIndex(m => m.id === id);
      if (index !== -1) {
        this.messages[index].visible = true;
      }
    }, 10);

    // Auto-hide after duration
    const duration = message.duration || 4000;
    setTimeout(() => {
      this.hideMessage(id);
    }, duration);
  }

  hideMessage(id: number) {
    const index = this.messages.findIndex(m => m.id === id);
    if (index !== -1) {
      this.messages[index].visible = false;
      // Remove after animation
      setTimeout(() => {
        this.messages = this.messages.filter(m => m.id !== id);
      }, 300);
    }
  }

  getIcon(type: string): string {
    const icons: { [key: string]: string } = {
      'success': 'check_circle',
      'error': 'error',
      'warning': 'warning',
      'info': 'info'
    };
    return icons[type] || 'info';
  }
}

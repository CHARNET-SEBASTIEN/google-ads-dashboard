import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-metric-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './metric-card.component.html',
  styleUrl: './metric-card.component.scss'
})
export class MetricCardComponent {
  @Input() label: string = '';
  @Input() value: string | number = '';
  @Input() icon?: string;
  @Input() trend?: number; // Positive or negative percentage
  @Input() color?: 'green' | 'red' | 'blue' | 'orange' = 'blue';
}

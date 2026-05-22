import { Component, Input, OnInit, OnDestroy, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import Plotly from 'plotly.js-dist-min';

export interface ChartData {
  x: any[];
  y: any[];
  type?: string;
  mode?: string;
  name?: string;
  line?: any;
  marker?: any;
  fill?: string;
  [key: string]: any;
}

export interface ChartLayout {
  title?: string;
  xaxis?: any;
  yaxis?: any;
  showlegend?: boolean;
  height?: number;
  margin?: any;
  [key: string]: any;
}

@Component({
  selector: 'app-chart',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="chart-container">
      <div #chartDiv class="chart"></div>
      <div *ngIf="loading" class="chart-loading">
        <div class="spinner"></div>
      </div>
    </div>
  `,
  styles: [`
    .chart-container {
      position: relative;
      width: 100%;
    }

    .chart {
      width: 100%;
      min-height: 300px;
    }

    .chart-loading {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(var(--surface-primary-rgb, 255, 255, 255), 0.8);
      z-index: 10;
    }

    .spinner {
      width: 40px;
      height: 40px;
      border: 4px solid var(--surface-secondary);
      border-top-color: var(--primary-color);
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }

    @keyframes spin {
      to {
        transform: rotate(360deg);
      }
    }
  `]
})
export class ChartComponent implements OnInit, AfterViewInit, OnDestroy {
  @ViewChild('chartDiv', { static: false }) chartDiv!: ElementRef;

  @Input() data: ChartData[] = [];
  @Input() layout: ChartLayout = {};
  @Input() config: any = { responsive: true, displayModeBar: true };
  @Input() loading = false;

  private plotlyInstance: any;
  private resizeObserver?: ResizeObserver;

  ngOnInit() {
    // Apply default layout settings
    this.layout = {
      autosize: true,
      margin: { l: 50, r: 30, t: 50, b: 50 },
      paper_bgcolor: 'transparent',
      plot_bgcolor: 'transparent',
      font: {
        family: 'Inter, system-ui, sans-serif',
        size: 12,
        color: 'var(--text-primary)'
      },
      xaxis: {
        gridcolor: 'var(--border-color)',
        linecolor: 'var(--border-color)',
        ...this.layout.xaxis
      },
      yaxis: {
        gridcolor: 'var(--border-color)',
        linecolor: 'var(--border-color)',
        ...this.layout.yaxis
      },
      ...this.layout
    };
  }

  ngAfterViewInit() {
    this.renderChart();
    this.setupResizeObserver();
  }

  ngOnDestroy() {
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
    }
    if (this.plotlyInstance) {
      Plotly.purge(this.chartDiv.nativeElement);
    }
  }

  private renderChart() {
    if (!this.chartDiv || this.data.length === 0) {
      return;
    }

    Plotly.newPlot(
      this.chartDiv.nativeElement,
      this.data,
      this.layout,
      this.config
    ).then((plot: any) => {
      this.plotlyInstance = plot;
    });
  }

  private setupResizeObserver() {
    if (!this.chartDiv) return;

    this.resizeObserver = new ResizeObserver(() => {
      if (this.plotlyInstance) {
        Plotly.Plots.resize(this.chartDiv.nativeElement);
      }
    });

    this.resizeObserver.observe(this.chartDiv.nativeElement);
  }

  updateChart(newData?: ChartData[], newLayout?: ChartLayout) {
    if (newData) {
      this.data = newData;
    }
    if (newLayout) {
      this.layout = { ...this.layout, ...newLayout };
    }

    if (this.plotlyInstance) {
      Plotly.react(
        this.chartDiv.nativeElement,
        this.data,
        this.layout,
        this.config
      );
    } else {
      this.renderChart();
    }
  }
}

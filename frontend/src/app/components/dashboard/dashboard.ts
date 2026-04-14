import { Component, Input, OnChanges, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PredictionResponse } from '../../services/solar';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.scss']
})
export class Dashboard implements OnChanges {
  @Input() data!: PredictionResponse;
  @ViewChild('productionChart') chartRef!: ElementRef;
  private chart: Chart | null = null;

  ngOnChanges() {
    if (this.data) {
      setTimeout(() => this.buildChart(), 100);
    }
  }

  buildChart() {
    if (this.chart) {
      this.chart.destroy();
    }

    const labels = this.data.predictions.map(p =>
      new Date(p.date).toLocaleDateString('fr-FR', { weekday: 'short', day: 'numeric', month: 'short' })
    );
    const productions = this.data.predictions.map(p => p.production_kwh);
    const economies = this.data.predictions.map(p => p.economies_eur);
    const nuages = this.data.predictions.map(p => p.cloud_cover);

    this.chart = new Chart(this.chartRef.nativeElement, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: 'Production (kWh)',
            data: productions,
            backgroundColor: 'rgba(245, 158, 11, 0.7)',
            borderColor: '#f59e0b',
            borderWidth: 2,
            borderRadius: 6,
            yAxisID: 'y'
          },
          {
            label: 'Couverture nuageuse (%)',
            data: nuages,
            type: 'line',
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 2,
            pointRadius: 4,
            fill: true,
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        responsive: true,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: {
            labels: { color: '#8888aa', font: { family: 'Inter' } }
          }
        },
        scales: {
          x: {
            ticks: { color: '#8888aa' },
            grid: { color: 'rgba(255,255,255,0.05)' }
          },
          y: {
            position: 'left',
            ticks: { color: '#f59e0b' },
            grid: { color: 'rgba(255,255,255,0.05)' },
            title: { display: true, text: 'kWh', color: '#f59e0b' }
          },
          y1: {
            position: 'right',
            ticks: { color: '#3b82f6' },
            grid: { drawOnChartArea: false },
            title: { display: true, text: '% nuages', color: '#3b82f6' },
            min: 0,
            max: 100
          }
        }
      }
    });
  }

  getCloudIcon(cloud: number): string {
    if (cloud < 25) return '☀️';
    if (cloud < 50) return '🌤️';
    if (cloud < 75) return '⛅';
    return '☁️';
  }
}
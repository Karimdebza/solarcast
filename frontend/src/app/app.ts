import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Solar, PredictionResponse } from './services/solar';
import { Simulator } from './components/simulator/simulator';
import { Dashboard } from './components/dashboard/dashboard';

@Component({
  selector: 'app-root',
  imports: [CommonModule, Simulator, Dashboard],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  result:PredictionResponse | null = null;

  loading = false;

  error = '';

  constructor(private solar: Solar) {}

  onPredict(config: any) {
    this.loading = true;
    this.error = '';
    this.solar.predict(config).subscribe({
      next: (res) => {
        this.result = res;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'An error occurred while fetching predictions.';
        console.error(err);
        this.loading = false;
      }
    });
  }
}

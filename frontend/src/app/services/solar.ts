import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';
export interface PanelConfig {
  latitude: number;
  longitude: number;
  power_kwc: number;
  surface_m2: number;
  orientation: number;
  tilt: number;
  efficiency: number;
}

export interface DayPrediction {
  date: string;
  production_kwh: number;
  irradiance: number;
  temperature: number;
  cloud_cover: number;
  economies_eur: number;
  co2_evite_kg: number;
}

export interface PredictionResponse {
  location: string;
  total_production_kwh: number;
  total_economies_eur: number;
  total_co2_evite_kg: number;
  predictions: DayPrediction[];
}


@Injectable({
  providedIn: 'root',
})
export class Solar {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}
  predict(config: PanelConfig): Observable<PredictionResponse> {
    return this.http.post<PredictionResponse>(`${this.apiUrl}/predict`, config);
}
}
import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PanelConfig } from '../../services/solar';
import { Map } from '../map/map';
@Component({
  selector: 'app-simulator',
  imports: [CommonModule, FormsModule,Map],
  templateUrl: './simulator.html',
  styleUrl: './simulator.scss',
})
export class Simulator {
  @Output() predict = new EventEmitter<PanelConfig>();

  config: PanelConfig = {
    latitude: 43.30,
    longitude: 5.37,
    power_kwc: 3.0,
    surface_m2: 20.0,
    orientation: 180,
    tilt: 30,
    efficiency: 0.20
  };

  cities = [
    { name: 'Marseille', lat: 43.30, lon: 5.37 },
    { name: 'Paris', lat: 48.85, lon: 2.35 },
    { name: 'Lyon', lat: 45.75, lon: 4.85 },
    { name: 'Bordeaux', lat: 44.84, lon: -0.58 },
    { name: 'Toulouse', lat: 43.60, lon: 1.44 },
    { name: 'Nice', lat: 43.71, lon: 7.26 },
    { name: 'Nantes', lat: 47.22, lon: -1.55 },
  ];

  selectCity(city: any) {
    this.config.latitude = city.lat;
    this.config.longitude = city.lon;
  }

  onSubmit() {
    this.predict.emit(this.config);
  }
  onMapLocationChange(coords: {lat: number, lng: number}) {
  this.config.latitude = parseFloat(coords.lat.toFixed(4));
  this.config.longitude = parseFloat(coords.lng.toFixed(4));
}
}

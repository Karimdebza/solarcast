import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import * as L from 'leaflet';
@Component({
  selector: 'app-map',
  imports: [],
  templateUrl: './map.html',
  styleUrl: './map.scss',
})
export class Map implements OnInit {
private map!: L.Map;
  private marker!: L.Marker;

  @Output() locationChanged = new EventEmitter<{lat: number, lng: number}>();

  ngOnInit() {
    this.initMap();
  }

  private initMap(): void {
    // 1. Initialisation sur Marseille par défaut
    this.map = L.map('map').setView([43.30, 5.37], 10);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(this.map);

    // 2. Icône par défaut (correction d'un bug connu de Leaflet avec Webpack/Angular)
    const iconRetinaUrl = 'assets/marker-icon-2x.png';
    const iconUrl = 'assets/marker-icon.png';
    const shadowUrl = 'assets/marker-shadow.png';
    const iconDefault = L.icon({
      iconRetinaUrl, iconUrl, shadowUrl,
      iconSize: [25, 41], iconAnchor: [12, 41],
      popupAnchor: [1, -34], tooltipAnchor: [16, -28], shadowSize: [41, 41]
    });
    L.Marker.prototype.options.icon = iconDefault;

    // 3. Gestion du clic
    this.map.on('click', (e: L.LeafletMouseEvent) => {
      const { lat, lng } = e.latlng;
      this.updateMarker(lat, lng);
    });
  }

  updateMarker(lat: number, lng: number) {
    if (this.marker) {
      this.marker.setLatLng([lat, lng]);
    } else {
      this.marker = L.marker([lat, lng]).addTo(this.map);
    }
    this.map.panTo([lat, lng]);
    
    // On envoie les infos au composant parent (ton formulaire)
    this.locationChanged.emit({ lat, lng });
  }

}

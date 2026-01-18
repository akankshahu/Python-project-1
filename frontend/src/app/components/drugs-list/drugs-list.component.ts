import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DataService } from '../../services/data.service';
import { Drug } from '../../models/data.models';

@Component({
  selector: 'app-drugs-list',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="drugs-container">
      <h2>Pharmaceutical Drugs</h2>
      
      <div class="drugs-list" *ngIf="!loading && drugs.length > 0">
        <div class="drug-card" *ngFor="let drug of drugs">
          <h3>{{ drug.name }}</h3>
          <p><strong>Generic Name:</strong> {{ drug.generic_name || 'N/A' }}</p>
          <p><strong>Manufacturer:</strong> {{ drug.manufacturer || 'N/A' }}</p>
          <p><strong>Therapeutic Area:</strong> {{ drug.therapeutic_area || 'N/A' }}</p>
          <p><strong>Molecule Type:</strong> {{ drug.molecule_type || 'N/A' }}</p>
          <p class="date"><strong>Approval Date:</strong> {{ drug.approval_date || 'N/A' }}</p>
        </div>
      </div>

      <div class="empty-state" *ngIf="!loading && drugs.length === 0">
        <p>No drugs found. Please add data through the API or run the data pipeline.</p>
      </div>

      <div class="loading" *ngIf="loading">
        <p>Loading drugs...</p>
      </div>

      <div class="error" *ngIf="error">
        <p>{{ error }}</p>
      </div>
    </div>
  `,
  styles: [`
    .drugs-container {
      padding: 20px;
      max-width: 1200px;
      margin: 0 auto;
    }

    h2 {
      color: #2c3e50;
      margin-bottom: 20px;
    }

    .drugs-list {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 20px;
    }

    .drug-card {
      background: white;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      transition: transform 0.2s;
    }

    .drug-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }

    .drug-card h3 {
      margin: 0 0 15px 0;
      color: #3498db;
      font-size: 18px;
    }

    .drug-card p {
      margin: 8px 0;
      color: #555;
      font-size: 14px;
    }

    .date {
      color: #7f8c8d;
      font-size: 12px;
    }

    .empty-state, .loading, .error {
      text-align: center;
      padding: 40px 20px;
      color: #7f8c8d;
    }

    .error {
      color: #e74c3c;
    }
  `]
})
export class DrugsListComponent implements OnInit {
  drugs: Drug[] = [];
  loading: boolean = true;
  error: string | null = null;

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.loadDrugs();
  }

  loadDrugs(): void {
    this.loading = true;
    this.dataService.getDrugs().subscribe({
      next: (data) => {
        this.drugs = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load drugs. Please ensure the backend is running.';
        this.loading = false;
        console.error('Error loading drugs:', err);
      }
    });
  }
}

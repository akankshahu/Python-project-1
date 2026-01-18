import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DataService } from '../../services/data.service';
import { AnalyticsSummary } from '../../models/data.models';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="dashboard-container">
      <h1>DataMAx Analytics Dashboard</h1>
      
      <div class="stats-grid" *ngIf="summary">
        <div class="stat-card">
          <h3>Total Drugs</h3>
          <p class="stat-value">{{ summary.total_drugs }}</p>
        </div>
        
        <div class="stat-card">
          <h3>Total Trials</h3>
          <p class="stat-value">{{ summary.total_trials }}</p>
        </div>
        
        <div class="stat-card">
          <h3>Active Trials</h3>
          <p class="stat-value">{{ summary.active_trials }}</p>
        </div>
        
        <div class="stat-card">
          <h3>Completed Trials</h3>
          <p class="stat-value">{{ summary.completed_trials }}</p>
        </div>
      </div>

      <div class="charts-grid">
        <div class="chart-card">
          <h3>Trials by Phase</h3>
          <div class="phase-list" *ngIf="summary">
            <div *ngFor="let phase of getTrialPhases()" class="phase-item">
              <span>{{ phase.name }}</span>
              <span class="phase-count">{{ phase.count }}</span>
            </div>
          </div>
        </div>

        <div class="chart-card">
          <h3>Trials by Status</h3>
          <div class="status-list" *ngIf="summary">
            <div *ngFor="let status of getTrialStatuses()" class="status-item">
              <span>{{ status.name }}</span>
              <span class="status-count">{{ status.count }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="loading" *ngIf="loading">
        <p>Loading data...</p>
      </div>

      <div class="error" *ngIf="error">
        <p>{{ error }}</p>
      </div>
    </div>
  `,
  styles: [`
    .dashboard-container {
      padding: 20px;
      max-width: 1200px;
      margin: 0 auto;
    }

    h1 {
      color: #2c3e50;
      margin-bottom: 30px;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 20px;
      margin-bottom: 30px;
    }

    .stat-card {
      background: white;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .stat-card h3 {
      margin: 0 0 10px 0;
      color: #7f8c8d;
      font-size: 14px;
      text-transform: uppercase;
    }

    .stat-value {
      font-size: 36px;
      font-weight: bold;
      color: #3498db;
      margin: 0;
    }

    .charts-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
      gap: 20px;
    }

    .chart-card {
      background: white;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .chart-card h3 {
      margin: 0 0 15px 0;
      color: #2c3e50;
    }

    .phase-list, .status-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .phase-item, .status-item {
      display: flex;
      justify-content: space-between;
      padding: 10px;
      background: #ecf0f1;
      border-radius: 4px;
    }

    .phase-count, .status-count {
      font-weight: bold;
      color: #3498db;
    }

    .loading, .error {
      text-align: center;
      padding: 20px;
      color: #7f8c8d;
    }

    .error {
      color: #e74c3c;
    }
  `]
})
export class DashboardComponent implements OnInit {
  summary: AnalyticsSummary | null = null;
  loading: boolean = true;
  error: string | null = null;

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.loadAnalytics();
  }

  loadAnalytics(): void {
    this.loading = true;
    this.dataService.getAnalyticsSummary().subscribe({
      next: (data) => {
        this.summary = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load analytics data. Please ensure the backend is running.';
        this.loading = false;
        console.error('Error loading analytics:', err);
      }
    });
  }

  getTrialPhases(): Array<{name: string, count: number}> {
    if (!this.summary?.trials_by_phase) return [];
    return Object.entries(this.summary.trials_by_phase).map(([name, count]) => ({
      name,
      count
    }));
  }

  getTrialStatuses(): Array<{name: string, count: number}> {
    if (!this.summary?.trials_by_status) return [];
    return Object.entries(this.summary.trials_by_status).map(([name, count]) => ({
      name,
      count
    }));
  }
}

import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { DrugsListComponent } from './components/drugs-list/drugs-list.component';

export const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'drugs', component: DrugsListComponent },
  { path: 'trials', component: DashboardComponent }, // Placeholder
  { path: '**', redirectTo: '/dashboard' }
];

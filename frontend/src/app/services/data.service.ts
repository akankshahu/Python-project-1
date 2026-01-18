import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Drug, ClinicalTrial, AnalyticsSummary } from '../models/data.models';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  // Drug API methods
  getDrugs(skip: number = 0, limit: number = 100): Observable<Drug[]> {
    return this.http.get<Drug[]>(`${this.apiUrl}/drugs/?skip=${skip}&limit=${limit}`);
  }

  getDrug(id: number): Observable<Drug> {
    return this.http.get<Drug>(`${this.apiUrl}/drugs/${id}`);
  }

  createDrug(drug: Partial<Drug>): Observable<Drug> {
    return this.http.post<Drug>(`${this.apiUrl}/drugs/`, drug);
  }

  // Clinical Trial API methods
  getClinicalTrials(skip: number = 0, limit: number = 100): Observable<ClinicalTrial[]> {
    return this.http.get<ClinicalTrial[]>(`${this.apiUrl}/clinical-trials/?skip=${skip}&limit=${limit}`);
  }

  getClinicalTrial(id: number): Observable<ClinicalTrial> {
    return this.http.get<ClinicalTrial>(`${this.apiUrl}/clinical-trials/${id}`);
  }

  getTrialsByDrug(drugId: number): Observable<ClinicalTrial[]> {
    return this.http.get<ClinicalTrial[]>(`${this.apiUrl}/clinical-trials/?drug_id=${drugId}`);
  }

  // Analytics API methods
  getAnalyticsSummary(): Observable<AnalyticsSummary> {
    return this.http.get<AnalyticsSummary>(`${this.apiUrl}/analytics/summary`);
  }

  getTopManufacturers(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/analytics/drugs/top-manufacturers`);
  }

  getTrialsByTherapeuticArea(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/analytics/trials/by-therapeutic-area`);
  }
}

export interface Drug {
  id: number;
  name: string;
  generic_name?: string;
  manufacturer?: string;
  approval_date?: string;
  therapeutic_area?: string;
  molecule_type?: string;
  created_at: string;
  updated_at: string;
}

export interface ClinicalTrial {
  id: number;
  trial_id: string;
  title: string;
  drug_id: number;
  phase?: string;
  status?: string;
  start_date?: string;
  end_date?: string;
  patient_count?: number;
  location?: string;
  sponsor?: string;
  created_at: string;
  updated_at: string;
}

export interface AnalyticsSummary {
  total_drugs: number;
  total_trials: number;
  active_trials: number;
  completed_trials: number;
  total_adverse_events: number;
  trials_by_phase: { [key: string]: number };
  trials_by_status: { [key: string]: number };
}

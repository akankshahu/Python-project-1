-- DataMAx Database Schema
-- PostgreSQL Database for Pharmaceutical Data Analytics Platform

-- Drop existing tables (for clean setup)
DROP TABLE IF EXISTS adverse_events CASCADE;
DROP TABLE IF EXISTS trial_results CASCADE;
DROP TABLE IF EXISTS clinical_trials CASCADE;
DROP TABLE IF EXISTS drugs CASCADE;

-- Drop existing types
DROP TYPE IF EXISTS trial_phase CASCADE;
DROP TYPE IF EXISTS trial_status CASCADE;

-- Create ENUM types
CREATE TYPE trial_phase AS ENUM ('Phase 1', 'Phase 2', 'Phase 3', 'Phase 4');
CREATE TYPE trial_status AS ENUM ('Planned', 'Ongoing', 'Completed', 'Terminated');

-- Drugs Table
CREATE TABLE drugs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    generic_name VARCHAR(200),
    manufacturer VARCHAR(200),
    approval_date DATE,
    therapeutic_area VARCHAR(100),
    molecule_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_drug_name UNIQUE (name)
);

CREATE INDEX idx_drugs_name ON drugs(name);
CREATE INDEX idx_drugs_manufacturer ON drugs(manufacturer);
CREATE INDEX idx_drugs_therapeutic_area ON drugs(therapeutic_area);

-- Clinical Trials Table
CREATE TABLE clinical_trials (
    id SERIAL PRIMARY KEY,
    trial_id VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(500) NOT NULL,
    drug_id INTEGER NOT NULL REFERENCES drugs(id) ON DELETE CASCADE,
    phase trial_phase,
    status trial_status,
    start_date DATE,
    end_date DATE,
    patient_count INTEGER CHECK (patient_count >= 0),
    location VARCHAR(200),
    sponsor VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT check_dates CHECK (end_date IS NULL OR end_date >= start_date)
);

CREATE INDEX idx_trials_trial_id ON clinical_trials(trial_id);
CREATE INDEX idx_trials_drug_id ON clinical_trials(drug_id);
CREATE INDEX idx_trials_phase ON clinical_trials(phase);
CREATE INDEX idx_trials_status ON clinical_trials(status);

-- Trial Results Table
CREATE TABLE trial_results (
    id SERIAL PRIMARY KEY,
    trial_id INTEGER NOT NULL REFERENCES clinical_trials(id) ON DELETE CASCADE,
    endpoint VARCHAR(200),
    result_value FLOAT,
    unit VARCHAR(50),
    p_value FLOAT CHECK (p_value >= 0 AND p_value <= 1),
    confidence_interval VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trial_results_trial_id ON trial_results(trial_id);

-- Adverse Events Table
CREATE TABLE adverse_events (
    id SERIAL PRIMARY KEY,
    drug_id INTEGER NOT NULL REFERENCES drugs(id) ON DELETE CASCADE,
    event_type VARCHAR(200),
    severity VARCHAR(50),
    frequency INTEGER CHECK (frequency >= 0),
    description TEXT,
    reported_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_adverse_events_drug_id ON adverse_events(drug_id);
CREATE INDEX idx_adverse_events_severity ON adverse_events(severity);

-- Create a trigger to update 'updated_at' timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_drugs_updated_at
    BEFORE UPDATE ON drugs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_trials_updated_at
    BEFORE UPDATE ON clinical_trials
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE drugs IS 'Pharmaceutical drugs and medications';
COMMENT ON TABLE clinical_trials IS 'Clinical trial information for drugs';
COMMENT ON TABLE trial_results IS 'Results and outcomes from clinical trials';
COMMENT ON TABLE adverse_events IS 'Reported adverse events for drugs';

-- Grant permissions (adjust as needed for your environment)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO datamax_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO datamax_user;

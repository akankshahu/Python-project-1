-- Sample Data for DataMAx Platform
-- This file contains seed data for testing and development

-- Insert sample drugs
INSERT INTO drugs (name, generic_name, manufacturer, approval_date, therapeutic_area, molecule_type) VALUES
('Aspirin', 'Acetylsalicylic acid', 'Bayer', '1899-03-06', 'Cardiology', 'Small Molecule'),
('Ibuprofen', 'Ibuprofen', 'Pfizer', '1969-01-01', 'Pain Management', 'Small Molecule'),
('Paracetamol', 'Acetaminophen', 'GSK', '1950-01-01', 'Pain Management', 'Small Molecule'),
('Amoxicillin', 'Amoxicillin', 'Novartis', '1972-06-01', 'Infectious Disease', 'Small Molecule'),
('Metformin', 'Metformin', 'Merck', '1994-12-29', 'Endocrinology', 'Small Molecule'),
('Lisinopril', 'Lisinopril', 'AstraZeneca', '1987-12-29', 'Cardiology', 'Small Molecule'),
('Atorvastatin', 'Atorvastatin', 'Pfizer', '1996-12-17', 'Cardiology', 'Small Molecule'),
('Omeprazole', 'Omeprazole', 'AstraZeneca', '1988-10-03', 'Gastroenterology', 'Small Molecule'),
('Adalimumab', 'Adalimumab', 'AbbVie', '2002-12-31', 'Immunology', 'Biologic'),
('Pembrolizumab', 'Pembrolizumab', 'Merck', '2014-09-04', 'Oncology', 'Biologic');

-- Insert sample clinical trials
INSERT INTO clinical_trials (trial_id, title, drug_id, phase, status, start_date, end_date, patient_count, location, sponsor) VALUES
('NCT00001', 'Phase 3 Study of Aspirin in Coronary Artery Disease', 1, 'Phase 3', 'Completed', '2020-01-15', '2022-12-31', 500, 'USA', 'Bayer'),
('NCT00002', 'Safety and Efficacy Study of Ibuprofen', 2, 'Phase 2', 'Ongoing', '2021-06-01', NULL, 250, 'EU', 'Pfizer'),
('NCT00003', 'Efficacy Trial of Paracetamol in Fever Management', 3, 'Phase 3', 'Completed', '2019-03-20', '2021-09-15', 300, 'USA', 'GSK'),
('NCT00004', 'Amoxicillin Resistance Study', 4, 'Phase 4', 'Ongoing', '2022-01-10', NULL, 150, 'Asia', 'Novartis'),
('NCT00005', 'Metformin in Type 2 Diabetes Management', 5, 'Phase 3', 'Completed', '2018-11-05', '2021-08-20', 800, 'Global', 'Merck'),
('NCT00006', 'Lisinopril Hypertension Trial', 6, 'Phase 3', 'Completed', '2019-02-10', '2022-01-15', 600, 'USA', 'AstraZeneca'),
('NCT00007', 'Atorvastatin Cardiovascular Outcomes Study', 7, 'Phase 4', 'Ongoing', '2020-05-20', NULL, 1000, 'Global', 'Pfizer'),
('NCT00008', 'Omeprazole GERD Treatment Study', 8, 'Phase 3', 'Completed', '2018-08-15', '2020-12-30', 400, 'EU', 'AstraZeneca'),
('NCT00009', 'Adalimumab in Rheumatoid Arthritis', 9, 'Phase 3', 'Completed', '2017-03-01', '2020-06-30', 750, 'USA', 'AbbVie'),
('NCT00010', 'Pembrolizumab in Melanoma Treatment', 10, 'Phase 2', 'Ongoing', '2021-09-01', NULL, 200, 'USA', 'Merck');

-- Insert sample trial results
INSERT INTO trial_results (trial_id, endpoint, result_value, unit, p_value, confidence_interval, notes) VALUES
(1, 'Cardiovascular events reduction', 25.5, 'percentage', 0.001, '95% CI: 18-33%', 'Significant reduction in primary endpoint'),
(3, 'Fever reduction time', 4.2, 'hours', 0.003, '95% CI: 3.8-4.6 hours', 'Effective fever management'),
(5, 'HbA1c reduction', 1.5, 'percentage', 0.0001, '95% CI: 1.2-1.8%', 'Significant glycemic control improvement'),
(6, 'Blood pressure reduction', 15, 'mmHg', 0.002, '95% CI: 12-18 mmHg', 'Effective BP management'),
(8, 'Heartburn symptom relief', 85, 'percentage', 0.0001, '95% CI: 80-90%', 'High efficacy in GERD treatment'),
(9, 'ACR20 response rate', 65, 'percentage', 0.0001, '95% CI: 60-70%', 'Significant improvement in RA symptoms');

-- Insert sample adverse events
INSERT INTO adverse_events (drug_id, event_type, severity, frequency, description, reported_date) VALUES
(1, 'Gastrointestinal bleeding', 'Moderate', 150, 'Upper GI bleeding in chronic users', '2022-06-15'),
(2, 'Stomach upset', 'Mild', 500, 'Mild gastrointestinal discomfort', '2022-08-20'),
(3, 'Liver toxicity', 'Severe', 25, 'Elevated liver enzymes at high doses', '2022-03-10'),
(4, 'Allergic reaction', 'Moderate', 200, 'Skin rash and itching', '2022-05-12'),
(5, 'Lactic acidosis', 'Severe', 10, 'Rare but serious metabolic complication', '2021-12-05'),
(7, 'Muscle pain', 'Mild', 300, 'Myalgia reported in clinical trials', '2022-07-18'),
(9, 'Injection site reaction', 'Mild', 400, 'Local pain and redness at injection site', '2022-04-22'),
(10, 'Immune-related adverse event', 'Moderate', 120, 'Thyroid dysfunction', '2022-09-30');

-- Verify data insertion
SELECT 'Drugs inserted: ' || COUNT(*) FROM drugs;
SELECT 'Clinical trials inserted: ' || COUNT(*) FROM clinical_trials;
SELECT 'Trial results inserted: ' || COUNT(*) FROM trial_results;
SELECT 'Adverse events inserted: ' || COUNT(*) FROM adverse_events;

-- Common SQL Queries for DataMAx Analytics Platform

-- 1. Get all drugs with their total number of trials
SELECT 
    d.id,
    d.name,
    d.manufacturer,
    d.therapeutic_area,
    COUNT(ct.id) as total_trials,
    COUNT(CASE WHEN ct.status = 'Ongoing' THEN 1 END) as ongoing_trials,
    COUNT(CASE WHEN ct.status = 'Completed' THEN 1 END) as completed_trials
FROM drugs d
LEFT JOIN clinical_trials ct ON d.id = ct.drug_id
GROUP BY d.id, d.name, d.manufacturer, d.therapeutic_area
ORDER BY total_trials DESC;

-- 2. Get trials by phase distribution
SELECT 
    phase,
    COUNT(*) as trial_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM clinical_trials
WHERE phase IS NOT NULL
GROUP BY phase
ORDER BY phase;

-- 3. Get trials by status
SELECT 
    status,
    COUNT(*) as trial_count,
    SUM(patient_count) as total_patients
FROM clinical_trials
WHERE status IS NOT NULL
GROUP BY status
ORDER BY trial_count DESC;

-- 4. Top manufacturers by number of drugs
SELECT 
    manufacturer,
    COUNT(*) as drug_count,
    COUNT(DISTINCT therapeutic_area) as therapeutic_areas
FROM drugs
WHERE manufacturer IS NOT NULL
GROUP BY manufacturer
ORDER BY drug_count DESC
LIMIT 10;

-- 5. Therapeutic area analysis
SELECT 
    d.therapeutic_area,
    COUNT(DISTINCT d.id) as drug_count,
    COUNT(ct.id) as trial_count,
    AVG(ct.patient_count) as avg_patients_per_trial
FROM drugs d
LEFT JOIN clinical_trials ct ON d.id = ct.drug_id
WHERE d.therapeutic_area IS NOT NULL
GROUP BY d.therapeutic_area
ORDER BY drug_count DESC;

-- 6. Trials with results and their outcomes
SELECT 
    ct.trial_id,
    ct.title,
    d.name as drug_name,
    ct.phase,
    ct.status,
    tr.endpoint,
    tr.result_value,
    tr.unit,
    tr.p_value
FROM clinical_trials ct
JOIN drugs d ON ct.drug_id = d.id
LEFT JOIN trial_results tr ON ct.id = tr.trial_id
WHERE tr.id IS NOT NULL
ORDER BY tr.p_value ASC;

-- 7. Adverse events summary by drug
SELECT 
    d.name as drug_name,
    d.manufacturer,
    COUNT(ae.id) as total_adverse_events,
    COUNT(CASE WHEN ae.severity = 'Severe' THEN 1 END) as severe_events,
    COUNT(CASE WHEN ae.severity = 'Moderate' THEN 1 END) as moderate_events,
    COUNT(CASE WHEN ae.severity = 'Mild' THEN 1 END) as mild_events,
    SUM(ae.frequency) as total_frequency
FROM drugs d
LEFT JOIN adverse_events ae ON d.id = ae.drug_id
GROUP BY d.id, d.name, d.manufacturer
HAVING COUNT(ae.id) > 0
ORDER BY total_adverse_events DESC;

-- 8. Trial duration analysis
SELECT 
    trial_id,
    title,
    start_date,
    end_date,
    CASE 
        WHEN end_date IS NULL THEN 'Ongoing'
        ELSE (end_date - start_date)::text || ' days'
    END as duration,
    patient_count,
    phase,
    status
FROM clinical_trials
ORDER BY start_date DESC;

-- 9. Drugs without any clinical trials
SELECT 
    d.id,
    d.name,
    d.manufacturer,
    d.approval_date,
    d.therapeutic_area
FROM drugs d
LEFT JOIN clinical_trials ct ON d.id = ct.drug_id
WHERE ct.id IS NULL;

-- 10. Monthly trial activity
SELECT 
    TO_CHAR(start_date, 'YYYY-MM') as month,
    COUNT(*) as trials_started,
    SUM(patient_count) as total_patients_enrolled
FROM clinical_trials
WHERE start_date IS NOT NULL
GROUP BY TO_CHAR(start_date, 'YYYY-MM')
ORDER BY month DESC;

-- 11. Statistical significance analysis of trial results
SELECT 
    ct.trial_id,
    ct.title,
    d.name as drug_name,
    tr.endpoint,
    tr.result_value,
    tr.p_value,
    CASE 
        WHEN tr.p_value < 0.001 THEN 'Highly Significant'
        WHEN tr.p_value < 0.05 THEN 'Significant'
        WHEN tr.p_value < 0.1 THEN 'Marginally Significant'
        ELSE 'Not Significant'
    END as significance_level
FROM trial_results tr
JOIN clinical_trials ct ON tr.trial_id = ct.id
JOIN drugs d ON ct.drug_id = d.id
WHERE tr.p_value IS NOT NULL
ORDER BY tr.p_value ASC;

-- 12. Drug approval timeline
SELECT 
    EXTRACT(YEAR FROM approval_date) as approval_year,
    COUNT(*) as drugs_approved,
    STRING_AGG(name, ', ' ORDER BY name) as drug_names
FROM drugs
WHERE approval_date IS NOT NULL
GROUP BY EXTRACT(YEAR FROM approval_date)
ORDER BY approval_year DESC;

-- 13. Comprehensive drug profile
SELECT 
    d.id,
    d.name,
    d.generic_name,
    d.manufacturer,
    d.approval_date,
    d.therapeutic_area,
    d.molecule_type,
    COUNT(DISTINCT ct.id) as total_trials,
    COUNT(DISTINCT tr.id) as total_results,
    COUNT(DISTINCT ae.id) as total_adverse_events,
    MAX(ct.end_date) as latest_trial_date
FROM drugs d
LEFT JOIN clinical_trials ct ON d.id = ct.drug_id
LEFT JOIN trial_results tr ON ct.id = tr.trial_id
LEFT JOIN adverse_events ae ON d.id = ae.drug_id
GROUP BY d.id
ORDER BY d.name;

-- 14. Performance metrics
SELECT 
    'Total Drugs' as metric,
    COUNT(*)::text as value
FROM drugs
UNION ALL
SELECT 
    'Total Clinical Trials',
    COUNT(*)::text
FROM clinical_trials
UNION ALL
SELECT 
    'Active Trials',
    COUNT(*)::text
FROM clinical_trials
WHERE status = 'Ongoing'
UNION ALL
SELECT 
    'Total Patients Enrolled',
    SUM(patient_count)::text
FROM clinical_trials
UNION ALL
SELECT 
    'Total Adverse Events',
    COUNT(*)::text
FROM adverse_events;

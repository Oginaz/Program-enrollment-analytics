USE pwani_teknowgalz;

DROP VIEW IF EXISTS v_program_performance;

CREATE VIEW v_program_performance AS
SELECT
    p.program_name AS program,
    COUNT(a.application_id) AS applicants,
    SUM(CASE WHEN a.offer_status = 'Offered' THEN 1 ELSE 0 END) AS offers,
    SUM(CASE WHEN a.application_status = 'Enrolled' THEN 1 ELSE 0 END) AS enrolled,
    ROUND(
        100.0 * SUM(CASE WHEN a.application_status = 'Enrolled' THEN 1 ELSE 0 END) / COUNT(a.application_id),
        2
    ) AS enrollment_rate,
    ROUND(
        100.0 * SUM(CASE WHEN a.application_status = 'Enrolled' THEN 1 ELSE 0 END)
        / NULLIF(SUM(CASE WHEN a.offer_status = 'Offered' THEN 1 ELSE 0 END), 0),
        2
    ) AS offer_to_enrollment_rate
FROM applications a
JOIN applicants ap ON a.applicant_id = ap.applicant_id
JOIN programs p ON ap.program_id = p.program_id
GROUP BY p.program_id, p.program_name;
USE pwani_teknowgalz;

DROP VIEW IF EXISTS v_county_performance;

CREATE VIEW v_county_performance AS
SELECT
    c.county_name AS county,
    COUNT(a.application_id) AS applicants,
    SUM(CASE WHEN a.application_status = 'Enrolled' THEN 1 ELSE 0 END) AS enrolled,
    SUM(CASE WHEN a.offer_status = 'Offered' THEN 1 ELSE 0 END) AS offers,
    ROUND(
        100.0 * SUM(CASE WHEN a.application_status = 'Enrolled' THEN 1 ELSE 0 END) / COUNT(a.application_id),
        2
    ) AS enrollment_rate,
    ROUND(
        100.0 * SUM(CASE WHEN a.offer_status = 'Offered' THEN 1 ELSE 0 END) / COUNT(a.application_id),
        2
    ) AS offer_rate
FROM applications a
JOIN applicants ap ON a.applicant_id = ap.applicant_id
JOIN counties c ON ap.county_id = c.county_id
GROUP BY c.county_id, c.county_name;
USE pwani_teknowgalz;

DROP VIEW IF EXISTS v_enrollment_factors;

CREATE VIEW v_enrollment_factors AS
-- Application channel
SELECT
    'Application Channel' AS factor_type,
    ac.channel_name AS factor,
    COUNT(*) AS applicants,
    SUM(CASE WHEN a.application_status = 'Enrolled' THEN 1 ELSE 0 END) AS enrolled,
    ROUND(
        100.0 * SUM(CASE WHEN a.application_status = 'Enrolled' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS enrollment_rate
FROM applications a
JOIN application_channels ac ON a.channel_id = ac.channel_id
GROUP BY ac.channel_id, ac.channel_name

UNION ALL

-- Eligibility outcome
SELECT
    'Eligibility' AS factor_type,
    a.eligibility_status AS factor,
    COUNT(*) AS applicants,
    SUM(CASE WHEN a.application_status = 'Enrolled' THEN 1 ELSE 0 END) AS enrolled,
    ROUND(
        100.0 * SUM(CASE WHEN a.application_status = 'Enrolled' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS enrollment_rate
FROM applications a
GROUP BY a.eligibility_status

UNION ALL

-- Interview outcome
SELECT
    'Interview Result' AS factor_type,
    a.interview_result AS factor,
    COUNT(*) AS applicants,
    SUM(CASE WHEN a.application_status = 'Enrolled' THEN 1 ELSE 0 END) AS enrolled,
    ROUND(
        100.0 * SUM(CASE WHEN a.application_status = 'Enrolled' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS enrollment_rate
FROM applications a
GROUP BY a.interview_result

UNION ALL

-- Offer status
SELECT
    'Offer Status' AS factor_type,
    a.offer_status AS factor,
    COUNT(*) AS applicants,
    SUM(CASE WHEN a.application_status = 'Enrolled' THEN 1 ELSE 0 END) AS enrolled,
    ROUND(
        100.0 * SUM(CASE WHEN a.application_status = 'Enrolled' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS enrollment_rate
FROM applications a
GROUP BY a.offer_status;
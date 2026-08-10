-- 1.	Where do applicants drop off?
USE pwani_teknowgalz;
DROP VIEW IF EXISTS funnel_summary;

CREATE VIEW funnel_summary AS
SELECT
    1 AS stage_order,
    'Applications' AS funnel_stage,
    COUNT(*) AS applicants,
    0 AS dropped_off,
    100.00 AS conversion_rate
FROM applications

UNION ALL

SELECT
    2,
    'Eligible',
    SUM(CASE WHEN eligibility_status = 'Eligible' THEN 1 ELSE 0 END),
    COUNT(*) - SUM(CASE WHEN eligibility_status = 'Eligible' THEN 1 ELSE 0 END),
    ROUND(
        100.0 * SUM(CASE WHEN eligibility_status = 'Eligible' THEN 1 ELSE 0 END) / COUNT(*),
        2
    )
FROM applications

UNION ALL

SELECT
    3,
    'Interview Passed',
    SUM(CASE WHEN interview_result = 'Passed' THEN 1 ELSE 0 END),
    SUM(CASE WHEN eligibility_status = 'Eligible' THEN 1 ELSE 0 END)
        - SUM(CASE WHEN interview_result = 'Passed' THEN 1 ELSE 0 END),
    ROUND(
        100.0 * SUM(CASE WHEN interview_result = 'Passed' THEN 1 ELSE 0 END)
        / NULLIF(SUM(CASE WHEN eligibility_status = 'Eligible' THEN 1 ELSE 0 END), 0),
        2
    )
FROM applications

UNION ALL

SELECT
    4,
    'Offered',
    SUM(CASE WHEN offer_status = 'Offered' THEN 1 ELSE 0 END),
    SUM(CASE WHEN interview_result = 'Passed' THEN 1 ELSE 0 END)
        - SUM(CASE WHEN offer_status = 'Offered' THEN 1 ELSE 0 END),
    ROUND(
        100.0 * SUM(CASE WHEN offer_status = 'Offered' THEN 1 ELSE 0 END)
        / NULLIF(SUM(CASE WHEN interview_result = 'Passed' THEN 1 ELSE 0 END), 0),
        2
    )
FROM applications

UNION ALL

SELECT
    5,
    'Enrolled',
    SUM(CASE WHEN application_status = 'Enrolled' THEN 1 ELSE 0 END),
    SUM(CASE WHEN offer_status = 'Offered' THEN 1 ELSE 0 END)
        - SUM(CASE WHEN application_status = 'Enrolled' THEN 1 ELSE 0 END),
    ROUND(
        100.0 * SUM(CASE WHEN application_status = 'Enrolled' THEN 1 ELSE 0 END)
        / NULLIF(SUM(CASE WHEN offer_status = 'Offered' THEN 1 ELSE 0 END), 0),
        2
    )
FROM applications;
USE pwani_teknowgalz;

DROP VIEW IF EXISTS v_funnel_opportunity;

CREATE VIEW v_funnel_opportunity AS
SELECT
    'Application → Eligibility' AS funnel_stage,
    COUNT(*) AS applicants_at_start,
    SUM(CASE WHEN eligibility_status = 'Eligible' THEN 1 ELSE 0 END) AS applicants_progressed,
    COUNT(*) - SUM(CASE WHEN eligibility_status = 'Eligible' THEN 1 ELSE 0 END) AS applicants_lost,
    ROUND(
        100.0 * (COUNT(*) - SUM(CASE WHEN eligibility_status = 'Eligible' THEN 1 ELSE 0 END)) / COUNT(*),
        2
    ) AS drop_off_rate
FROM applications

UNION ALL

SELECT
    'Eligibility → Interview Passed',
    SUM(CASE WHEN eligibility_status = 'Eligible' THEN 1 ELSE 0 END),
    SUM(CASE WHEN interview_result = 'Passed' THEN 1 ELSE 0 END),
    SUM(CASE WHEN eligibility_status = 'Eligible' AND interview_result != 'Passed' THEN 1 ELSE 0 END),
    ROUND(
        100.0 * SUM(CASE WHEN eligibility_status = 'Eligible' AND interview_result != 'Passed' THEN 1 ELSE 0 END)
        / SUM(CASE WHEN eligibility_status = 'Eligible' THEN 1 ELSE 0 END),
        2
    )
FROM applications

UNION ALL

SELECT
    'Interview Passed → Offer',
    SUM(CASE WHEN interview_result = 'Passed' THEN 1 ELSE 0 END),
    SUM(CASE WHEN offer_status = 'Offered' THEN 1 ELSE 0 END),
    SUM(CASE WHEN interview_result = 'Passed' AND offer_status != 'Offered' THEN 1 ELSE 0 END),
    ROUND(
        100.0 * SUM(CASE WHEN interview_result = 'Passed' AND offer_status != 'Offered' THEN 1 ELSE 0 END)
        / SUM(CASE WHEN interview_result = 'Passed' THEN 1 ELSE 0 END),
        2
    )
FROM applications

UNION ALL

SELECT
    'Offer → Enrollment',
    SUM(CASE WHEN offer_status = 'Offered' THEN 1 ELSE 0 END),
    SUM(CASE WHEN application_status = 'Enrolled' THEN 1 ELSE 0 END),
    SUM(CASE WHEN offer_status = 'Offered' AND application_status != 'Enrolled' THEN 1 ELSE 0 END),
    ROUND(
        100.0 * SUM(CASE WHEN offer_status = 'Offered' AND application_status != 'Enrolled' THEN 1 ELSE 0 END)
        / SUM(CASE WHEN offer_status = 'Offered' THEN 1 ELSE 0 END),
        2
    )
FROM applications;
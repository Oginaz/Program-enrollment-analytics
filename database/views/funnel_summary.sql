-- 1.	Where do applicants drop off?
CREATE VIEW funnel_summary AS 
SELECT
	COUNT(*) AS total_applications,
    SUM(CASE WHEN eligibility_status = 'Eligible' THEN 1 ELSE 0 END) AS eligible,
    SUM(CASE WHEN interview_result = 'Passed' THEN 1 ELSE 0 END) AS interview_passed,
    SUM(CASE WHEN offer_status = 'Offered' THEN 1 ELSE 0 END) AS offered,
    SUM(CASE WHEN application_status = 'Enrolled' THEN 1 ELSE 0 END) AS enrolled,
    ROUND(SUM(CASE WHEN eligibility_status = 'Eligible' THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS eligible_rate,
    ROUND(SUM(CASE WHEN interview_result = 'Passed' THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN eligibility_status = 'Eligible' THEN 1 ELSE 0 END),0) * 100, 1) AS interview_pass_rate,
    ROUND(SUM(CASE WHEN application_status = 'Enrolled' THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN offer_status = 'Offered' THEN 1 ELSE 0 END),0) * 100, 1) AS offer_to_enroll_rate
FROM applications;
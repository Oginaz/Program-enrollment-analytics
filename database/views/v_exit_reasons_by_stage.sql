USE pwani_teknowgalz;

DROP VIEW IF EXISTS v_exit_reasons_by_stage;

CREATE VIEW v_exit_reasons_by_stage AS
SELECT
    a.stage,
    er.reason,
    COUNT(*) AS applicants_lost
FROM applications a
JOIN exit_reasons er
    ON a.exit_reason_id = er.exit_reason_id
WHERE a.exit_reason_id IS NOT NULL
GROUP BY
    a.stage,
    er.reason;
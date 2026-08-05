# MySQL Setup Guide  Pwani Teknowgalz Database

This guide walks through creating the database schema and loading the synthetic dataset into MySQL using MySQL Workbench. It covers both loading methods used in this project: the **Table Data Import Wizard** (for the small lookup tables) and **`LOAD DATA LOCAL INFILE`** (for the larger tables containing empty/NULL values, which the wizard can't handle).

---

## Prerequisites

- MySQL Server installed and running locally
- MySQL Workbench installed and connected to your local server (Hostname `127.0.0.1`, Port `3306`)
- This repo cloned locally, with `database/schema/create_tables.sql` and the generated CSVs in `data/`

---

## Step 1: Run the schema script

1. In MySQL Workbench, go to **File → Open SQL Script...**
2. Select `database/schema/create_tables.sql`
3. Click the **⚡ lightning bolt icon** (or `Ctrl+Shift+Enter`) to execute the whole script

This creates the `pwani_teknowgalz` database and all 11 tables in the correct dependency order. Confirm success by right-clicking **SCHEMAS → Refresh All**  `pwani_teknowgalz` should appear with all 11 tables listed:

```
applicants, application_channels, applications, cohorts, counties,
enrollments, exit_reasons, participant_resources, programs,
resource_allocations, resources
```

---

## Step 2: Loading order matters

Because of foreign key relationships, "parent" tables must be loaded before "child" tables that reference them:

| Order | Table | Depends on |
|---|---|---|
| 1 | `counties` | — |
| 2 | `application_channels` | — |
| 3 | `exit_reasons` | — |
| 4 | `resources` | — |
| 5 | `programs` | — |
| 6 | `applicants` | counties, programs |
| 7 | `cohorts` | programs, counties |
| 8 | `applications` | applicants, cohorts, application_channels, exit_reasons |
| 9 | `enrollments` | applications |
| 10 | `resource_allocations` | cohorts, resources |
| 11 | `participant_resources` | enrollments, resources |

Loading a child table before its parent will fail with a foreign key error.

---

## Step 3: Load the 5 lookup tables using the Table Data Import Wizard

These tables (`counties`, `application_channels`, `exit_reasons`, `resources`, `programs`) contain no blank/NULL values, so the GUI wizard works fine for them.

**For each table, in this order:**

1. In the Navigator panel, right-click the table name → **Table Data Import Wizard**
2. Click **Browse**, select the matching CSV from `data/` (e.g. `counties.csv` for the `counties` table)
3. Click **Next** through the file-preview and column-mapping screens — confirm each CSV column maps to a distinct destination column (no duplicates)
4. On the final screen, click **Next** to execute
5. Confirm it reports success (e.g. "6 rows imported")

Repeat for all 5 tables in order: `counties` → `application_channels` → `exit_reasons` → `resources` → `programs`.

**Quick verification after each:**
```sql
SELECT COUNT(*) FROM <table_name>;
```

---

## Step 4: Why the wizard doesn't work for the remaining 6 tables

`applicants`, `cohorts`, `applications`, `enrollments`, `resource_allocations`, and `participant_resources` all contain **legitimately blank cells** for some rows — e.g. an application that never reached a cohort has an empty `cohort_id`; an enrollment still in progress has an empty `completion_date`.

The Import Wizard tries to insert an empty CSV cell as an empty string `''` into numeric/date columns, which MySQL rejects (`Incorrect integer value: '' for column...`, error 1366). This isn't a data problem — it's a wizard limitation. Use `LOAD DATA LOCAL INFILE` instead, which lets us explicitly convert blanks to real `NULL` values.

---

## Step 5: One-time server setup for `LOAD DATA LOCAL INFILE`

Local infile loading is disabled by default for security. Enable it:

```sql
SET GLOBAL local_infile = 1;
```

Verify:
```sql
SHOW GLOBAL VARIABLES LIKE 'local_infile';
```
Should show `ON`.

**Note:** this setting does not persist across a MySQL Server restart — if it reverts to `OFF` later, just rerun the command above.

If you still get **Error 2068 / 3948** ("local data is disabled... on client side") after this, the client side also needs enabling:
1. Close and reopen your Workbench connection
2. If it persists, go to your connection tile on the Workbench home screen → **Edit Connection → Advanced tab** → add `OPT_LOCAL_INFILE=1` in the "Others" field → OK → reconnect

---

## Step 6: Load `applicants`

```sql
USE pwani_teknowgalz;

LOAD DATA LOCAL INFILE 'C:/path/to/your/repo/data/applicants.csv'
INTO TABLE applicants
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(applicant_id, first_name, last_name, gender, date_of_birth, phone_number,
 email, county_id, education_level, income_level, device_ownership,
 program_id, registered_at);
```

Replace the file path with your actual local path (use forward slashes, even on Windows).

Verify:
```sql
SELECT COUNT(*) FROM applicants;   -- should be 20543
```

---

## Step 7: Load `cohorts`

```sql
LOAD DATA LOCAL INFILE 'C:/path/to/your/repo/data/cohorts.csv'
INTO TABLE cohorts
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(cohort_id, program_id, county_id, year, cohort_name, capacity,
 delivery_mode, start_date, end_date);
```

Verify:
```sql
SELECT COUNT(*) FROM cohorts;   -- should be 126
```

---

## Step 8: Load `applications`

This table has blank `cohort_id`, `channel_id`, and `exit_reason_id` values for some rejected applicants — use `@variable` placeholders and `NULLIF()` to convert blanks to real `NULL`:

```sql
LOAD DATA LOCAL INFILE 'C:/path/to/your/repo/data/applications.csv'
INTO TABLE applications
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(application_id, applicant_id, @cohort_id, @channel_id, application_date,
 eligibility_status, interview_result, offer_status, application_status,
 stage, @exit_reason_id)
SET
  cohort_id = NULLIF(@cohort_id, ''),
  channel_id = NULLIF(@channel_id, ''),
  exit_reason_id = NULLIF(@exit_reason_id, '');
```

Verify:
```sql
SELECT COUNT(*) FROM applications;   -- should be 20543, matching applicants exactly
```

---

## Step 9: Load `enrollments`

Blank `completion_date` values (for still-"Ongoing" enrollments) need the same `NULLIF()` treatment:

```sql
LOAD DATA LOCAL INFILE 'C:/path/to/your/repo/data/enrollments.csv'
INTO TABLE enrollments
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(enrollment_id, application_id, enrollment_date, completion_status, @completion_date)
SET
  completion_date = NULLIF(@completion_date, '');
```

Verify:
```sql
SELECT COUNT(*) FROM enrollments;   -- should match the enrolled count from applications
```

---

## Step 10: Load `resource_allocations`

No blank values expected here:

```sql
LOAD DATA LOCAL INFILE 'C:/path/to/your/repo/data/resource_allocations.csv'
INTO TABLE resource_allocations
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(allocation_id, cohort_id, resource_id, quantity_needed, quantity_available, allocation_date);
```

---

## Step 11: Load `participant_resources`

```sql
LOAD DATA LOCAL INFILE 'C:/path/to/your/repo/data/participant_resources.csv'
INTO TABLE participant_resources
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(participant_resource_id, enrollment_id, resource_id, quantity);
```

---

## Step 12: Full verification

Run this to confirm every table loaded with the expected row counts:

```sql
SELECT
  (SELECT COUNT(*) FROM counties)               AS counties,
  (SELECT COUNT(*) FROM application_channels)   AS channels,
  (SELECT COUNT(*) FROM exit_reasons)           AS exit_reasons,
  (SELECT COUNT(*) FROM resources)              AS resources,
  (SELECT COUNT(*) FROM programs)               AS programs,
  (SELECT COUNT(*) FROM applicants)             AS applicants,
  (SELECT COUNT(*) FROM cohorts)                AS cohorts,
  (SELECT COUNT(*) FROM applications)           AS applications,
  (SELECT COUNT(*) FROM enrollments)            AS enrollments,
  (SELECT COUNT(*) FROM resource_allocations)   AS resource_allocations,
  (SELECT COUNT(*) FROM participant_resources)  AS participant_resources;
```

And confirm the core funnel numbers line up:

```sql
SELECT
  (SELECT COUNT(*) FROM applicants) AS total_applicants,
  (SELECT COUNT(*) FROM applications) AS total_applications,
  (SELECT COUNT(*) FROM enrollments) AS total_enrollments,
  ROUND((SELECT COUNT(*) FROM enrollments) / (SELECT COUNT(*) FROM applicants) * 100, 2) AS enrollment_rate_pct;
```

`total_applicants` and `total_applications` should match exactly (20,543), and `enrollment_rate_pct` should land close to 15%.

---

## Troubleshooting reference

| Error | Cause | Fix |
|---|---|---|
| `Incorrect integer value: '' for column X` (1366) | Wizard tried to insert a blank cell into a numeric/date column | Use `LOAD DATA LOCAL INFILE` with `NULLIF(@var, '')` instead of the wizard |
| `Column 'X' specified twice` (1110) | Wizard's auto column-mapping matched two CSV columns to the same destination | Cancel and retry the wizard, manually checking the column-mapping screen |
| `LOAD DATA LOCAL INFILE file request rejected` (2068) | `local_infile` not enabled on the server | `SET GLOBAL local_infile = 1;` then reconnect Workbench |
| `Loading local data is disabled; must be enabled on both client and server` (3948) | Client-side setting also needed | Add `OPT_LOCAL_INFILE=1` in connection's Advanced tab, then reconnect |
| `No database selected` (1046) | Forgot to select/USE the schema first | Run `USE pwani_teknowgalz;` before the load command, or double-click the schema in the Navigator |
| `Duplicate entry 'X' for key 'PRIMARY'` | Table already had leftover rows from an earlier partial/failed load attempt | Clear the table first (see below), then reload |
| `Cannot truncate a table referenced in a foreign key constraint` (1701) | `TRUNCATE` blocked because another table has a FK pointing at this one | Use `DELETE FROM <table>;` instead |
| `You are using safe update mode...` (1175) | Workbench blocks blanket UPDATE/DELETE without a WHERE on a key column | Add a WHERE that matches everything, e.g. `DELETE FROM applications WHERE application_id > 0;` |

---

## Notes

- Always use **forward slashes** in file paths, even on Windows (`C:/path/to/file.csv`, not `C:\path\to\file.csv`)
- If you ever need to reload a table that other tables depend on (e.g. reloading `applications` after `enrollments` already has data), clear the dependent child table(s) first, then the parent, then reload both back up in the correct order
- `SET GLOBAL local_infile = 1` resets to `OFF` if the MySQL service restarts — just rerun it if you hit error 2068/3948 again in a future session

# Program Enrollment Analytics — Pwani Teknowgalz

A synthetic data engineering and analytics project modeling the end-to-end program enrollment funnel for **Pwani Teknowgalz**, a Mombasa-based, women-led NGO equipping young women with digital and technology skills. Built for the **ITExperience Mid-Year Event 2026**, Data Analytics Track.

Pwani Teknowgalz was unable to share real applicant data, so this project instead designs a relational database schema and generates a realistic, research-calibrated synthetic dataset — simulating how applicants move from registration through eligibility, interview, selection, offer, enrollment, and program completion.

📄 **Read the full [Project Brief](docs/project_brief.md)** for the business problem, objectives, and success metrics this project is built around.

---

## Overview

The project combines database design, synthetic data generation, data validation, and analytics into a modular, reproducible pipeline: an analytics-ready dataset that supports reporting, dashboarding, and evidence-based decision-making, without exposing any real organizational or personal data.

**Current status:** database schema finalized, synthetic dataset generated and verified (20,543 applicants, 20,543 applications — zero data loss, ~14.7% enrollment rate matching the brief's baseline), fully loaded into MySQL. SQL views built for dashboard consumption. Power BI dashboard in progress.

---

## Documentation

Detailed reasoning, numbers, and step-by-step instructions live in `docs/` rather than in this README — start here:

| Doc | Purpose |
|---|---|
| [`docs/project_brief.md`](docs/project_brief.md) | The business problem, objectives, scope, success metrics, assumptions, and risks this project addresses |
| [`docs/data_overview.md`](docs/data_overview.md) | What each table contains, how the synthetic data was calibrated (yearly volumes, funnel rates, exit-reason design, program timelines), and the key assumptions behind it |
| [`docs/mysql.md`](docs/mysql.md) | Step-by-step guide to creating the schema and loading the CSVs into MySQL, including the Import Wizard and `LOAD DATA LOCAL INFILE` methods, plus a troubleshooting reference for every error encountered during setup |

---

## Technology Stack

| Category | Tools |
|---|---|
| Programming Language | Python |
| Libraries | Pandas, Faker, Random, Datetime |
| Database | MySQL |
| Version Control | Git, GitHub |
| Business Intelligence | Power BI |

---

## Project Structure

```text
Program-enrollment-analytics/
├── data/
│   ├── applicants.csv
│   ├── applications.csv
│   ├── cohorts.csv
│   ├── enrollments.csv
│   ├── resource_allocations.csv
│   ├── participant_resources.csv
│   └── (lookup tables: counties, application_channels, exit_reasons, resources, programs)
│
├── database/
│   ├── schema/
│   │   └── create_tables.sql
│   └── views/
│       ├── funnel_summary.sql
│       ├── v_county.sql
│       ├── v_enrollment.sql
│       ├── v_exit_reasons_by_stage.sql
│       ├── v_funnel_opportunity.sql
│       └── v_program.sql
│
├── scripts/
│   ├── config.py
│   ├── generate.py
│   ├── requirements.txt
│   └── generators/
│       ├── lookup_generator.py
│       ├── cohort_generator.py
│       ├── applicant_generator.py
│       ├── application_generator.py
│       ├── enrollment_generator.py
│       └── allocation_generator.py
│
├── docs/
│   ├── project_brief.md
│   ├── data_overview.md
│   └── mysql.md
│
├── README.md
├── LICENSE
└── .gitignore
```

---

## Installation

### Prerequisites

- Python 3.10 or later
- Git
- MySQL Server 8.0+ and MySQL Workbench (for database import — see [`docs/mysql.md`](docs/mysql.md))
- Power BI Desktop, plus MySQL Connector/NET (for dashboard visualization)

### Clone the repository

```bash
git clone https://github.com/Oginaz/Program-enrollment-analytics.git
cd Program-enrollment-analytics
```

### Create a virtual environment (recommended)

**Windows**
```bash
python -m venv myvenv
myvenv\Scripts\activate
```

**Linux / macOS**
```bash
python3 -m venv myvenv
source myvenv/bin/activate
```

### Install dependencies

```bash
pip install -r scripts/requirements.txt
```

---

## Running the Project

```bash
cd scripts
python generate.py
```

This runs the full pipeline in dependency order (lookup tables → cohorts → applicants → applications → enrollments → resource allocations → participant resources) and writes all output CSVs to `data/`.

**Expected output on a successful run:**
- `applicants.csv`: 20,543 records
- `applications.csv`: 20,543 records (one per applicant — no drops)
- `enrollments.csv`: ~3,000 records (~14–15% enrollment rate)

Full field-level detail on every table, and the reasoning behind these figures, is in [`docs/data_overview.md`](docs/data_overview.md).

---

## Loading into MySQL

Full step-by-step instructions — including which tables to load via the Table Data Import Wizard versus `LOAD DATA LOCAL INFILE`, and a troubleshooting table for common errors — are in **[`docs/mysql.md`](docs/mysql.md)**.

Quick summary of load order (required, due to foreign key dependencies):
```
counties → application_channels → exit_reasons → resources → programs
→ applicants → cohorts → applications → enrollments
→ resource_allocations → participant_resources
```

`database/views/` contains SQL views built on top of the loaded tables, intended to be imported directly into Power BI for dashboard visuals.

---

## Data Generation Philosophy & Key Assumptions

This project uses **synthetic data**, not real participant information — the organization did not share real applicant records, so all figures are modeled from publicly available research rather than actual historical data. A cohort-allocation bug and a cohort-date-matching bug were both caught and fixed during development; see [`docs/project_brief.md`](docs/project_brief.md) (Assumptions & Risks) for the full account.

Full reasoning behind every generation decision — yearly applicant volumes, funnel conversion rates, program timelines, exit-reason design, resource costs — is documented in [`docs/data_overview.md`](docs/data_overview.md), not duplicated here.

---

## Reproducibility

The project uses a fixed random seed (`RANDOM_SEED = 42` in `config.py`), so running the generator with the same configuration always produces identical datasets — making results comparable across team members and reruns.

---

## Power BI Dashboard

The generated datasets and SQL views connect directly to MySQL for interactive analysis in Power BI, covering:

- Applicant demographics
- Program popularity
- Application funnel conversion rates, by stage
- Enrollment trends over time
- Cohort capacity utilization
- Completion and withdrawal rates
- Resource allocation and cost/time per enrollment
- County-level participation

---

## Future Improvements

- Automated data validation pipeline
- Configurable generation via YAML/JSON instead of hardcoded `config.py` values
- CI/CD integration (GitHub Actions) to catch pipeline regressions automatically
- Expanded dashboard with predictive analytics

---

## Contributors

Developed as part of the ITExperience Mid-Year Event 2026.

- **Sammy Shoka** — [GitHub](https://github.com/Oginaz) · [LinkedIn](https://www.linkedin.com/in/sammy-shoka)
- **Sunday Layefa** — [GitHub](https://github.com/sundaylayefa) · [LinkedIn](https://www.linkedin.com/in/layefasunday)

---

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

## Acknowledgements

- ITExperience, for the opportunity
- Pwani Teknowgalz, for inspiring the project scenario
- The open-source Python community for the tools used throughout

---

## Final Note

Data is more than numbers  it tells a story. This project demonstrates how synthetic data, grounded in real research rather than convenient guesses, can be transformed into meaningful insights through careful database design, rigorous validation, and reproducible engineering practice.
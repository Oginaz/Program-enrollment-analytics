# Program Enrollment Analytics  Pwani Teknowgalz

A synthetic data engineering and analytics project modeling the end-to-end program enrollment funnel for **Pwani Teknowgalz**, a Mombasa-based, women-led NGO equipping young women with digital and technology skills. Built for the **ITExperience Mid-Year Event 2026**, Data Analytics Track.

Pwani Teknowgalz was unable to share real applicant data, so this project instead designs a relational database schema and generates a realistic, research-calibrated synthetic dataset — simulating how applicants move from registration through eligibility, interview, offer, enrollment, and program completion.

📄 **Read the full [Project Brief](docs/project_brief.md)** for the business problem, objectives, and success metrics this project is built around.

---

## Overview

The project combines database design, synthetic data generation, data validation, and analytics into a modular, reproducible pipeline: an analytics-ready dataset that supports reporting, dashboarding, and evidence-based decision-making, without exposing any real organizational or personal data.

**Current status:** database schema finalized, synthetic dataset generated and verified (20,543 applicants, 20,543 applications — zero data loss, ~15.7% enrollment rate matching the brief's baseline), fully loaded into MySQL. Power BI dashboard in progress.

---

## Documentation

| Doc | Purpose |
|---|---|
| [`docs/project_brief.md`](docs/project_brief.md) | The business problem, objectives, scope, success metrics, assumptions, and risks this project addresses |
| [`docs/data_overview.md`](docs/data_overview.md) | What each table/dataset contains, how the synthetic data was calibrated (yearly volumes, funnel rates, program timelines), and the key assumptions behind it |
| [`docs/mysql.md`](docs/mysql.md) | Step-by-step guide to creating the schema and loading the CSVs into MySQL, including the Import Wizard and `LOAD DATA LOCAL INFILE` methods, plus a troubleshooting reference for every error encountered during setup |

---

## Project Objectives

- Design a normalized relational database for managing program enrollment data
- Generate realistic synthetic datasets that preserve referential integrity
- Simulate the complete applicant-to-enrollment workflow, calibrated against real, research-verified organizational figures
- Produce analytics-ready datasets for visualization and reporting
- Support dashboard development using Power BI and SQL-based analytics

## Project Features

- Modular Python data generation pipeline, one generator per entity
- Synthetic relational datasets with enforced foreign key consistency
- Realistic applicant-to-program enrollment workflow, including funnel drop-off and rejection tracking
- Configurable yearly enrollment trends reflecting the organization's actual growth phases (2015 founding → 2020 COVID-era spike → capacity-constrained decline → 2025–26 recovery)
- Cohort-based program management, respecting verified program launch years
- Both cohort-level (capacity constraint) and participant-level (impact/beneficiary) resource tracking
- Analytics-ready CSV outputs
- Reproducible data generation using a fixed random seed
- Modular project architecture for easy maintenance and extension

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
│   └── schema/
│       └── create_tables.sql
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

## Database Schema Overview

The database is built on a normalized relational schema modeling the complete applicant-to-program enrollment lifecycle:

**Lookup tables:** `counties`, `application_channels`, `exit_reasons`, `resources`, `programs`

**Operational tables:** `cohorts`, `applicants`, `applications`, `enrollments`, `resource_allocations`, `participant_resources`

`resource_allocations` and `participant_resources` are deliberately separate: the former is a **per-cohort capacity constraint signal** (did this cohort have enough of a resource to meet demand), while the latter is a **per-participant impact record** (what a specific enrolled participant actually received). See `docs/data_overview.md` for full field-level definitions.

---

## Synthetic Data Generation Pipeline

Generation is dependency-driven, so every dataset is only generated once its prerequisite data exists — preserving referential integrity throughout:

```text
config.py
   │
   ▼
lookup_generator.py        (counties, channels, exit reasons, resources, programs)
   │
   ▼
cohort_generator.py        (cohorts, allocated proportionally to expected program volume)
   │
   ▼
applicant_generator.py     (20,543 applicants across 2015–2026)
   │
   ▼
application_generator.py   (the funnel: eligibility → interview → offer → enrollment/rejection)
   │
   ▼
enrollment_generator.py    (enrollment + completion status, respecting the Aug 2026 snapshot date)
   │
   ▼
allocation_generator.py    (resource_allocations + participant_resources)
```

---

## Installation

### Prerequisites

- Python 3.10 or later
- Git
- MySQL Server 8.0+ and MySQL Workbench (for database import — see `docs/mysql.md`)
- Power BI Desktop (for dashboard visualization)

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
- `enrollments.csv`: ~3,200–3,300 records (~15–16% enrollment rate)

---

## Loading into MySQL

Full step-by-step instructions — including which tables to load via the Table Data Import Wizard versus `LOAD DATA LOCAL INFILE`, and a troubleshooting table for common errors — are in **[`docs/mysql.md`](docs/mysql.md)**.

Quick summary of load order (required, due to foreign key dependencies):
```
counties → application_channels → exit_reasons → resources → programs
→ applicants → cohorts → applications → enrollments
→ resource_allocations → participant_resources
```

---

## Data Generation Philosophy

This project uses **synthetic data**, not real participant information. The organization did not share real applicant records, so all figures are modeled from publicly available research (the organization's website, LinkedIn, and media coverage) rather than actual historical data. See `docs/data_overview.md` for the full reasoning behind yearly applicant volumes, funnel conversion rates, and program timelines.

The generated data is designed to:
- Preserve relational integrity
- Simulate realistic enrollment workflows, including a documented COVID-era volume spike and subsequent capacity-constrained decline
- Support dashboard development and analytics
- Protect organizational privacy
- Provide reproducible datasets for learning and demonstration

---

## Reproducibility

The project uses a fixed random seed (`RANDOM_SEED = 42` in `config.py`), so running the generator with the same configuration always produces identical datasets — making results comparable across team members and reruns.

---

## Key Project Assumptions

Full reasoning is documented in `docs/project_brief.md` (Assumptions & Risks) and `docs/data_overview.md`. Highlights:

- Programs are introduced progressively, matching verified launch years where evidence exists (e.g. CodeHack launched 2020); unverified programs are explicitly flagged as assumptions, not invented
- Each applicant submits a single application per cohort cycle
- Cohorts run a fixed 3-month duration
- Enrollment capacity is funding-constrained, not demand-constrained
- Delivery mode: Physical (pre-2020) → Online (2020, COVID) → Physical (2021 onward)
- The dataset represents the organization's state as of **August 2026** — completion status logic respects this snapshot date
- 30/90/180-day retention tracking was deliberately scoped out, since a 3-month program makes a 180-day checkpoint fall after the program has already ended

---

## A Note on Data Integrity

During development, a cohort-allocation bug caused **~94% of applicants to be silently dropped** from the dataset with no application record at all — despite the pipeline running without any errors. This was only caught by explicitly verifying row counts (`applicants.csv` vs. `applications.csv`), traced to its root cause (cohort capacity being split evenly across all active programs instead of proportionally to expected demand), and fixed. Full details are in the repo's commit history and `docs/mysql.md`.

This is called out deliberately: a pipeline completing without errors is not proof its output is correct.

---

## Power BI Dashboard

The generated datasets connect directly to MySQL for interactive analysis in Power BI, covering:

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
- CI/CD integration (GitHub Actions) to catch pipeline regressions like the one described above automatically
- Expanded dashboard with predictive analytics

---

## Contributors

Developed as part of the ITExperience Mid-Year Event 2026.

- **Sammy Shoka** — [GitHub](https://github.com/Oginaz) · [LinkedIn](https://www.linkedin.com/in/sammy-shoka)
- **Sunday Layefa**

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

Data is more than numbers — it tells a story. This project demonstrates how synthetic data, grounded in real research rather than convenient guesses, can be transformed into meaningful insights through careful database design, rigorous validation, and reproducible engineering practice.

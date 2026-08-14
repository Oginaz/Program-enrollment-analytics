# Project Brief

*This document explains what the project is, why it exists, how we solve the problem, and what success looks like.*

## Contents

1. [Project Overview](#project-overview)
2. [Executive Summary](#executive-summary)
3. [Background](#background)
4. [Business Problem](#business-problem)
5. [Project Objectives](#project-objectives)
6. [Project Scope](#project-scope)
7. [Stakeholders](#stakeholders)
8. [Business Questions](#business-questions)
9. [Success Metrics](#success-metrics)
10. [Deliverables](#deliverables)
11. [Assumptions & Risks](#assumptions--risks)
12. [Timeline](#timeline)
13. [Team Roles](#team-roles)

---

## Project Overview

| | |
|---|---|
| **Project Title** | Program Enrollment Analytics |
| **Organization** | Pwani Teknowgalz |
| **Team Members** | Sammy Shoka & Sunday Layefa |
| **Date** | 04/08/2026 |

---

## Executive Summary

**The organization's challenge**

The organization experiences a significant gap between the number of applicants and the number who successfully enroll in its programs. Despite receiving considerable interest, only approximately **15% of applicants complete the enrollment process**, falling well short of the organization's target of **50% enrollment**. Limited visibility into the applicant journey, resource constraints, and fragmented reporting make it difficult to identify bottlenecks, understand the causes of applicant drop-off, and implement targeted interventions that improve enrollment outcomes.

**Proposed analytics solution**

- Design a relational database schema covering applicants, programs, counties, cohorts, application stages, and resource constraints.
- Generate a realistic synthetic dataset calibrated to the funnel figures in the original brief (20,000+ applications → 12,000 qualifying → 6,000 interviewed → 3,000 enrolled), with reasonable variation by county, age group, and program.
- Clean and validate the dataset, then perform EDA to identify where and why drop-off happens, and which segments (county/age/program) are underrepresented relative to the applicant pool.
- Build an interactive Power BI dashboard tracking the funnel, KPIs, and progress toward the 50%-reach goal.

**Note on figures:** the numbers above are the *original target design figures* from the brief. The actual generated dataset (see [`data_overview.md`](./data_overview.md)) lands at **20,543 applicants, 3,014 enrolled (~14.7%)** — close to target and consistent with the brief's stated ~15% baseline.

---

## Background

**What the organization does**

The organization is a registered technology-focused non-governmental organization (NGO) committed to equipping girls and young women from marginalized communities across Kenya's coastal region with market-relevant digital and technology skills. Through its training programs, the organization seeks to improve participants' employability, foster economic independence, and increase their participation in the growing digital economy by providing sustainable pathways to livelihood and career opportunities.

**Their mission**

> To equip young Kenyan women in marginalized communities with employable technology skills, with the aim of empowering them to have a financially stable future and contribute to the digital economy.

**A note on age range:** the organization's overall mission statement references girls and young women aged **15–28** across all of its programs. Our synthetic dataset and schema specifically model **CodeHack** (the organization's flagship, recurring, cohort-based program), whose verified eligibility criteria target ages **17–28**. This is a deliberate scoping decision, not an inconsistency — the broader 15–28 range likely includes other one-off programs (e.g. Mombasa Girls in STEM, which targeted high-school-age girls) outside CodeHack's specific funnel.

---

## Business Problem

**Current pain points**

The organization receives a substantial number of applications for its programs, but only a small proportion of applicants successfully progress through the entire enrollment process. Although there is strong interest in the programs, the organization lacks visibility into where applicants disengage, why they fail to complete the process, and which operational factors contribute to low enrollment. This makes it difficult to identify bottlenecks, allocate resources effectively, and implement targeted interventions that improve enrollment outcomes.

**Why the problem matters**

Low enrollment limits the organization's ability to fulfill its mission of reaching and supporting more beneficiaries. Without clear insights into the applicant journey, leadership cannot make evidence-based decisions to improve conversion rates, justify funding requests, or optimize the use of available resources. Improving enrollment performance is therefore essential to increasing program impact, operational efficiency, and accountability.

**Strategic impact**

- Reduced ability to achieve the target enrollment rate of 50%
- Lower overall program reach and social impact
- Difficulty demonstrating measurable outcomes to donors and funding partners
- Reduced confidence in strategic planning due to limited data-driven insights
- Missed opportunities to optimize program expansion and resource investment
- Limited evidence to support future funding proposals and organizational growth

---

## Project Objectives

1. Analyze the applicant funnel end-to-end (application → eligibility → interview → selection → enrollment)
2. Identify bottlenecks and the funnel stage(s) with the largest drop-off
3. Evaluate resource allocation and capacity constraints against demand
4. Improve enrollment visibility through a single consolidated, queryable dataset
5. Support evidence-based decision-making for leadership and funders

---

## Project Scope

**In Scope**

1. Database design
2. Synthetic dataset generation
3. SQL database (MySQL)
4. Power BI dashboard
5. KPI development

**Out of Scope**

6. Live production system
7. Real-time integration with the organization's actual systems

---

## Stakeholders

| Internal | External |
|---|---|
| Executive Director | Donors |
| Operations Team | Funding Partners |
| Program Managers | Government |

---

## Business Questions

1. Where do applicants drop off?
2. What factors contribute to drop-off at each funnel stage?
3. What factors are most strongly associated with successful enrollment?
4. Which counties perform best?
5. Which programs have the highest enrollment?
6. Does resource availability affect enrollment?
7. Which stage of the enrollment funnel offers the greatest opportunity for improvement?
8. What operational changes could most effectively increase enrollment toward the 50% target?

---

## Success Metrics

| Metric | Definition |
|---|---|
| **Enrollment Rate** | % of applicants who reach `application_status = 'Enrolled'` |
| **Conversion Rate** | % pass-through at each funnel stage (Applied → Eligible → Interviewed → Selected → Enrolled) |
| **Offer Acceptance Rate** | % of genuine offers (real seat, real capacity) that convert to enrollment — a distinct, narrower metric from overall Enrollment Rate |
| **Capacity Utilization** | Enrolled count ÷ `cohorts.capacity`, per cohort |
| **Device Allocation** | `resource_allocations.quantity_available` ÷ `quantity_needed`, filtered to the Laptop resource |
| **Program Completion** | % of enrollments with `completion_status = 'Completed'` |
| **Cost / Time per Enrollment** | Average resource cost and elapsed days (application → enrollment), by county and program |

See [`mysql.md`](./mysql.md) for the underlying schema these metrics are computed from, and `database/views/` for the SQL views that pre-compute several of them directly for Power BI.

---

## Deliverables

1. Database schema ([`database/schema/create_tables.sql`](../database/schema/create_tables.sql))
2. SQL views for dashboard consumption ([`database/views/`](../database/views/))
3. Synthetic dataset (see [`data_overview.md`](./data_overview.md))
4. SQL setup scripts and database load guide ([`mysql.md`](./mysql.md))
5. Power BI dashboard
6. Documentation (this brief, plus the supporting docs listed above)
7. Final presentation

---

## Assumptions & Risks

**Assumptions**

- All data is synthetic — the organization did not share real applicant records, so figures are modeled from public research (organization website, LinkedIn, media coverage) rather than actual historical data.
- Counties remain unchanged over the 2015–2026 modeled period.
- Programs are introduced progressively over time, matching verified launch years where evidence exists (e.g. CodeHack launched 2020); programs without a confirmed launch year were excluded rather than guessed.
- Each applicant submits a single application, matched to the nearest realistic cohort intake for their program (not just any cohort sharing the same calendar year).
- Program cohorts run a fixed 3-month duration.
- Enrollment capacity is limited by cohort size, which is funding-constrained (subsidized at ~KES 30,000/participant) rather than demand-constrained.
- Delivery mode shifted from Physical (pre-2020) → Online (2020, COVID-driven) → back to Physical (2021 onward).
- The dataset represents the organization's state as of **August 2026**; completion status logic respects this, as well as each individual cohort's own end date.
- 30/90/180-day retention tracking was deliberately excluded from the schema, since CodeHack's 3-month program length makes a 180-day checkpoint fall after the program has already ended — this was a scoped-out KPI, not an oversight.
- Exit reasons are split across 4 funnel stages (Eligibility, Interview, Selection, Enrollment) — see `data_overview.md` for why Selection and Enrollment are modeled as distinct, both to avoid a single generic "capacity" reason dominating the data and to correctly separate organizational capacity limits from genuine applicant-side decisions.

**Risks**

- **Missing business rules**: several real operational details (exact eligibility criteria, true exit reasons, current per-cohort capacity) remain unconfirmed pending a response from the organization to our outreach inquiry.
- **Enrollment process uncertainty**: the exact real-world distinction (if any) between "selected" and "offered" is modeled but unverified.
- **Data quality risks realized and mitigated during development**:
  - A cohort-allocation bug caused ~94% of applicants to be silently dropped from the dataset with no application record at all. Caught through row-count verification (`applicants.csv` vs. `applications.csv` mismatch), traced to its root cause, and fixed.
  - A cohort-matching bug allowed applicants to be paired with cohorts that had already finished (or wouldn't start for a long time), producing enrollment/completion dates that were chronologically impossible. Caught through explicit date-order validation, traced to the funnel logic matching only by calendar year rather than actual cohort timing, and fixed.
  - Both are flagged here as a reminder that all pipeline output should be verified against expected totals and logical constraints, not assumed correct because it ran without errors.

---

## Timeline

| Phase | Description |
|---|---|
| Planning | Scope definition, clarifying questions, organization research |
| Database Schema Design/Creation | Relational schema design, verified against KPI requirements |
| Data Generation | Python/Faker synthetic dataset pipeline, calibrated to funnel targets |
| Database Load | MySQL setup and CSV import (see `mysql.md`) |
| Dashboard | Power BI development against the loaded database |
| Presentation | Final submission and demo |

---

## Team Roles

**Sunday Layefa**
Leads on KPI definition, funnel/segmentation logic, business narrative and insights framing, stakeholder-style documentation, and **Power BI dashboard development**.

**Sammy Shoka**
Leads on database schema design, synthetic dataset generation, the data generation pipeline, MySQL setup, SQL view development, and data validation.

**Joint Responsibilities**
Joint review of whether the dataset "feels" realistic against the brief's figures, and joint preparation of the final presentation.

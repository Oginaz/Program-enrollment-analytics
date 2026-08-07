# Data Overview

This document explains what each table in the dataset contains, how the synthetic data was calibrated, and the reasoning behind the key numbers. For the business context behind this project, see [`project_brief.md`](./project_brief.md). For how to load this data into MySQL, see [`mysql.md`](./mysql.md).

---

## Contents

1. [Dataset Summary](#dataset-summary)
2. [Table Reference](#table-reference)
3. [Yearly Applicant Volumes](#yearly-applicant-volumes)
4. [Funnel Calibration](#funnel-calibration)
5. [Program Timeline](#program-timeline)
6. [Geography](#geography)
7. [Resources & Unit Costs](#resources--unit-costs)
8. [Key Assumptions](#key-assumptions)

---

## Dataset Summary

| Metric | Value |
|---|---|
| Total applicants | 20,543 |
| Total applications | 20,543 (one per applicant — no drops) |
| Total enrollments | 3,224 |
| Overall enrollment rate | ~15.7% |
| Time span | 2015–2026 (partial year, through July) |
| Total cohorts | 126 |
| Programs modeled | 7 |
| Counties | 6 |
| Random seed | 42 (fixed, for reproducibility) |
| Dataset snapshot date | August 2026 |

---

## Table Reference

### Lookup tables

**`counties`** — geographic reference
| Field | Description |
|---|---|
| `county_id` | Primary key |
| `county_name` | e.g. Mombasa, Kilifi, Kwale, Taita Taveta, Lamu, Tana River |
| `region` | Region classification |

**`application_channels`** — how an applicant entered the funnel
| Field | Description |
|---|---|
| `channel_id` | Primary key |
| `channel_name` | e.g. School Outreach, Website, Social Media, Referral, Community, Career Fair, Partner |

**`exit_reasons`** — why an applicant dropped off, by stage
| Field | Description |
|---|---|
| `exit_reason_id` | Primary key |
| `stage` | The funnel stage this reason applies to |
| `reason` | Description of the reason |

**`resources`** — catalog of resource types provided to participants
| Field | Description |
|---|---|
| `resource_id` | Primary key |
| `resource_name` | e.g. Laptop, Internet Bundle, Meals |
| `unit_cost` | Full 3-month cohort cost per participant (KES) |
| `description` | Free-text notes |

**`programs`** — catalog of program offerings
| Field | Description |
|---|---|
| `program_id` | Primary key |
| `program_name` | e.g. CodeHack, Technovation Challenge |
| `description` | Free-text notes |
| `launch_year` | Year the program began (verified where evidence exists — see [Program Timeline](#program-timeline)) |

### Operational tables

**`applicants`** — one row per person who ever applied
| Field | Description |
|---|---|
| `applicant_id` | Primary key |
| `first_name`, `last_name` | Generated via Faker (`en_KE` locale) |
| `gender` | Defaults to female, matching the organization's girls/women-only mission |
| `date_of_birth` | Constrained so age at `registered_at` falls within 17–28 |
| `county_id`, `program_id`, `channel_id` (on `applications`, not here) | Foreign keys |
| `education_level`, `income_level`, `device_ownership` | Demographic fields |
| `phone_number`, `email` | Generated contact details |
| `registered_at` | Application date |

**`cohorts`** — a specific run/intake of a program
| Field | Description |
|---|---|
| `cohort_id` | Primary key |
| `program_id`, `county_id` | Foreign keys |
| `year` | Calendar year of the cohort |
| `cohort_name` | e.g. `CH-2022-03` |
| `capacity` | Maximum seats — basis for Capacity Utilization |
| `delivery_mode` | Physical / Online, depending on year (see [Key Assumptions](#key-assumptions)) |
| `start_date`, `end_date` | 3-month cohort window |

**`applications`** — the funnel backbone; one row per applicant
| Field | Description |
|---|---|
| `application_id` | Primary key |
| `applicant_id`, `cohort_id`, `channel_id` | Foreign keys (`cohort_id`/`channel_id` nullable for edge cases) |
| `application_date` | Date applied |
| `stage` | Furthest stage reached |
| `eligibility_status`, `interview_result`, `offer_status` | Outcome at each gate |
| `application_status` | Final outcome: Enrolled / Rejected |
| `exit_reason_id` | Nullable — set only if rejected |

**`enrollments`** — post-enrollment lifecycle, one row per successful applicant
| Field | Description |
|---|---|
| `enrollment_id` | Primary key |
| `application_id` | Foreign key (unique — one enrollment per application) |
| `enrollment_date` | Date enrolled |
| `completion_status` | Completed / Ongoing / Withdrawn — logic respects the Aug 2026 snapshot date (see [Key Assumptions](#key-assumptions)) |
| `completion_date` | Nullable — set for Completed/Withdrawn only |

**`resource_allocations`** — per-**cohort** capacity signal
| Field | Description |
|---|---|
| `allocation_id` | Primary key |
| `cohort_id`, `resource_id` | Foreign keys |
| `quantity_needed` | Equals cohort capacity |
| `quantity_available` | Randomized shortfall — the capacity constraint signal |
| `allocation_date` | Date of the record |

**`participant_resources`** — per-**enrollment** impact/beneficiary record
| Field | Description |
|---|---|
| `participant_resource_id` | Primary key |
| `enrollment_id`, `resource_id` | Foreign keys |
| `quantity` | Almost always 1 |

`resource_allocations` and `participant_resources` intentionally answer different questions — see `project_brief.md` for the reasoning.

---

## Yearly Applicant Volumes

| Year | Applicants | Enrolled | Rate | Reasoning |
|---|---|---|---|---|
| 2015 | 120 | 30 | 25% | Founding era — small, informal, founders' own network |
| 2016 | 180 | 46 | 26% | Early growth |
| 2017 | 300 | 72 | 24% | Django Girls Mombasa launches |
| 2018 | 450 | 99 | 22% | Mombasa Girls in STEM (Phase 2) |
| 2019 | 700 | 140 | 20% | STEM Cafe Kenya launches, multi-region |
| 2020 | 1,350 | 243 | 18% | **COVID-era peak** — CodeHack launches ("COVID-19 Edition"); virtual delivery removes geographic/physical barriers, reaching 6 counties at once |
| 2021 | 1,100 | 143 | 13% | **Post-COVID dip** — tech hub opens physically (Feb 2021); virtual-era awareness held applicant volume up, but full reversion to Physical-only delivery reintroduced transport/venue/geographic constraints, sharply cutting conversion |
| 2022 | 1,700 | 255 | 15% | Recovery begins, capacity-constrained |
| 2023 | 2,700 | 405 | 15% | Continued capacity strain |
| 2024 | 3,500 | 525 | 15% | Matches the brief's stated current baseline |
| 2025 | 3,900 | 585 | 15% | KPI/funnel-improvement initiative begins (this project) |
| 2026 (Jan–Jul, partial) | 4,543 | 681 | 15% | Continued, still well short of the 50% target |
| **Total** | **20,543** | **3,224** | **~15.7%** | |

---

## Funnel Calibration

The dataset is calibrated against the original brief's target funnel shape:

```
20,000+ Applications → 12,000 Qualifying → 6,000 Interviewed → 3,000 Enrolled
        (100%)              (60%)              (50%)              (50%)
```

This cascade (60% eligible → 50% interviewed → 50% enrolled = 15% overall) came directly from the funnel graphic in the organization's official project brief, and is the authoritative target the yearly rates in `config.py` (`YEAR_TARGET_RATE`) are tuned against. The actual generated dataset lands at 20,543 → 3,224 (15.7%), closely matching this target.

**Note on the "6,800" figure:** earlier drafts of the brief (and the organization's own website) reference "impacted 6,800 young women... representing 15% of the applicant pool" — this is mathematically inconsistent (6,800/20,000 = 34%, not 15%) and appears to be a persistent copy-paste error traced across multiple independent sources, including the org's own blog. The funnel graphic's **3,000 / 15%** figure was treated as authoritative instead, since it's internally consistent and matches the brief's stated current-state baseline.

---

## Program Timeline

| Program | Launch Year | Confidence |
|---|---|---|
| Technovation Challenge | 2015 | Verified — Ruth Kaveke: "launched in 2015, Mombasa region" |
| Mombasa Girls in STEM | 2016 | Verified — Phase 1 ~2016, Phase 2 ~2018 |
| Django Girls Mombasa | 2017 | Verified — first workshop, February 2017 |
| STEM Cafe Kenya | 2019 | Verified — target of 135 participants across 5 regions |
| CodeHack | 2020 | Verified — first cohort was the "COVID-19 Edition" |
| AjiraForShe | 2024 | Verified active by mid-2024; exact launch year unconfirmed |
| CodeHack Women in Tech Accelerator | 2025 | Verified — launched July 2025 |

No program appears in the dataset before its verified (or reasonably assumed) launch year — cohorts are only generated for programs that had actually launched by that point. Several other real program names found during research (e.g. Africa Code Week, Coders at American Spaces, 3D Design & Printing) were deliberately excluded from the final dataset rather than assigned a guessed launch year, to avoid presenting invented data as fact.

---

## Geography

6 counties are modeled, reflecting Kenya's coastal region where the organization primarily operates: **Mombasa, Kilifi, Kwale, Taita Taveta, Lamu, Tana River**. County selection per applicant/cohort is weighted, not uniform, reflecting the organization's actual concentration of activity around Mombasa.

---

## Resources & Unit Costs

All costs represent the **full 3-month cohort cost per participant** (not a monthly rate), in KES:

| Resource | Unit Cost (KES) | Notes |
|---|---|---|
| Laptop | 25,000 | One-time; ~25% of enrolled participants receive one |
| Internet Bundle | 4,500 | ~1,500/month × 3 months; Online/Hybrid cohorts only |
| Training Manual | 500 | One-time issuance |
| Stationery | 300 | One-time kit |
| Meals | 4,800 | ~24 sessions × ~200 KES |
| Transport Support | 3,600 | ~24 sessions × ~150 KES |
| Mentorship | 2,000 | Flat, program-long |
| Branded T-Shirt | 700 | One-time |

**Sanity check:** a full physical-delivery participant's typical resource cost (Manual + Stationery + Meals + Transport + Mentorship + T-Shirt ≈ KES 11,900, or ~36,900 if they also receive a laptop) brackets reasonably around the verified **KES 30,000 CodeHack subsidy per participant**, supporting these as defensible estimates rather than arbitrary numbers.

---

## Key Assumptions

- **Delivery mode**: Physical by default → Online in 2020 (COVID) → reverted to Physical from 2021 onward (not Hybrid) — reflecting a full return to in-person delivery once the tech hub reopened physically in February 2021.
- **Age range**: 17–28, matching CodeHack's verified eligibility criteria (the organization's broader mission references 15–28 across all programs — see `project_brief.md` for why these differ).
- **Gender**: defaults to female, matching the organization's girls/women-only mission.
- **Cohort capacity**: funding-constrained (subsidized per-seat cost), not demand-constrained — total available seats across all years (~5,400+) comfortably exceed the ~3,200 actually needed to hit the 15% target, meaning the low enrollment rate is driven primarily by funnel selectivity, not a hard capacity ceiling, except in the smallest early years.
- **Completion status**: respects the **August 2026 snapshot date** — a cohort that hasn't finished yet cannot show as "Completed," and a cohort that has already finished cannot show as "Ongoing."
- **Retention tracking (30/90/180-day)**: deliberately excluded from the schema. CodeHack's 3-month program length makes a 180-day checkpoint fall after the program has already concluded, measuring undefined post-program engagement rather than in-program retention.
- **Exit reasons**: seeded with plausible, stage-appropriate placeholder categories (cost, distance/transport, device access, family obligation, lost contact, etc.), pending the organization's confirmation of actual drop-off reasons.
- **Programs list**: trimmed to 7 entries with genuine evidence (verified launch year or explicitly confirmed as active), rather than including plausible-sounding but unverified program names.

For the full narrative behind these decisions — including the data-integrity bug caught and fixed during development — see [`project_brief.md`](./project_brief.md).

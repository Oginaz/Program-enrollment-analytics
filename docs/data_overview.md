# Data Overview

This document explains what each table in the dataset contains, how the synthetic data was calibrated, and the reasoning behind the key numbers. For the business context behind this project, see [`project_brief.md`](./project_brief.md). For how to load this data into MySQL, see [`mysql.md`](./mysql.md).

---

## Contents

1. [Dataset Summary](#dataset-summary)
2. [Table Reference](#table-reference)
3. [Yearly Applicant Volumes](#yearly-applicant-volumes)
4. [Funnel Calibration](#funnel-calibration)
5. [Exit Reasons Design](#exit-reasons-design)
6. [Program Timeline](#program-timeline)
7. [Geography](#geography)
8. [Resources & Unit Costs](#resources--unit-costs)
9. [Key Assumptions](#key-assumptions)

---

## Dataset Summary

| Metric | Value |
|---|---|
| Total applicants | 20,543 |
| Total applications | 20,543 (one per applicant  no drops) |
| Total enrollments | 3,014 |
| Overall enrollment rate | ~14.7% |
| Time span | 2015–2026 (partial year, through July) |
| Total cohorts | 126 |
| Programs modeled | 7 |
| Counties | 6 |
| Exit reasons | 17, across 4 stages |
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
| `stage` | Eligibility, Selection, Interview, or Enrollment — see [Exit Reasons Design](#exit-reasons-design) |
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
| `county_id`, `program_id` | Foreign keys |
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
| `applicant_id`, `cohort_id`, `channel_id` | Foreign keys (`cohort_id` nullable for edge cases) |
| `application_date` | Date applied |
| `stage` | Furthest stage reached: Eligibility, Interview, Selection, or Enrollment |
| `eligibility_status`, `interview_result`, `offer_status` | Outcome at each gate |
| `application_status` | Final outcome: Enrolled / Rejected |
| `exit_reason_id` | Nullable — set only if rejected before an offer was ever extended |

**`enrollments`** — post-enrollment lifecycle, one row per successful applicant
| Field | Description |
|---|---|
| `enrollment_id` | Primary key |
| `application_id` | Foreign key (unique — one enrollment per application) |
| `enrollment_date` | Date enrolled |
| `completion_status` | Completed / Ongoing / Withdrawn — logic respects the Aug 2026 snapshot date and the cohort's own `end_date` (see [Key Assumptions](#key-assumptions)) |
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

`resource_allocations` and `participant_resources` intentionally answer different questions — see `project_brief.md` for the reasoning. Both are also available as MySQL **views** for direct Power BI consumption  see `database/views/`.

---

## Yearly Applicant Volumes

Figures below are the **actual realized output** of the generator (not the raw target rates in `config.py`), pulled directly from the loaded dataset:

| Year | Applicants | Enrolled | Rate | Reasoning |
|---|---|---|---|---|
| 2015 | 120 | 16 | 13.3% | Founding era  small, informal, founders' own network |
| 2016 | 180 | 38 | 21.1% | Early growth |
| 2017 | 300 | 57 | 19.0% | Django Girls Mombasa launches |
| 2018 | 450 | 93 | 20.7% | Mombasa Girls in STEM (Phase 2) |
| 2019 | 700 | 138 | 19.7% | STEM Cafe Kenya launches, multi-region |
| 2020 | 1,350 | 223 | 16.5% | **COVID-era peak**  CodeHack launches ("COVID-19 Edition"); virtual delivery removes geographic/physical barriers, reaching 6 counties at once |
| 2021 | 1,100 | 164 | 14.9% | Tech hub reopens physically (Feb 2021); reversion to Physical-only delivery reintroduces transport/venue/geographic constraints |
| 2022 | 1,700 | 245 | 14.4% | Recovery continues, capacity-constrained |
| 2023 | 2,700 | 326 | 12.1% | Applicant growth outpaces capacity — lowest point in the series |
| 2024 | 3,500 | 494 | 14.1% | Close to the brief's stated current baseline |
| 2025 | 3,900 | 567 | 14.5% | KPI/funnel-improvement initiative begins (this project) |
| 2026 (Jan–Jul, partial) | 4,543 | 653 | 14.4% | Continued, still well short of the 50% target |
| **Total** | **20,543** | **3,014** | **~14.7%** | |

**The realized rate is therefore an *emergent result* of eligibility, interview, capacity, and offer-acceptance combined — not a number forced directly onto the output. This is a more realistic model, at the cost of the yearly rate no longer being a precise dial.

---

## Funnel Calibration

The dataset is calibrated against the original brief's target funnel shape:

```
20,000+ Applications → 12,000 Qualifying → 6,000 Interviewed → 3,000 Enrolled
        (100%)              (60%)              (50%)              (50%)
```

This cascade (60% eligible → 50% interviewed → 50% enrolled = 15% overall) came directly from the funnel graphic in the organization's official project brief. The actual generated dataset lands at 20,543 → 3,014 (~14.7%), closely matching this target.

**Note on the "6,800" figure:** earlier drafts of the brief (and the organization's own website) reference "impacted 6,800 young women... representing 15% of the applicant pool" — this is mathematically inconsistent (6,800/20,000 = 34%, not 15%) and appears to be a persistent copy-paste error traced across multiple independent sources, including the org's own blog. The funnel graphic's **3,000 / 15%** figure was treated as authoritative instead, since it's internally consistent and matches the brief's stated current-state baseline.

---

## Exit Reasons Design

Exit reasons are split across **four funnel stages**, reflecting a deliberate redesign partway through development:

| Stage | Reasons | Applicant-attributable? |
|---|---|---|
| **Eligibility** | Did not meet requirements, incomplete application, missing documents, submitted after deadline | Yes |
| **Interview** | Interview not attended, interview unsuccessful | Yes |
| **Selection** | Selection criteria not met, lower selection ranking, program requirements not matched | Used when a genuinely qualified applicant (passed interview) can't be offered a seat — either no cohort capacity remains, or the year's enrollment target has already been reached |
| **Enrollment** | Declined offer, did not respond in time, could not afford costs, family did not permit, lost contact, personal/health emergency | Yes — used only when a **genuine offer was extended** (a real seat existed) but the applicant didn't convert |



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

No program appears in the dataset before its verified (or reasonably assumed) launch year  cohorts are only generated for programs that had actually launched by that point. Several other real program names found during research (e.g. Africa Code Week, Coders at American Spaces, 3D Design & Printing) were deliberately excluded from the final dataset rather than assigned a guessed launch year, to avoid presenting invented data as fact.

---

## Geography

6 counties are modeled, reflecting Kenya's coastal region where the organization primarily operates: **Mombasa, Kilifi, Kwale, Taita Taveta, Lamu, Tana River**. County selection per applicant/cohort is weighted, not uniform, reflecting the organization's actual concentration of activity around Mombasa.

---

## Resources & Unit Costs

All costs represent the **full 3-month cohort cost per participant** (not a monthly rate), in KES:

| Resource | Unit Cost (KES) | Notes |
|---|---|---|
| Laptop | 25,000 | One-time; a minority of enrolled participants receive one |
| Internet Bundle | 3,000 | 1,000/month × 3 months; Online-delivery cohorts only |
| Training Manual | 500 | One-time issuance |
| Stationery | 300 | One-time kit |
| Meals | 4,800 | 24 sessions × ~200 KES |
| Transport Support | 3,600 | 24 sessions × 150 KES |
| Mentorship | 2,000 | Flat, program-long |
| Branded T-Shirt | 700 | One-time |

**Sanity check:** a full physical-delivery participant's typical resource cost (Manual + Stationery + Meals + Transport + Mentorship + T-Shirt ≈ KES 11,900, or ~36,900 if they also receive a laptop) brackets reasonably around the verified **KES 30,000 CodeHack subsidy per participant**, supporting these as defensible estimates rather than arbitrary numbers.

---

## Key Assumptions

- **Delivery mode**: Physical by default → Online in 2020 (COVID) → reverted to Physical from 2021 onward — reflecting a full return to in-person delivery once the tech hub reopened physically in February 2021.
- **Cohort matching**: applicants are matched to the nearest realistic cohort intake for their program — either one already running at the time they applied, or one starting within a bounded window afterward — rather than any cohort sharing the same calendar year. This prevents an applicant from being paired with a cohort that had already finished, which previously produced impossible enrollment/completion date combinations.
- **Age range**: 17–28, matching CodeHack's verified eligibility criteria (the organization's broader mission references 15–28 across all programs  see `project_brief.md` for why these differ).
- **Gender**: defaults to female, matching the organization's girls/women-only mission.
- **Cohort capacity**: funding-constrained (subsidized per-seat cost), not demand-constrained — total available seats across all years comfortably exceed the number actually enrolled, meaning the low enrollment rate is driven primarily by funnel selectivity (eligibility, interview, selection competition), not a hard capacity ceiling in most years.
- **Completion status**: respects both the **August 2026 snapshot date** and each cohort's own `end_date` — a cohort that hasn't finished yet cannot show as "Completed," and a cohort that has already finished cannot show as "Ongoing."
- **Retention tracking (30/90/180-day)**: deliberately excluded from the schema. CodeHack's 3-month program length makes a 180-day checkpoint fall after the program has already concluded, measuring undefined post-program engagement rather than in-program retention.
- **Exit reasons**: seeded with plausible, stage-appropriate categories across 4 stages (see [Exit Reasons Design](#exit-reasons-design)), pending the organization's confirmation of actual drop-off reasons.
- **Programs list**: trimmed to 7 entries with genuine evidence (verified launch year or explicitly confirmed as active), rather than including plausible-sounding but unverified program names.

For the full narrative behind these decisions  including the data-integrity issues caught and fixed during development  see [`project_brief.md`](./project_brief.md).


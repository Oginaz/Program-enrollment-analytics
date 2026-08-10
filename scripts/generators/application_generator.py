"""
PWANI TEKNOWGALZ
APPLICATION GENERATOR
"""

import random
import pandas as pd

from config import (
    DATA_DIR,
    RANDOM_SEED,
    APPLICATION_CHANNELS,
    YEAR_CONFIGURATION
)

random.seed(RANDOM_SEED)

# Dataset snapshot
CURRENT_DATE = pd.Timestamp("2026-08-01")

# Application channel weights
CHANNEL_WEIGHTS = [
    40,  # School Outreach
    15,  # Website
    18,  # Social Media
    10,  # Referral
    10,  # Community
    4,   # Career Fair
    3    # Partner
]

# Exit reasons
DOCUMENT_EXIT_REASONS = [1, 2, 3, 4]                       # Eligibility
SELECTION_EXIT_REASONS = [5, 6, 7]                         # Selection
SELECTION_WEIGHTS = [40, 30, 30]
INTERVIEW_EXIT_REASONS = [8, 9]                            # Interview
ENROLLMENT_DECLINE_REASONS = [10, 11, 12, 13, 14, 15, 16, 17]  # Enrollment
DECLINE_WEIGHTS = [25, 20, 18, 12, 10, 8, 4, 3]

OFFER_ACCEPTANCE_RATE = 0.92

YEAR_TARGET_RATE = {
    2015: 0.28,
    2016: 0.26,
    2017: 0.24,
    2018: 0.22,
    2019: 0.20,
    2020: 0.23,
    2021: 0.16,
    2022: 0.15,
    2023: 0.15,
    2024: 0.15,
    2025: 0.15,
    2026: 0.15
}


# -------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------

def random_channel():
    return random.choices(APPLICATION_CHANNELS, weights=CHANNEL_WEIGHTS, k=1)[0]


def random_selection_reason():
    return random.choices(SELECTION_EXIT_REASONS, weights=SELECTION_WEIGHTS, k=1)[0]


# -------------------------------------------------------------
# MAIN GENERATOR
# -------------------------------------------------------------

def generate():
    applicants = pd.read_csv(DATA_DIR / "applicants.csv")
    cohorts = pd.read_csv(DATA_DIR / "cohorts.csv")

    # Ensure dates are datetime objects
    cohorts["start_date"] = pd.to_datetime(cohorts["start_date"])
    cohorts["end_date"] = pd.to_datetime(cohorts["end_date"])

    # Remaining seats per cohort
    remaining_capacity = {
        row.cohort_id: row.capacity
        for _, row in cohorts.iterrows()
    }

    # ---------------------------------------------------------
    # PASS 1
    # Determine eligibility and interview results.
    # ---------------------------------------------------------
    prepared = []

    for _, applicant in applicants.iterrows():
        application_year = pd.to_datetime(applicant.registered_at).year
        application_date = pd.to_datetime(applicant.registered_at)

        eligible_cohorts = cohorts[
            (cohorts.program_id == applicant.program_id)
            & (cohorts.year == application_year)
            & (cohorts.start_date >= application_date)
            & (cohorts.start_date <= CURRENT_DATE)
        ]

        # No suitable cohort
        if len(eligible_cohorts) == 0:
            prepared.append({
                "applicant": applicant,
                "year": application_year,
                "date": application_date,
                "eligible_cohorts": eligible_cohorts,
                "eligible": False,
                "interview_pass": False
            })
            continue

        # Eligibility
        eligible = random.random() < 0.97

        if not eligible:
            prepared.append({
                "applicant": applicant,
                "year": application_year,
                "date": application_date,
                "eligible_cohorts": eligible_cohorts,
                "eligible": False,
                "interview_pass": False
            })
            continue

        # Interview
        interview_pass = random.random() < 0.85

        prepared.append({
            "applicant": applicant,
            "year": application_year,
            "date": application_date,
            "eligible_cohorts": eligible_cohorts,
            "eligible": True,
            "interview_pass": interview_pass
        })

    # ---------------------------------------------------------
    # YEARLY APPLICANT COUNTS
    # Targets are based on ALL applicants.
    # ---------------------------------------------------------
    yearly_applicants = (
        applicants.assign(year=pd.to_datetime(applicants.registered_at).dt.year)
        .groupby("year")
        .size()
        .to_dict()
    )

    yearly_targets = {}
    for year, count in yearly_applicants.items():
        yearly_targets[year] = int(count * YEAR_TARGET_RATE[year])

    # ---------------------------------------------------------
    # OFFER CANDIDATES
    # ---------------------------------------------------------
    offer_candidates = {year: [] for year in YEAR_TARGET_RATE}

    for item in prepared:
        if item["eligible"] and item["interview_pass"] and len(item["eligible_cohorts"]) > 0:
            offer_candidates[item["year"]].append(item)

    # ---------------------------------------------------------
    # ENROLLMENT CANDIDATES
    # Oversample offers because only approximately 92%
    # of genuine offers are expected to convert.
    # ---------------------------------------------------------
    enrollment_candidates = {}

    for year in YEAR_TARGET_RATE:
        candidates = offer_candidates.get(year, [])
        target = yearly_targets.get(year, 0)

        oversampled_target = int(target / OFFER_ACCEPTANCE_RATE)
        oversampled_target = min(oversampled_target, len(candidates))

        shuffled = candidates.copy()
        random.shuffle(shuffled)

        enrollment_candidates[year] = set(
            id(item) for item in shuffled[:oversampled_target]
        )

    # ---------------------------------------------------------
    # PASS 2
    # Generate applications
    # ---------------------------------------------------------
    applications = []
    application_id = 1
    yearly_enrolled = {year: 0 for year in YEAR_TARGET_RATE}

    for item in prepared:
        applicant = item["applicant"]
        application_year = item["year"]
        application_date = item["date"]
        eligible_cohorts = item["eligible_cohorts"]
        eligible = item["eligible"]
        interview_pass = item["interview_pass"]

        # No suitable cohort
        if len(eligible_cohorts) == 0:
            applications.append({
                "application_id": application_id,
                "applicant_id": applicant.applicant_id,
                "cohort_id": None,
                "channel_id": random_channel()["channel_id"],
                "application_date": application_date,
                "eligibility_status": "Not Eligible",
                "interview_result": "Not Interviewed",
                "offer_status": "Not Offered",
                "application_status": "Rejected",
                "stage": "Eligibility",
                "exit_reason_id": None
            })
            application_id += 1
            continue

        # Eligibility failure
        if not eligible:
            applications.append({
                "application_id": application_id,
                "applicant_id": applicant.applicant_id,
                "cohort_id": None,
                "channel_id": random_channel()["channel_id"],
                "application_date": application_date,
                "eligibility_status": "Not Eligible",
                "interview_result": "Not Interviewed",
                "offer_status": "Not Offered",
                "application_status": "Rejected",
                "stage": "Eligibility",
                "exit_reason_id": random.choice(DOCUMENT_EXIT_REASONS)
            })
            application_id += 1
            continue

        # Interview failure
        if not interview_pass:
            applications.append({
                "application_id": application_id,
                "applicant_id": applicant.applicant_id,
                "cohort_id": None,
                "channel_id": random_channel()["channel_id"],
                "application_date": application_date,
                "eligibility_status": "Eligible",
                "interview_result": "Failed",
                "offer_status": "Not Offered",
                "application_status": "Rejected",
                "stage": "Interview",
                "exit_reason_id": random.choice(INTERVIEW_EXIT_REASONS)
            })
            application_id += 1
            continue

        # Interview passed — check available cohort capacity
        available = eligible_cohorts[
            eligible_cohorts.cohort_id.map(remaining_capacity) > 0
        ]

        # No available capacity
        if len(available) == 0:
            applications.append({
                "application_id": application_id,
                "applicant_id": applicant.applicant_id,
                "cohort_id": eligible_cohorts.iloc[0].cohort_id,
                "channel_id": random_channel()["channel_id"],
                "application_date": application_date,
                "eligibility_status": "Eligible",
                "interview_result": "Passed",
                "offer_status": "Not Offered",
                "application_status": "Rejected",
                "stage": "Selection",
                "exit_reason_id": random_selection_reason()
            })
            application_id += 1
            continue

        # Select a suitable cohort randomly
        selected_cohort = available.sample(1).iloc[0]

        # Selection — only selected candidates receive genuine offers
        if id(item) not in enrollment_candidates[application_year]:
            applications.append({
                "application_id": application_id,
                "applicant_id": applicant.applicant_id,
                "cohort_id": selected_cohort.cohort_id,
                "channel_id": random_channel()["channel_id"],
                "application_date": application_date,
                "eligibility_status": "Eligible",
                "interview_result": "Passed",
                "offer_status": "Not Offered",
                "application_status": "Rejected",
                "stage": "Selection",
                "exit_reason_id": random_selection_reason()
            })
            application_id += 1
            continue

        # Genuine offer
        offer_status = "Offered"
        stage = "Enrollment"

        if random.random() < OFFER_ACCEPTANCE_RATE:
            status = "Enrolled"
            exit_reason_id = None

            yearly_enrolled[application_year] += 1
            remaining_capacity[selected_cohort.cohort_id] -= 1
        else:
            status = "Rejected"
            exit_reason_id = random.choices(
                ENROLLMENT_DECLINE_REASONS,
                weights=DECLINE_WEIGHTS,
                k=1
            )[0]

        applications.append({
            "application_id": application_id,
            "applicant_id": applicant.applicant_id,
            "cohort_id": selected_cohort.cohort_id,
            "channel_id": random_channel()["channel_id"],
            "application_date": application_date,
            "eligibility_status": "Eligible",
            "interview_result": "Passed",
            "offer_status": offer_status,
            "application_status": status,
            "stage": stage,
            "exit_reason_id": exit_reason_id
        })
        application_id += 1

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------
    df = pd.DataFrame(applications)
    df.to_csv(DATA_DIR / "applications.csv", index=False)

    print(f"✓ applications.csv ({len(df)} records)")
    print("\nEnrollment Summary")

    total = 0
    for year in sorted(yearly_enrolled):
        print(f"{year}: {yearly_enrolled[year]}")
        total += yearly_enrolled[year]

    print(f"\nTOTAL ENROLLED = {total}")
    print(f"OVERALL RATE = {total / len(applicants):.1%}")

    return df
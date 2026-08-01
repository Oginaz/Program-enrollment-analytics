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

CHANNEL_WEIGHTS = [
    40,     # School Outreach
    15,     # Website
    18,     # Social Media
    10,     # Referral
    10,     # Community
    4,      # Career Fair
    3       # Partner
]

DOCUMENT_EXIT_REASONS = [1, 2, 3, 4]
INTERVIEW_EXIT_REASONS = [6, 7]
YEAR_TARGET_RATE = {

    2015: 0.28,
    2016: 0.26,
    2017: 0.24,
    2018: 0.22,
    2019: 0.20,

    2020: 0.18,

    2021: 0.16,

    2022: 0.15,
    2023: 0.15,
    2024: 0.15,
    2025: 0.15,
    2026: 0.15

}

def random_channel():
    return random.choices(
        APPLICATION_CHANNELS,
        weights=CHANNEL_WEIGHTS,
        k=1
    )[0]


def generate():

    applicants = pd.read_csv(
        DATA_DIR / "applicants.csv"
    )

    cohorts = pd.read_csv(
        DATA_DIR / "cohorts.csv"
    )

    # Remaining seats per cohort
    remaining_capacity = {
        row.cohort_id: row.capacity
        for _, row in cohorts.iterrows()
    }

    applications = []

    application_id = 1

    yearly_enrolled = {year: 0 for year in YEAR_TARGET_RATE}

    for _, applicant in applicants.iterrows():

        application_year = pd.to_datetime(
            applicant.registered_at
        ).year

        year_target = int(YEAR_CONFIGURATION[application_year]["applications"] * YEAR_TARGET_RATE[application_year])

        eligible_cohorts = cohorts[
            (cohorts.program_id == applicant.program_id)
            &
            (cohorts.year == application_year)
        ]

        if len(eligible_cohorts) == 0:
            continue

        available = eligible_cohorts[eligible_cohorts.cohort_id.map(remaining_capacity) > 0]

        if len(available) == 0:
            continue
        selected_cohort = available.sample(1).iloc[0]

        eligible = random.random() < 0.97

        interviewed = False

        interview_pass = False

        enrolled = False

        stage = "Eligibility"

        status = "Rejected"

        exit_reason = None

        interview_result = "Not Interviewed"

        offer_status = "Not Offered"

        # Eligibility
        if not eligible:

            stage = "Eligibility"

            exit_reason = random.choice(
                DOCUMENT_EXIT_REASONS
            )

        else:

            interviewed = True

            stage = "Interview"

            interview_pass = (
                random.random() < 0.85
            )

            if interview_pass:

                interview_result = "Passed"

            else:

                interview_result = "Failed"

            # Interview Failed
            if not interview_pass:

                exit_reason = random.choice(
                    INTERVIEW_EXIT_REASONS
                )

            else:

                offer_status = "Offered"

                stage = "Selection"

           
                # Capacity Check
                if (
                    yearly_enrolled[application_year] < year_target and remaining_capacity[selected_cohort.cohort_id] > 0 ):

                    status = "Enrolled"

                    enrolled = True

                    yearly_enrolled[application_year] += 1

                    remaining_capacity[
                        selected_cohort.cohort_id
                    ] -= 1

                else:

                    status = "Rejected"

                    exit_reason = 5

        application_date = pd.to_datetime(
            applicant.registered_at
        )

        applications.append({

            "application_id": application_id,

            "applicant_id": applicant.applicant_id,

            "cohort_id": selected_cohort.cohort_id,

            "channel_id": random_channel()["channel_id"],

            "application_date": application_date,

            "eligibility_status":
                "Eligible" if eligible else "Not Eligible",

            "interview_result":
                interview_result,

            "offer_status":
                offer_status,

            "application_status":
                status,

            "stage":
                stage,

            "exit_reason_id":
                exit_reason

        })

        application_id += 1

    df = pd.DataFrame(applications)

    df.to_csv(
        DATA_DIR / "applications.csv",
        index=False
    )

    print(
        f" applications.csv ({len(df)} records)"
    )

    print("\nEnrollment Summary")

    total = 0

    for year in sorted(yearly_enrolled):
        print(
        f"{year}: {yearly_enrolled[year]}")

        total += yearly_enrolled[year]

    print(f"\nTOTAL ENROLLED = {total}")

    return df
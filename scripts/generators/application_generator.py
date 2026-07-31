"""
==========================================================
PWANI TEKNOWGALZ
APPLICATION GENERATOR
==========================================================
"""

import random
from datetime import timedelta

import pandas as pd

from config import (
    DATA_DIR,
    RANDOM_SEED,
    APPLICATION_CHANNELS,
    EXIT_REASONS
)

random.seed(RANDOM_SEED)


APPLICATION_STATUSES = [

    "Rejected",

    "Enrolled"

]


CHANNEL_WEIGHTS = [

    40,     # School Outreach

    15,     # Website

    18,     # Social Media

    10,     # Referral

    10,     # Community

    4,      # Career Fair

    3       # Partner
]


def random_channel():

    return random.choices(

        APPLICATION_CHANNELS,

        weights=CHANNEL_WEIGHTS,

        k=1

    )[0]


def random_exit():

    return random.choice(EXIT_REASONS)


def generate():

    applicants = pd.read_csv(

        DATA_DIR / "applicants.csv"

    )

    cohorts = pd.read_csv(

        DATA_DIR / "cohorts.csv"

    )

    applications = []

    application_id = 1

    enrolled_counter = 0

    enrollment_target = int(

        len(applicants) * 0.15

    )

    for _, applicant in applicants.iterrows():

        eligible = random.random() < 0.90

        interviewed = False

        offer = False

        enrolled = False

        stage = "Eligibility"

        exit_reason = None

        cohort = cohorts[

            cohorts.program_id == applicant.program_id

        ]

        if len(cohort) == 0:

            continue

        selected_cohort = cohort.sample(1).iloc[0]

        if not eligible:

            status = "Rejected"

            stage = "Eligibility"

            exit_reason = random.choice(

                [1,2,3,4]

            )

        else:

            interviewed = True

            stage = "Interview"

            interview_pass = random.random() < 0.35

            if not interview_pass:

                status = "Rejected"

                exit_reason = random.choice(

                    [6,7]

                )

            else:

                offer = True

                stage = "Offer"

                accepted = (

                    enrolled_counter

                    < enrollment_target

                )

                if accepted:

                    enrolled = True

                    status = "Enrolled"

                    exit_reason = None

                    enrolled_counter += 1

                else:

                    status = "Rejected"

                    stage = "Selection"

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

            "eligibility_status": "Eligible" if eligible else "Not Eligible",

            "interview_result": "Passed" if interviewed else "Not Interviewed",

            "offer_status": "Accepted" if offer else "Not Offered",

            "application_status": status,

            "stage": stage,

            "exit_reason_id": exit_reason

        })

        application_id += 1

    df = pd.DataFrame(applications)

    df.to_csv(

        DATA_DIR / "applications.csv",

        index=False

    )

    print(

        f"✓ applications.csv ({len(df)} records)"

    )

    print(

        f"Total Enrolled = {enrolled_counter}"

    )

    return df
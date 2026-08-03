"""
PWANI TEKNOWGALZ
ENROLLMENT GENERATOR
"""

from datetime import datetime, timedelta
import random

import pandas as pd

from config import DATA_DIR, RANDOM_SEED

random.seed(RANDOM_SEED)

# Dataset snapshot date
CURRENT_DATE = datetime(2026, 8, 1)


def generate():

    applications = pd.read_csv(
        DATA_DIR / "applications.csv"
    )

    cohorts = pd.read_csv(
        DATA_DIR / "cohorts.csv"
    )

    enrollments = []
    enrollment_id = 1

    for _, application in applications.iterrows():

        if application["application_status"] != "Enrolled":
            continue

        application_date = pd.to_datetime(
            application["application_date"]
        )

        cohort = cohorts[
            cohorts["cohort_id"] == application["cohort_id"]
        ].iloc[0]

        start_date = pd.to_datetime(
            cohort["start_date"]
        )

        end_date = pd.to_datetime(
            cohort["end_date"]
        )

        # Enrollment occurs shortly after application,
        # but never before cohort start or after the snapshot date.
        enrollment_date = max(
            application_date + timedelta(days=random.randint(3, 14)),
            start_date
        )

        enrollment_date = min(
            enrollment_date,
            CURRENT_DATE
        )

        # Determine whether the cohort has finished
        cohort_finished = end_date <= CURRENT_DATE

        if cohort_finished:

            completion_status = random.choices(
                ["Completed", "Withdrawn"],
                weights=[92, 8],
                k=1
            )[0]

            if completion_status == "Completed":

                completion_date = min(
                    end_date + timedelta(days=random.randint(0, 5)),
                    CURRENT_DATE
                )

            else:

                withdrawal_date = (
                    enrollment_date +
                    timedelta(days=random.randint(5, 60))
                )

                completion_date = min(
                    withdrawal_date,
                    end_date,
                    CURRENT_DATE
                )

        else:

            completion_status = random.choices(
                ["Ongoing", "Withdrawn"],
                weights=[90, 10],
                k=1
            )[0]

            if completion_status == "Ongoing":

                completion_date = None

            else:

                withdrawal_date = (
                    enrollment_date +
                    timedelta(days=random.randint(5, 60))
                )

                completion_date = min(
                    withdrawal_date,
                    end_date,
                    CURRENT_DATE
                )

        enrollments.append({

            "enrollment_id": enrollment_id,

            "application_id": application["application_id"],

            "enrollment_date": enrollment_date.date(),

            "completion_status": completion_status,

            "completion_date": (
                completion_date.date()
                if completion_date is not None
                else None
            )

        })

        enrollment_id += 1

    df = pd.DataFrame(enrollments)

    df.to_csv(
        DATA_DIR / "enrollments.csv",
        index=False
    )

    print(f"✓ enrollments.csv ({len(df)} records)")

    return df
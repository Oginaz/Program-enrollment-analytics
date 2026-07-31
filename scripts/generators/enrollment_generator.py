"""
==========================================================
PWANI TEKNOWGALZ
ENROLLMENT GENERATOR
==========================================================
"""

from datetime import timedelta
import random

import pandas as pd

from config import DATA_DIR, RANDOM_SEED

random.seed(RANDOM_SEED)


def generate():

    applications = pd.read_csv(
        DATA_DIR / "applications.csv"
    )

    enrollments = []

    enrollment_id = 1

    for _, application in applications.iterrows():

        if application["application_status"] != "Enrolled":
            continue

        application_date = pd.to_datetime(
            application["application_date"]
        )

        enrollment_date = (
            application_date
            + timedelta(days=random.randint(7, 30))
        )

        completion_probability = random.random()

        if completion_probability <= 0.88:
            completion_status = "Completed"
        elif completion_probability <= 0.95:
            completion_status = "Ongoing"
        else:
            completion_status = "Withdrawn"

        enrollments.append({

            "enrollment_id": enrollment_id,

            "application_id": application["application_id"],

            "enrollment_date": enrollment_date.date(),

            "completion_status": completion_status

        })

        enrollment_id += 1

    df = pd.DataFrame(enrollments)

    df.to_csv(
        DATA_DIR / "enrollments.csv",
        index=False
    )

    print(f"✓ enrollments.csv ({len(df)} records)")

    return df
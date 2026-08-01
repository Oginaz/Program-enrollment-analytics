"""
PWANI TEKNOWGALZ
RESOURCE ALLOCATION GENERATOR
"""

import random

import pandas as pd

from config import DATA_DIR, RANDOM_SEED

random.seed(RANDOM_SEED)


def generate():

    enrollments = pd.read_csv(
        DATA_DIR / "enrollments.csv"
    )

    applications = pd.read_csv(
        DATA_DIR / "applications.csv"
    )

    cohorts = pd.read_csv(
        DATA_DIR / "cohorts.csv"
    )

    # Merge to obtain each participant's cohort
    merged = enrollments.merge(
        applications[["application_id", "cohort_id"]],
        on="application_id"
    )

    merged = merged.merge(
        cohorts[["cohort_id", "delivery_mode"]],
        on="cohort_id"
    )

    allocations = []

    allocation_id = 1

    for _, row in merged.iterrows():

        enrollment_id = row["enrollment_id"]
        mode = row["delivery_mode"]

        resources = []

        # Resources given to everyone
        resources.extend([3, 7, 8])      # Manual, Mentorship, T-Shirt

        # Delivery-mode resources
        if mode == "Online":

            resources.append(2)          # Internet Bundle

        elif mode == "Hybrid":

            resources.extend([
                2,      # Internet
                4       # Stationery
            ])

            if random.random() < 0.60:
                resources.append(5)      # Meals

            if random.random() < 0.40:
                resources.append(6)      # Transport

        else:   # Physical

            resources.extend([
                4,      # Stationery
                5       # Meals
            ])

            if random.random() < 0.80:
                resources.append(6)      # Transport

        # Laptop support (limited)
        if random.random() < 0.25:
            resources.append(1)

        # Remove duplicates
        resources = sorted(set(resources))

        for resource_id in resources:

            allocations.append({

                "allocation_id": allocation_id,

                "enrollment_id": enrollment_id,

                "resource_id": resource_id,

                "quantity": 1

            })

            allocation_id += 1

    df = pd.DataFrame(allocations)

    df.to_csv(
        DATA_DIR / "resource_allocations.csv",
        index=False
    )

    print(
        f"✓ resource_allocations.csv ({len(df)} records)"
    )

    return df
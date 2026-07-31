"""
PWANI TEKNOWGALZ
RESOURCE ALLOCATION GENERATOR
"""

import random

import pandas as pd

from config import DATA_DIR, RANDOM_SEED

random.seed(RANDOM_SEED)


RESOURCE_PROBABILITIES = {

    1:0.35,     # Laptop

    2:1.00,     # Internet

    3:1.00,     # Manual

    4:1.00,     # Stationery

    5:0.55,     # Meals

    6:0.30,     # Transport

    7:1.00,     # Mentorship

    8:0.90      # T-Shirt

}


def generate():

    enrollments = pd.read_csv(

        DATA_DIR / "enrollments.csv"

    )

    allocations = []

    allocation_id = 1

    for _, enrollment in enrollments.iterrows():

        for resource_id, probability in RESOURCE_PROBABILITIES.items():

            if random.random() <= probability:

                allocations.append({

                    "allocation_id": allocation_id,

                    "enrollment_id": enrollment["enrollment_id"],

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

        f" resource_allocations.csv ({len(df)} records)"

    )

    return df
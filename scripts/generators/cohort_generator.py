"""
COHORT GENERATOR
"""

from datetime import datetime
from pathlib import Path
import random

import pandas as pd

from config import (
    DATA_DIR,
    YEAR_CONFIGURATION,
    PROGRAMS,
    COUNTIES,
    RANDOM_SEED
)

random.seed(RANDOM_SEED)


PROGRAM_LOOKUP = {}

for p in PROGRAMS:
    PROGRAM_LOOKUP[p["program_id"]] = p


def generate():

    cohorts = []

    cohort_id = 1

    for year in sorted(YEAR_CONFIGURATION.keys()):

        config = YEAR_CONFIGURATION[year]

        active_programs = [
            p for p in PROGRAMS
            if p["launch_year"] <= year
        ]

        if len(active_programs) == 0:
            continue

        cohorts_per_program = max(
            1,
            config["cohorts"] // len(active_programs)
        )

        for program in active_programs:

            prefix = "".join(
                word[0]
                for word in program["program_name"].split()
            ).upper()

            for number in range(1, cohorts_per_program + 1):

                county = random.choice(COUNTIES)

                start_date = datetime(
                    year,
                    random.randint(1, 10),
                    random.randint(1, 20)
                )

                end_date = start_date.replace(
                    month=min(start_date.month + 2, 12)
                )

                cohorts.append({

                    "cohort_id": cohort_id,

                    "program_id": program["program_id"],

                    "county_id": county["county_id"],

                    "cohort_name": f"{prefix}-{year}-{number:02}",

                    "capacity": config["capacity_per_cohort"],

                    "delivery_mode": config["delivery"],

                    "start_date": start_date.date(),

                    "end_date": end_date.date()

                })

                cohort_id += 1

    df = pd.DataFrame(cohorts)

    df.to_csv(
        DATA_DIR / "cohorts.csv",
        index=False
    )

    print(f"✓ cohorts.csv ({len(df)} records)")

    return df
"""
COHORT GENERATOR
"""

from datetime import datetime
import random

import pandas as pd

from config import (
    DATA_DIR,
    YEAR_CONFIGURATION,
    PROGRAMS,
    COUNTIES,
    COUNTY_WEIGHTS,
    RANDOM_SEED
)

random.seed(RANDOM_SEED)

PROGRAM_LOOKUP = {
    p["program_id"]: p
    for p in PROGRAMS
}


def weighted_county():

    county_id = random.choices(

        list(COUNTY_WEIGHTS.keys()),

        weights=list(COUNTY_WEIGHTS.values()),

        k=1

    )[0]

    return next(

        county

        for county in COUNTIES

        if county["county_id"] == county_id

    )


def generate():

    cohorts = []

    cohort_id = 1

    for year in sorted(YEAR_CONFIGURATION.keys()):

        config = YEAR_CONFIGURATION[year]

        active_programs = [

            p

            for p in PROGRAMS

            if p["launch_year"] <= year

        ]

        if not active_programs:
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

                county = weighted_county()

                start_date = datetime(

                    year,

                    random.randint(1, 10),

                    random.randint(1, 20)

                )

                end_month = min(start_date.month + 2, 12)

                end_date = start_date.replace(

                    month=end_month

                )

                cohorts.append({

                    "cohort_id": cohort_id,

                    "program_id": program["program_id"],

                    "county_id": county["county_id"],

                    "year": year,

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

    print(

        f"✓ cohorts.csv ({len(df)} records)"

    )

    return df
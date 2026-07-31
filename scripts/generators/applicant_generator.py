"""
PWANI TEKNOWGALZ
APPLICANT GENERATOR
"""

import random
from datetime import datetime

import pandas as pd
from faker import Faker

from config import (
    DATA_DIR,
    RANDOM_SEED,
    FAKER_LOCALE,
    COUNTIES,
    PROGRAMS,
    YEAR_CONFIGURATION
)

fake = Faker(FAKER_LOCALE)

random.seed(RANDOM_SEED)
Faker.seed(RANDOM_SEED)



# LOOKUP VALUES


EDUCATION_LEVELS = [
    "Primary",
    "Secondary",
    "TVET",
    "University"
]

EMPLOYMENT_STATUS = [
    "Student",
    "Unemployed",
    "Self-employed"
]

DISABILITY = [
    "Yes",
    "No"
]

GENDERS = [
    "Female"
]



# HELPER FUNCTIONS


def weighted_program(year):

    available = [
        p for p in PROGRAMS
        if p["launch_year"] <= year
    ]

    return random.choice(available)


def weighted_county():

    weights = [

        35,     # Mombasa

        25,     # Kilifi

        15,     # Kwale

        10,     # Taita Taveta

        8,      # Lamu

        7       # Tana River

    ]

    return random.choices(
        COUNTIES,
        weights=weights,
        k=1
    )[0]


def random_phone():

    prefixes = [
        "070",
        "071",
        "072",
        "074",
        "075",
        "079",
        "010",
        "011"
    ]

    return (
        random.choice(prefixes)
        + "".join(
            str(random.randint(0,9))
            for _ in range(7)
        )
    )


def random_birthdate(year):

    minimum_age = 15

    maximum_age = 30

    birth_year = random.randint(

        year - maximum_age,

        year - minimum_age

    )

    month = random.randint(1,12)

    day = random.randint(1,28)

    return datetime(

        birth_year,

        month,

        day

    ).date()
# MAIN GENERATOR


def generate():

    applicants = []

    applicant_id = 1

    for year in YEAR_CONFIGURATION:

        yearly_target = YEAR_CONFIGURATION[year]["applications"]

        print(
            f"Generating {yearly_target} applicants for {year}"
        )

        for _ in range(yearly_target):

            county = weighted_county()

            program = weighted_program(year)

            first_name = fake.first_name_female()

            last_name = fake.last_name()

            email = (

                first_name.lower()

                + "."

                + last_name.lower()

                + str(random.randint(1,999))

                + "@gmail.com"

            )

            applicants.append({

                "applicant_id": applicant_id,

                "first_name": first_name,

                "last_name": last_name,

                "gender": "Female",

                "date_of_birth": random_birthdate(year),

                "phone_number": random_phone(),

                "email": email,

                "county_id": county["county_id"],

                "education_level": random.choices(

                    EDUCATION_LEVELS,

                    weights=[15,55,15,15]

                )[0],

                "employment_status": random.choices(

                    EMPLOYMENT_STATUS,

                    weights=[75,20,5]

                )[0],

                "disability_status": random.choices(

                    DISABILITY,

                    weights=[3,97]

                )[0],

                "program_id": program["program_id"],

                "registered_at": datetime(

                    year,

                    random.randint(1,12),

                    random.randint(1,28)

                ).date()

            })

            applicant_id += 1

    df = pd.DataFrame(applicants)

    df.to_csv(

        DATA_DIR / "applicants.csv",

        index=False

    )

    print(

        f" applicants.csv ({len(df)} records)"

    )

    return df
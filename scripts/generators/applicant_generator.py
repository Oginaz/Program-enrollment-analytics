"""
PWANI TEKNOWGALZ
APPLICANT GENERATOR
"""

import random
from datetime import datetime

import pandas as pd

from config import (
    DATA_DIR,
    RANDOM_SEED,
    COUNTIES,
    COUNTY_WEIGHTS,
    PROGRAMS,
    PROGRAM_DISTRIBUTION,
    YEAR_CONFIGURATION
)

random.seed(RANDOM_SEED)

FIRST_NAMES = [
    "Amina","Halima","Fatuma","Saumu","Aisha",
    "Mwanajuma","Mariam","Zainabu","Salma","Mishi",
    "Neema","Joyce","Faith","Mercy","Brenda",
    "Purity","Christine","Caroline","Rose","Grace",
    "Janet","Sharon","Sheila","Dorcas","Esther",
    "Ann","Lydia","Agnes","Diana","Cynthia"
]

LAST_NAMES = [
    "Juma","Mwajuma","Mwakio","Mwandawiro",
    "Mwashumbe","Mghoi","Kazungu","Kombe",
    "Baya","Kenga","Munga","Mwadime",
    "Mwangeka","Masha","Mutiso","Kioko",
    "Musyoka","Odhiambo","Achieng","Otieno",
    "Omondi","Njeri","Wambui","Chebet",
    "Kemunto"
]

PHONE_PREFIXES = [
    "070","071","072","073","074",
    "075","076","077","078","079",
    "010","011"
]

EDUCATION_LEVELS = [
    "Primary",
    "Secondary",
    "TVET",
    "University"
]

INCOME_LEVELS = [
    "Low",
    "Lower-Middle",
    "Middle",
    "Upper-Middle"
]

GENDERS = ["Female"]


# HELPER FUNCTIONS
def weighted_program(year):

    distribution = PROGRAM_DISTRIBUTION[year]
    program_ids = list(distribution.keys())
    weights = list(distribution.values())

    selected_id = random.choices(
        program_ids,
        weights=weights,
        k=1
    )[0]

    return next(
        program
        for program in PROGRAMS
        if program["program_id"] == selected_id
    )


def weighted_county():

    county_ids = list(COUNTY_WEIGHTS.keys())
    weights = list(COUNTY_WEIGHTS.values())

    selected = random.choices(
        county_ids,
        weights=weights,
        k=1
    )[0]

    return next(
        county
        for county in COUNTIES
        if county["county_id"] == selected
    )


def random_phone():

    prefix = random.choice(PHONE_PREFIXES)
    suffix = "".join(str(random.randint(0, 9)) for _ in range(7))

    return prefix + suffix


def random_birthdate(year):

    minimum_age = 17
    maximum_age = 28

    birth_year = random.randint(
        year - maximum_age,
        year - minimum_age
    )

    month = random.randint(1, 12)
    day = random.randint(1, 28)

    return datetime(birth_year, month, day).date()


# MAIN GENERATOR
def generate():

    applicants = []
    applicant_id = 1

    for year in YEAR_CONFIGURATION:

        yearly_target = YEAR_CONFIGURATION[year]["applications"]

        print(f"Generating {yearly_target} applicants for {year}")

        for _ in range(yearly_target):

            county = weighted_county()
            program = weighted_program(year)

            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)

            email = (
                first_name.lower()
                #+ "."
                + last_name.lower()
                + str(random.randint(100, 999))
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
                    weights=[15, 55, 15, 15]
                )[0],
                "income_level": random.choices(
                    INCOME_LEVELS,
                    weights=[45, 30, 18, 7]   # skewed low, matching marginalized-community target population
                )[0],
                "device_ownership": random.choices(
                    [True, False],
                    weights=[45, 55]           # device access is a known constraint per Close the Gap partnership research
                )[0],
                "program_id": program["program_id"],
                "registered_at": datetime(
                    year,
                    random.randint(1, 12),
                    random.randint(1, 28)
                ).date()
            })

            applicant_id += 1

    df = pd.DataFrame(applicants)

    df.to_csv(
        DATA_DIR / "applicants.csv",
        index=False
    )

    print(f"✓ applicants.csv ({len(df)} records)")

    return df
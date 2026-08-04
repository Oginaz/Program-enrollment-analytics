"""
PWANI TEKNOWGALZ
RESOURCE ALLOCATION GENERATOR
"""

import random

import pandas as pd

from config import DATA_DIR, RANDOM_SEED

random.seed(RANDOM_SEED)

# Which resources apply to which delivery mode, and how tightly constrained
# availability tends to be relative to what's needed (ratio range = % of need actually met).
RESOURCE_RULES = {
    1: {"applies": "all",                    "avail_ratio": (0.35, 0.55)},  # Laptop — scarce, shared
    2: {"applies": ["Online", "Hybrid"],     "avail_ratio": (0.70, 0.90)},  # Internet Bundle
    3: {"applies": "all",                    "avail_ratio": (0.90, 1.00)},  # Training Manual
    4: {"applies": ["Physical", "Hybrid"],   "avail_ratio": (0.85, 1.00)},  # Stationery
    5: {"applies": ["Physical", "Hybrid"],   "avail_ratio": (0.75, 0.95)},  # Meals
    6: {"applies": ["Physical", "Hybrid"],   "avail_ratio": (0.50, 0.80)},  # Transport Support
    7: {"applies": "all",                    "avail_ratio": (0.90, 1.00)},  # Mentorship
    8: {"applies": "all",                    "avail_ratio": (0.80, 1.00)},  # Branded T-Shirt
}


def generate():
    """
    Per-cohort resource allocation  the CAPACITY CONSTRAINT signal.
    Answers: did this cohort have enough of resource  to meet its capacity?
    Exists independent of who actually enrolled.
    """

    cohorts = pd.read_csv(DATA_DIR / "cohorts.csv")

    allocations = []
    allocation_id = 1

    for _, cohort in cohorts.iterrows():

        quantity_needed = cohort["capacity"]

        for resource_id, rule in RESOURCE_RULES.items():

            applies = rule["applies"]

            if applies != "all" and cohort["delivery_mode"] not in applies:
                continue

            low, high = rule["avail_ratio"]
            ratio = random.uniform(low, high)

            quantity_available = max(0, round(quantity_needed * ratio))

            allocations.append({
                "allocation_id": allocation_id,
                "cohort_id": cohort["cohort_id"],
                "resource_id": resource_id,
                "quantity_needed": quantity_needed,
                "quantity_available": quantity_available,
                "allocation_date": cohort["start_date"],
            })

            allocation_id += 1

    df = pd.DataFrame(allocations)

    df.to_csv(
        DATA_DIR / "resource_allocations.csv",
        index=False
    )

    print(f"✓ resource_allocations.csv ({len(df)} records)")

    return df


def generate_participant_resources():
    """
    Per-enrollment resource issuance — the IMPACT record.
    Answers: what did this specific enrolled participant actually receive?
    Kept separate from resource_allocations() rather than overloading one
    table to answer two different questions.
    """

    enrollments = pd.read_csv(DATA_DIR / "enrollments.csv")
    applications = pd.read_csv(DATA_DIR / "applications.csv")
    cohorts = pd.read_csv(DATA_DIR / "cohorts.csv")

    merged = enrollments.merge(
        applications[["application_id", "cohort_id"]],
        on="application_id"
    ).merge(
        cohorts[["cohort_id", "delivery_mode"]],
        on="cohort_id"
    )

    records = []
    record_id = 1

    for _, row in merged.iterrows():

        mode = row["delivery_mode"]
        resources = [3, 7, 8]  # Manual, Mentorship, T-Shirt — given to everyone

        if mode == "Online":
            resources.append(2)
        elif mode == "Hybrid":
            resources.extend([2, 4])
            if random.random() < 0.60:
                resources.append(5)
            if random.random() < 0.40:
                resources.append(6)
        else:  # Physical
            resources.extend([4, 5])
            if random.random() < 0.80:
                resources.append(6)

        if random.random() < 0.25:
            resources.append(1)  # Laptop — limited

        for resource_id in sorted(set(resources)):

            records.append({
                "participant_resource_id": record_id,
                "enrollment_id": row["enrollment_id"],
                "resource_id": resource_id,
                "quantity": 1,
            })

            record_id += 1

    df = pd.DataFrame(records)

    df.to_csv(
        DATA_DIR / "participant_resources.csv",
        index=False
    )

    print(f"participant_resources.csv ({len(df)} records)")

    return df
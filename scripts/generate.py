"""
PWANI TEKNOWGALZ SYNTHETIC DATA GENERATOR
"""

from generators.lookup_generator import generate as lookup
from generators.cohort_generator import generate as cohorts
from generators.applicant_generator import generate as applicants
from generators.application_generator import generate as applications
from generators.enrollment_generator import generate as enrollments
from generators.allocation_generator import generate as allocations
from generators.allocation_generator import generate_participant_resources as participant_resources

import time


def run_step(title, function):

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    start = time.time()
    function()
    elapsed = time.time() - start

    print(f"Completed in {elapsed:.2f} seconds")


def main():

    print("=" * 70)
    print("PWANI TEKNOWGALZ SYNTHETIC DATA GENERATOR")
    print("=" * 70)

    run_step("SPRINT 1 - LOOKUP TABLES", lookup)
    run_step("SPRINT 2 - COHORTS", cohorts)
    run_step("SPRINT 3 - APPLICANTS", applicants)
    run_step("SPRINT 4 - APPLICATIONS", applications)
    run_step("SPRINT 5 - ENROLLMENTS", enrollments)
    run_step("SPRINT 6 - RESOURCE ALLOCATIONS (per cohort)", allocations)
    run_step("SPRINT 7 - PARTICIPANT RESOURCES (per enrollment)", participant_resources)

    print("\n" + "=" * 70)
    print("ALL DATASETS GENERATED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()
"""
==========================================================
PWANI TEKNOWGALZ SYNTHETIC DATA GENERATOR
==========================================================
"""

from generators.lookup_generator import generate as lookup

from generators.cohort_generator import generate as cohorts

from generators.applicant_generator import generate as applicants

from generators.application_generator import generate as applications

from generators.enrollment_generator import generate as enrollments

from generators.allocation_generator import generate as allocations


def main():

    print("="*70)
    print("PWANI TEKNOWGALZ SYNTHETIC DATA GENERATOR")
    print("="*70)

    print("\nSprint 1")
    lookup()

    print("\nSprint 2")
    cohorts()

    print("\nSprint 3")
    applicants()

    print("\nSprint 4")
    applications()

    print("\nSprint 5")
    enrollments()

    print("\nSprint 6")
    allocations()

    print("\n" + "="*70)
    print("DATASET GENERATION COMPLETED SUCCESSFULLY")
    print("="*70)


if __name__ == "__main__":
    main()
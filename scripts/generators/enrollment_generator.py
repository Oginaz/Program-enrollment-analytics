"""
PWANI TEKNOWGALZ
ENROLLMENT GENERATOR
"""

from datetime import datetime, timedelta
import random

import pandas as pd

from config import DATA_DIR, RANDOM_SEED

random.seed(RANDOM_SEED)

# Dataset snapshot date
CURRENT_DATE = datetime(2026, 8, 1)


def generate():
    applications = pd.read_csv(DATA_DIR / "applications.csv")
    cohorts = pd.read_csv(DATA_DIR / "cohorts.csv")

    # Ensure dates are datetime
    applications["application_date"] = pd.to_datetime(applications["application_date"])
    cohorts["start_date"] = pd.to_datetime(cohorts["start_date"])
    cohorts["end_date"] = pd.to_datetime(cohorts["end_date"])

    enrollments = []
    enrollment_id = 1

    # Process ONLY applications marked Enrolled
    enrolled_applications = applications[applications["application_status"] == "Enrolled"]

    # Validate that every enrolled application has a cohort
    missing_cohort = enrolled_applications[enrolled_applications["cohort_id"].isna()]

    if len(missing_cohort) > 0:
        raise ValueError(f"{len(missing_cohort)} enrolled applications have no cohort_id.")

    # ---------------------------------------------------------
    # Generate enrollment records
    # ---------------------------------------------------------
    for _, application in enrolled_applications.iterrows():
        application_id = application["application_id"]
        application_date = pd.to_datetime(application["application_date"])

        cohort_matches = cohorts[cohorts["cohort_id"] == application["cohort_id"]]

        # Every enrolled application must have a valid cohort
        if len(cohort_matches) == 0:
            raise ValueError(
                f"Application {application_id} is marked Enrolled but cohort "
                f"{application['cohort_id']} does not exist."
            )

        cohort = cohort_matches.iloc[0]
        start_date = pd.to_datetime(cohort["start_date"])
        end_date = pd.to_datetime(cohort["end_date"])


        # Enrollment date
        enrollment_start = max(application_date, start_date)

        if enrollment_start > CURRENT_DATE:
            raise ValueError(
                f"Application {application_id} is marked Enrolled but its "
                f"cohort has not started by {CURRENT_DATE.date()}."
            )

        enrollment_date = enrollment_start + timedelta(days=random.randint(3, 14))
        enrollment_date = min(enrollment_date, CURRENT_DATE)  # never exceed snapshot

        # Safety validation
        if enrollment_date < application_date:
            raise ValueError(
                f"Application {application_id}: enrollment date occurs before application date."
            )

        if enrollment_date < start_date:
            raise ValueError(
                f"Application {application_id}: enrollment date occurs before cohort start."
            )

        # -----------------------------------------------------
        # Completion status
        # -----------------------------------------------------
        cohort_finished = end_date <= CURRENT_DATE

        if cohort_finished:
            completion_status = random.choices(
                ["Completed", "Withdrawn"], weights=[92, 8], k=1
            )[0]

            if completion_status == "Completed":
                completion_date = min(
                    end_date + timedelta(days=random.randint(0, 5)),
                    CURRENT_DATE
                )
                # Safety: completion cannot precede enrollment
                completion_date = max(completion_date, enrollment_date)
            else:
                completion_date = _resolve_withdrawal_date(
                    enrollment_date, end_date, CURRENT_DATE
                )

        else:
            completion_status = random.choices(
                ["Ongoing", "Withdrawn"], weights=[90, 10], k=1
            )[0]

            if completion_status == "Ongoing":
                completion_date = None
            else:
                completion_date = _resolve_withdrawal_date(
                    enrollment_date, end_date, CURRENT_DATE
                )

        # Final completion-date validation
        if completion_date is not None:
            if completion_date < enrollment_date:
                raise ValueError(
                    f"Application {application_id}: completion date occurs before enrollment."
                )
            if completion_date > CURRENT_DATE:
                raise ValueError(
                    f"Application {application_id}: completion date exceeds dataset snapshot."
                )

        enrollments.append({
            "enrollment_id": enrollment_id,
            "application_id": application_id,
            "enrollment_date": enrollment_date.date(),
            "completion_status": completion_status,
            "completion_date": completion_date.date() if completion_date is not None else None
        })

        enrollment_id += 1

    # Final integrity check
    if len(enrollments) != len(enrolled_applications):
        raise ValueError(
            "Enrollment record count does not match applications marked Enrolled."
        )

    # Save
    df = pd.DataFrame(enrollments)
    df.to_csv(DATA_DIR / "enrollments.csv", index=False)

    print(f"✓ enrollments.csv ({len(df)} records)")
    print(f"✓ Enrolled applications processed: {len(enrolled_applications)}")
    print(f"✓ Enrollment records created: {len(df)}")
    print("✓ Enrollment integrity check passed")

    return df


def _resolve_withdrawal_date(enrollment_date, end_date, current_date):
    """
    Pick a withdrawal date on/after enrollment, bounded by the
    cohort end date and the dataset snapshot.
    """
    latest_withdrawal = min(end_date, current_date)
    earliest_withdrawal = enrollment_date + timedelta(days=5)

    if earliest_withdrawal <= latest_withdrawal:
        withdrawal_date = earliest_withdrawal + timedelta(days=random.randint(0, 30))
        return min(withdrawal_date, latest_withdrawal)

    # If the cohort is already near completion,
    # withdrawal happens on/after enrollment.
    completion_date = min(latest_withdrawal, current_date)
    return max(completion_date, enrollment_date)
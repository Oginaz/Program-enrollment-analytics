from pathlib import Path

import pandas as pd

from config import (
    DATA_DIR,
    COUNTIES,
    APPLICATION_CHANNELS,
    EXIT_REASONS,
    RESOURCES,
    PROGRAMS,
)


def save_csv(data, filename):
    """
    Save a list of dictionaries as CSV.
    """
    df = pd.DataFrame(data)

    output_path = DATA_DIR / filename

    df.to_csv(output_path, index=False)

    print(f"✓ {filename} ({len(df)} records)")


def generate():

    print("\nGenerating lookup tables...")

    save_csv(COUNTIES, "counties.csv")

    save_csv(APPLICATION_CHANNELS, "application_channels.csv")

    save_csv(EXIT_REASONS, "exit_reasons.csv")

    save_csv(RESOURCES, "resources.csv")

    save_csv(PROGRAMS, "programs.csv")

    print("Lookup tables completed.\n")
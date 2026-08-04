"""
PWANI TEKNOWGALZ SYNTHETIC DATA GENERATOR
Configuration File
"""

from pathlib import Path



PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

DATA_DIR.mkdir(exist_ok=True)

RANDOM_SEED = 42

# DATE RANGE
YEARS = list(range(2015, 2027))

# TARGETS
TOTAL_APPLICATIONS = 20543

CURRENT_ENROLLMENT_RATE = 0.15
TARGET_ENROLLMENT_RATE = 0.50

# FAKER
FAKER_LOCALE = "en_KE"

# COUNTIES
COUNTIES = [
    {"county_id": 1, "county_name": "Mombasa", "region": "Coast"},
    {"county_id": 2, "county_name": "Kilifi", "region": "Coast"},
    {"county_id": 3, "county_name": "Kwale", "region": "Coast"},
    {"county_id": 4, "county_name": "Taita Taveta", "region": "Coast"},
    {"county_id": 5, "county_name": "Lamu", "region": "Coast"},
    {"county_id": 6, "county_name": "Tana River", "region": "Coast"},
]
COUNTY_WEIGHTS = {

    1: 32,   # Mombasa
    2: 26,   # Kilifi
    3: 18,   # Kwale
    4: 10,   # Taita Taveta
    5: 8,    # Tana River
    6: 6     # Lamu

}

# APPLICATION CHANNELS
APPLICATION_CHANNELS = [
    {"channel_id": 1, "channel_name": "School Outreach"},
    {"channel_id": 2, "channel_name": "Website"},
    {"channel_id": 3, "channel_name": "Social Media"},
    {"channel_id": 4, "channel_name": "Referral"},
    {"channel_id": 5, "channel_name": "Community Outreach"},
    {"channel_id": 6, "channel_name": "Career Fair"},
    {"channel_id": 7, "channel_name": "Partner Organization"},
]


# EXIT REASONS
EXIT_REASONS = [
    {"exit_reason_id": 1, "stage": "Eligibility", "reason": "Did not meet eligibility requirements"},
    {"exit_reason_id": 2, "stage": "Eligibility", "reason": "Incomplete application"},
    {"exit_reason_id": 3, "stage": "Eligibility", "reason": "Missing required documents"},
    {"exit_reason_id": 4, "stage": "Eligibility", "reason": "Application submitted after deadline"},
    {"exit_reason_id": 5, "stage": "Selection", "reason": "Cohort reached capacity"},
    {"exit_reason_id": 6, "stage": "Interview", "reason": "Interview not attended"},
    {"exit_reason_id": 7, "stage": "Interview", "reason": "Interview unsuccessful"},
    {"exit_reason_id": 8, "stage": "Offer", "reason": "Offer declined"},
    {"exit_reason_id": 9, "stage": "Enrollment", "reason": "Failed to confirm enrollment"},
    {"exit_reason_id": 10, "stage": "Enrollment", "reason": "Withdrew voluntarily"},
]

RESOURCES = [
    {"resource_id": 1, "resource_name": "Laptop", "unit_cost": 25000.00, "description": "Laptop issued to participant"},
    {"resource_id": 2, "resource_name": "Internet Bundle", "unit_cost": 3000.00, "description": "Internet connectivity support"},
    {"resource_id": 3, "resource_name": "Training Manual", "unit_cost": 500.00, "description": "Training manual"},
    {"resource_id": 4, "resource_name": "Stationery", "unit_cost": 300.00, "description": "Training stationery"},
    {"resource_id": 5, "resource_name": "Meals", "unit_cost": 4800.00, "description": "Meals during training"},
    {"resource_id": 6, "resource_name": "Transport Support", "unit_cost": 3600.00, "description": "Transport facilitation"},
    {"resource_id": 7, "resource_name": "Mentorship", "unit_cost": 2000.00, "description": "Mentorship support"},
    {"resource_id": 8, "resource_name": "Branded T-Shirt", "unit_cost": 700.00, "description": "Official programme T-shirt"},
]

# PROGRAMS
PROGRAMS = [
    {
        "program_id": 1,
        "program_name": "Technovation Challenge",
        "description": "Technovation Challenge programme",
        "launch_year": 2015      # Verified — Ruth Kaveke: "launched in 2015, Mombasa region"
    },
    {
        "program_id": 2,
        "program_name": "Mombasa Girls in STEM",
        "description": "TechWomen Kenya alumnae partnership project",
        "launch_year": 2016      # Verified — Phase 1 2016, Phase 2 2018
    },
    {
        "program_id": 3,
        "program_name": "Django Girls Mombasa",
        "description": "Django Girls workshops",
        "launch_year": 2017      # Verified — first workshop, February 2017
    },
    {
        "program_id": 4,
        "program_name": "STEM Cafe Kenya",
        "description": "Multi-region STEM outreach programme",
        "launch_year": 2019      # Verified — target of 135 across 5 regions
    },
    {
        "program_id": 5,
        "program_name": "CodeHack",
        "description": "CodeHack programme",
        "launch_year": 2020      # Verified — first cohort was the "COVID-19 Edition"
    },
    {
        "program_id": 6,
        "program_name": "AjiraForShe",
        "description": "AjiraForShe apprenticeship programme",
        "launch_year": 2024      # Verified active by mid-2024 — exact launch year not confirmed
    },
    {
        "program_id": 7,
        "program_name": "CodeHack Women in Tech Accelerator",
        "description": "Advanced CodeHack track: AI/ML, Cybersecurity, Data Science, Flutter, Backend",
        "launch_year": 2025      # Verified — launched July 2025
    },
]

PROGRAM_DISTRIBUTION = {

    2015:{1:100},

    2016:{
        1:90,
        2:10
    },

    2017:{
        1:70,
        2:20,
        3:10
    },

    2018:{
        1:55,
        2:20,
        3:15,
        4:10
    },

    2019:{
        1:45,
        2:20,
        3:20,
        4:15
    },

    2020:{
        5:100
    },

    2021:{
        5:80,
        6:20
    },

    2022:{
        5:70,
        6:15,
        7:15
    },

    2023:{
        5:65,
        6:20,
        7:15
    },

    2024:{
        5:60,
        6:20,
        7:20
    },

    2025:{
        5:60,
        6:20,
        7:20
    },

    2026:{
        5:55,
        6:20,
        7:25
    }

}


YEAR_CONFIGURATION = {

    2015: {"applications":120,  "cohorts":2,  "capacity_per_cohort":15,  "delivery":"Physical"},
    2016: {"applications":180,  "cohorts":3,  "capacity_per_cohort":18,  "delivery":"Physical"},
    2017: {"applications":300,  "cohorts":4,  "capacity_per_cohort":22,  "delivery":"Physical"},
    2018: {"applications":450,  "cohorts":5,  "capacity_per_cohort":28,  "delivery":"Physical"},
    2019: {"applications":700,  "cohorts":6,  "capacity_per_cohort":35,  "delivery":"Physical"},

    2020: {"applications":1350, "cohorts":12, "capacity_per_cohort":22,  "delivery":"Online"},

    2021: {"applications":1100, "cohorts":10, "capacity_per_cohort":24,  "delivery":"Physical"},

    2022: {"applications":1700, "cohorts":12, "capacity_per_cohort":32,  "delivery":"Physical"},
    2023: {"applications":2700, "cohorts":14, "capacity_per_cohort":40,  "delivery":"Physical"},
    2024: {"applications":3500, "cohorts":16, "capacity_per_cohort":52,  "delivery":"Physical"},
    2025: {"applications":3900, "cohorts":18, "capacity_per_cohort":60,  "delivery":"Physical"},
    2026: {"applications":4543, "cohorts":20, "capacity_per_cohort":70,  "delivery":"Physical"}

}
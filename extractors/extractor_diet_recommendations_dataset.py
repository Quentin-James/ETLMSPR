import csv
import os


def extract_diet_recommendations(filepath: str) -> list[dict]:
    """Read the diet-recommendations CSV and return a list of row dicts."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found: {filepath}")
    with open(filepath, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return [dict(row) for row in reader]


def extract_gym_tracking(filepath: str) -> list[dict]:
    """Read the gym-tracking synthetic CSV and return a list of row dicts."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found: {filepath}")
    with open(filepath, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return [dict(row) for row in reader]

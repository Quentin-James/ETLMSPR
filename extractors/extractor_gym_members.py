import pandas as pd
import os

def extract_gym_members(filepath: str) -> pd.DataFrame:
    """
    Lit le fichier gym_members_exercise_tracking_synthetic_data.csv
    et retourne un DataFrame brut.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Fichier introuvable : {filepath}")

    df = pd.read_csv(filepath)
    print(f"[EXTRACT] {len(df)} lignes chargées depuis {filepath}")
    return df
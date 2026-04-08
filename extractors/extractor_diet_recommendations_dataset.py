import pandas as pd
import os


def extract_diet_recommendations(filepath: str) -> pd.DataFrame:
    """
    Lit le fichier diet_recommendations_dataset.csv
    et retourne un DataFrame brut.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Fichier introuvable : {filepath}")

    df = pd.read_csv(filepath)
    print(f"[EXTRACT] {len(df)} lignes chargées depuis {filepath}")
    return df
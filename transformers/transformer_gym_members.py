import pandas as pd

def transform_gym_members(df: pd.DataFrame) -> dict:
    """
    Nettoie et sépare le DataFrame en 2 tables :
    patients, fitness_sessions
    """

    # --- Nettoyage général ---
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df.drop_duplicates(inplace=True)

    # --- Table patients ---
    patients = df[["age", "gender", "weight_(kg)", "height_(m)", "bmi"]].copy()
    patients = patients.rename(columns={
        "weight_(kg)": "weight_kg",
        "height_(m)":  "height_cm"
    })
    patients["age"]       = pd.to_numeric(patients["age"], errors="coerce").astype("Int64")
    patients["weight_kg"] = pd.to_numeric(patients["weight_kg"], errors="coerce").replace({float('nan'): None})
    patients["height_cm"] = pd.to_numeric(patients["height_cm"], errors="coerce").replace({float('nan'): None})
    patients["bmi"]       = pd.to_numeric(patients["bmi"], errors="coerce").replace({float('nan'): None})
    patients["gender"]    = patients["gender"].str.strip().str.capitalize()
    patients.dropna(subset=["age", "gender"], inplace=True)

    # --- Table fitness_sessions ---
    fitness_sessions = df[[
        "max_bpm", "avg_bpm", "resting_bpm",
        "session_duration_(hours)", "calories_burned",
        "workout_type", "fat_percentage",
        "water_intake_(liters)", "workout_frequency_(days/week)",
        "experience_level"
    ]].copy()
    fitness_sessions = fitness_sessions.rename(columns={
        "session_duration_(hours)":      "session_duration_hours",
        "water_intake_(liters)":         "water_intake_liters",
        "workout_frequency_(days/week)": "workout_frequency_days_week"
    })

    fitness_sessions["max_bpm"]                     = pd.to_numeric(fitness_sessions["max_bpm"], errors="coerce").fillna(0).astype("Int64")
    fitness_sessions["avg_bpm"]                     = pd.to_numeric(fitness_sessions["avg_bpm"], errors="coerce").fillna(0).astype("Int64")
    fitness_sessions["resting_bpm"]                 = pd.to_numeric(fitness_sessions["resting_bpm"], errors="coerce").fillna(0).astype("Int64")
    fitness_sessions["workout_frequency_days_week"] = pd.to_numeric(fitness_sessions["workout_frequency_days_week"], errors="coerce").fillna(0).astype("Int64")
    fitness_sessions["experience_level"]            = pd.to_numeric(fitness_sessions["experience_level"], errors="coerce").fillna(0).astype("Int64")

    # ← Colonnes décimales : replace NaN par None
    decimal_cols = [
        "session_duration_hours", "calories_burned",
        "fat_percentage", "water_intake_liters"
    ]
    for col in decimal_cols:
        fitness_sessions[col] = pd.to_numeric(fitness_sessions[col], errors="coerce").replace({float('nan'): None})

    fitness_sessions["workout_type"] = fitness_sessions["workout_type"].str.strip().str.capitalize()

    fitness_sessions.dropna(subset=["calories_burned", "workout_type"], inplace=True)

    print(f"[TRANSFORM] patients: {len(patients)} lignes")
    print(f"[TRANSFORM] fitness_sessions: {len(fitness_sessions)} lignes")

    return {
        "patients":        patients,
        "fitness_sessions": fitness_sessions
    }
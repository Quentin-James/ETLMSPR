import pandas as pd

def transform_diet_recommendations(df: pd.DataFrame) -> dict:
    """
    Nettoie et sépare le DataFrame en 3 tables :
    patients, health_profiles, diet_preferences
    """

    # --- Nettoyage général ---
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df.drop_duplicates(inplace=True)

    # --- Table patients ---
    patients = df[["age", "gender", "weight_kg", "height_cm", "bmi"]].copy()
    patients["age"] = pd.to_numeric(patients["age"], errors="coerce").astype("Int64")
    patients["weight_kg"] = pd.to_numeric(patients["weight_kg"], errors="coerce")
    patients["height_cm"] = pd.to_numeric(patients["height_cm"], errors="coerce")
    patients["bmi"] = pd.to_numeric(patients["bmi"], errors="coerce")
    patients["gender"] = patients["gender"].str.strip().str.capitalize()
    patients.dropna(subset=["age", "gender"], inplace=True)

    # --- Table health_profiles ---
    health_profiles = df[[
        "disease_type", "severity", "physical_activity_level",
        "daily_caloric_intake", "cholesterol_mg/dl",
        "blood_pressure_mmhg", "glucose_mg/dl"
    ]].copy()
    health_profiles["daily_caloric_intake"] = pd.to_numeric(health_profiles["daily_caloric_intake"], errors="coerce").astype("Int64")
    health_profiles["cholesterol_mg/dl"] = pd.to_numeric(health_profiles["cholesterol_mg/dl"], errors="coerce")
    health_profiles["blood_pressure_mmhg"] = pd.to_numeric(health_profiles["blood_pressure_mmhg"], errors="coerce").astype("Int64")
    health_profiles["glucose_mg/dl"] = pd.to_numeric(health_profiles["glucose_mg/dl"], errors="coerce")
    health_profiles["disease_type"] = health_profiles["disease_type"].str.strip()
    health_profiles["severity"] = health_profiles["severity"].str.strip().str.capitalize()
    health_profiles["physical_activity_level"] = health_profiles["physical_activity_level"].str.strip().str.capitalize()

    # --- Table diet_preferences ---
    diet_preferences = df[[
        "dietary_restrictions", "allergies", "preferred_cuisine",
        "weekly_exercise_hours", "adherence_to_diet_plan"
    ]].copy()
    diet_preferences["weekly_exercise_hours"] = (pd.to_numeric(diet_preferences["weekly_exercise_hours"], errors="coerce")
                                                 .round()
                                                 .astype("Int64"))
    diet_preferences["adherence_to_diet_plan"] = pd.to_numeric(diet_preferences["adherence_to_diet_plan"], errors="coerce")
    diet_preferences["dietary_restrictions"] = diet_preferences["dietary_restrictions"].str.strip()
    diet_preferences["allergies"] = diet_preferences["allergies"].str.strip()
    diet_preferences["preferred_cuisine"] = diet_preferences["preferred_cuisine"].str.strip()

    print(f"[TRANSFORM] patients: {len(patients)} lignes")
    print(f"[TRANSFORM] health_profiles: {len(health_profiles)} lignes")
    print(f"[TRANSFORM] diet_preferences: {len(diet_preferences)} lignes")

    return {
        "patients": patients,
        "health_profiles": health_profiles,
        "diet_preferences": diet_preferences
    }
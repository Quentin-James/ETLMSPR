import psycopg2
from psycopg2.extras import execute_values
from config import DB_CONFIG

def load_diet_recommendations(tables: dict):
    """
    Insère les 3 DataFrames (patients, health_profiles, diet_preferences)
    dans PostgreSQL.
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        # --- Insertion patients ---
        patients = tables["patients"]
        patient_ids = []

        for _, row in patients.iterrows():
            cursor.execute("""
                INSERT INTO patients (age, gender, weight_kg, height_cm, bmi)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (
                row["age"], row["gender"], row["weight_kg"],
                row["height_cm"], row["bmi"]
            ))
            patient_ids.append(cursor.fetchone()[0])

        print(f"[LOAD] {len(patient_ids)} patients insérés")

        # --- Insertion health_profiles ---
        health_profiles = tables["health_profiles"]
        hp_data = [
            (
                patient_ids[i],
                row["disease_type"], row["severity"],
                row["physical_activity_level"], row["daily_caloric_intake"],
                row["cholesterol_mg/dl"], row["blood_pressure_mmhg"],
                row["glucose_mg/dl"]
            )
            for i, (_, row) in enumerate(health_profiles.iterrows())
        ]
        execute_values(cursor, """
            INSERT INTO health_profiles (
                patient_id, disease_type, severity, physical_activity_level,
                daily_caloric_intake, cholesterol_mg_dl,
                blood_pressure_mmhg, glucose_mg_dl
            ) VALUES %s
        """, hp_data)
        print(f"[LOAD] {len(hp_data)} health_profiles insérés")

        # --- Insertion diet_preferences ---
        diet_preferences = tables["diet_preferences"]
        dp_data = [
            (
                patient_ids[i],
                row["dietary_restrictions"], row["allergies"],
                row["preferred_cuisine"], row["weekly_exercise_hours"],
                row["adherence_to_diet_plan"]
            )
            for i, (_, row) in enumerate(diet_preferences.iterrows())
        ]
        execute_values(cursor, """
            INSERT INTO diet_preferences (
                patient_id, dietary_restrictions, allergies,
                preferred_cuisine, weekly_exercise_frequency, adherence_to_diet
            ) VALUES %s
        """, dp_data)
        print(f"[LOAD] {len(dp_data)} diet_preferences insérés")

        conn.commit()
        print("[LOAD] Toutes les données insérées avec succès")

    except Exception as e:
        conn.rollback()
        print(f"[LOAD] Erreur : {e}")
        raise

    finally:
        cursor.close()
        conn.close()
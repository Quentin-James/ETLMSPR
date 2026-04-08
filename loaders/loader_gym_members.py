import psycopg2
from psycopg2.extras import execute_values
from config import DB_CONFIG

def load_gym_members(tables: dict):
    """
    Insère patients et fitness_sessions dans PostgreSQL.
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

        # --- Insertion fitness_sessions ---
        fitness_sessions = tables["fitness_sessions"]
        fs_data = [
            (
                patient_ids[i],
                row["max_bpm"], row["avg_bpm"], row["resting_bpm"],
                row["session_duration_hours"], row["calories_burned"],
                row["workout_type"], row["fat_percentage"],
                row["water_intake_liters"], row["workout_frequency_days_week"],
                row["experience_level"]
            )
            for i, (_, row) in enumerate(fitness_sessions.iterrows())
        ]
        execute_values(cursor, """
            INSERT INTO fitness_sessions (
                patient_id, max_bpm, avg_bpm, resting_bpm,
                session_duration_hours, calories_burned, workout_type,
                fat_percentage, water_intake_liters,
                workout_frequency_days_week, experience_level
            ) VALUES %s
        """, fs_data)
        print(f"[LOAD] {len(fs_data)} fitness_sessions insérées")

        conn.commit()
        print("[LOAD] Toutes les données insérées avec succès")

    except Exception as e:
        conn.rollback()
        print(f"[LOAD] Erreur : {e}")
        raise

    finally:
        cursor.close()
        conn.close()
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


# ─── upsert helpers ──────────────────────────────────────────────────────────

def _upsert_patients(cursor, rows: list[dict]) -> int:
    sql = """
        INSERT INTO core.patients (id, age, gender, weight_kg, height_cm, bmi)
        VALUES (%(id)s, %(age)s, %(gender)s, %(weight_kg)s, %(height_cm)s, %(bmi)s)
        ON CONFLICT (id) DO UPDATE SET
            age       = EXCLUDED.age,
            gender    = EXCLUDED.gender,
            weight_kg = EXCLUDED.weight_kg,
            height_cm = EXCLUDED.height_cm,
            bmi       = EXCLUDED.bmi;
    """
    cursor.executemany(sql, rows)
    return len(rows)


def _upsert_health_profiles(cursor, rows: list[dict]) -> int:
    sql = """
        INSERT INTO core.health_profiles (
            patient_id, disease_type, severity, physical_activity_level,
            daily_caloric_intake, cholesterol_mg_dl, blood_pressure_mmhg, glucose_mg_dl
        )
        VALUES (
            %(patient_id)s, %(disease_type)s, %(severity)s, %(physical_activity_level)s,
            %(daily_caloric_intake)s, %(cholesterol_mg_dl)s, %(blood_pressure_mmhg)s,
            %(glucose_mg_dl)s
        )
        ON CONFLICT (patient_id) DO UPDATE SET
            disease_type            = EXCLUDED.disease_type,
            severity                = EXCLUDED.severity,
            physical_activity_level = EXCLUDED.physical_activity_level,
            daily_caloric_intake    = EXCLUDED.daily_caloric_intake,
            cholesterol_mg_dl       = EXCLUDED.cholesterol_mg_dl,
            blood_pressure_mmhg     = EXCLUDED.blood_pressure_mmhg,
            glucose_mg_dl           = EXCLUDED.glucose_mg_dl;
    """
    cursor.executemany(sql, rows)
    return len(rows)


def _upsert_diet_preferences(cursor, rows: list[dict]) -> int:
    sql = """
        INSERT INTO core.diet_preferences (
            patient_id, dietary_restrictions, allergies, preferred_cuisine,
            weekly_exercise_frequency, adherence_to_diet
        )
        VALUES (
            %(patient_id)s, %(dietary_restrictions)s, %(allergies)s,
            %(preferred_cuisine)s, %(weekly_exercise_frequency)s, %(adherence_to_diet)s
        )
        ON CONFLICT (patient_id) DO UPDATE SET
            dietary_restrictions      = EXCLUDED.dietary_restrictions,
            allergies                 = EXCLUDED.allergies,
            preferred_cuisine         = EXCLUDED.preferred_cuisine,
            weekly_exercise_frequency = EXCLUDED.weekly_exercise_frequency,
            adherence_to_diet         = EXCLUDED.adherence_to_diet;
    """
    cursor.executemany(sql, rows)
    return len(rows)


def _insert_gym_tracking(cursor, rows: list[dict]) -> int:
    sql = """
        INSERT INTO core.gym_tracking (
            age, gender, weight_kg, height_m, max_bpm, avg_bpm, resting_bpm,
            session_duration_hours, calories_burned, workout_type, fat_percentage,
            water_intake_liters, workout_frequency_days_week, experience_level,
            bmi, bmi_category
        )
        VALUES (
            %(age)s, %(gender)s, %(weight_kg)s, %(height_m)s, %(max_bpm)s,
            %(avg_bpm)s, %(resting_bpm)s, %(session_duration_hours)s,
            %(calories_burned)s, %(workout_type)s, %(fat_percentage)s,
            %(water_intake_liters)s, %(workout_frequency_days_week)s,
            %(experience_level)s, %(bmi)s, %(bmi_category)s
        );
    """
    cursor.executemany(sql, rows)
    return len(rows)


# ─── public API ──────────────────────────────────────────────────────────────

def persist_core_tables_to_postgres(
    conn,
    patients: list[dict],
    health_profiles: list[dict],
    diet_preferences: list[dict],
    gym_tracking: list[dict] | None = None,
) -> dict:
    """
    Write transformed data to the core schema tables.

    Parameters
    ----------
    conn            : active psycopg2 connection
    patients        : rows for core.patients
    health_profiles : rows for core.health_profiles
    diet_preferences: rows for core.diet_preferences
    gym_tracking    : (optional) rows for core.gym_tracking

    Returns
    -------
    dict with counts per table
    """
    counts: dict[str, int] = {}
    with conn:
        cur = conn.cursor()
        try:
            counts["patients"] = _upsert_patients(cur, patients)
            logger.info("Upserted %d patients", counts["patients"])

            counts["health_profiles"] = _upsert_health_profiles(cur, health_profiles)
            logger.info("Upserted %d health_profiles", counts["health_profiles"])

            counts["diet_preferences"] = _upsert_diet_preferences(cur, diet_preferences)
            logger.info("Upserted %d diet_preferences", counts["diet_preferences"])

            if gym_tracking:
                counts["gym_tracking"] = _insert_gym_tracking(cur, gym_tracking)
                logger.info("Inserted %d gym_tracking rows", counts["gym_tracking"])

        finally:
            cur.close()

    return counts

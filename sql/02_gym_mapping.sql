-- =============================================================
-- 02_gym_mapping.sql  –  Gym-tracking staging + clean tables
-- =============================================================
-- Prerequisites: sql/01_schema.sql must have been applied first.
--
-- Usage (from psql):
--   \i sql/02_gym_mapping.sql
--
-- Or step-by-step:
--   1. Apply this file to create the tables.
--   2. Run the \copy command below (adjust the CSV path as needed).
--   3. Run the INSERT … SELECT block to populate core.gym_tracking.
-- =============================================================

-- ─── Staging table (all columns as TEXT for safe bulk load) ──
CREATE TABLE IF NOT EXISTS core.gym_tracking_staging (
    age                         TEXT,
    gender                      TEXT,
    weight_kg                   TEXT,
    height_m                    TEXT,
    max_bpm                     TEXT,
    avg_bpm                     TEXT,
    resting_bpm                 TEXT,
    session_duration_hours      TEXT,
    calories_burned             TEXT,
    workout_type                TEXT,
    fat_percentage              TEXT,
    water_intake_liters         TEXT,
    workout_frequency_days_week TEXT,
    experience_level            TEXT,
    bmi                         TEXT
);

-- ─── Clean typed table ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS core.gym_tracking (
    id                          SERIAL PRIMARY KEY,
    age                         INTEGER,
    gender                      VARCHAR(10),
    weight_kg                   NUMERIC(5,1),
    height_m                    NUMERIC(4,2),
    max_bpm                     INTEGER,
    avg_bpm                     NUMERIC(6,1),
    resting_bpm                 NUMERIC(6,1),
    session_duration_hours      NUMERIC(4,2),
    calories_burned             NUMERIC(8,1),
    workout_type                VARCHAR(30),
    fat_percentage              NUMERIC(4,1),
    water_intake_liters         NUMERIC(4,1),
    workout_frequency_days_week INTEGER,
    experience_level            INTEGER,
    bmi                         NUMERIC(5,2),
    bmi_category                VARCHAR(20)
);

-- =============================================================
-- Step 1 – Load raw CSV into staging
-- =============================================================
-- Adjust the file path to match your local environment.
-- On Windows use forward slashes or escaped back-slashes.
--
-- \copy core.gym_tracking_staging (
--     age, gender, weight_kg, height_m, max_bpm, avg_bpm,
--     resting_bpm, session_duration_hours, calories_burned,
--     workout_type, fat_percentage, water_intake_liters,
--     workout_frequency_days_week, experience_level, bmi
-- )
-- FROM 'datasets/gym_members_exercise_tracking_synthetic_data.csv'
-- WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- =============================================================
-- Step 2 – Transform staging → core.gym_tracking
-- =============================================================
INSERT INTO core.gym_tracking (
    age,
    gender,
    weight_kg,
    height_m,
    max_bpm,
    avg_bpm,
    resting_bpm,
    session_duration_hours,
    calories_burned,
    workout_type,
    fat_percentage,
    water_intake_liters,
    workout_frequency_days_week,
    experience_level,
    bmi,
    bmi_category
)
SELECT
    age::NUMERIC::INTEGER,
    TRIM(gender),
    weight_kg::NUMERIC(5,1),
    height_m::NUMERIC(4,2),
    max_bpm::NUMERIC::INTEGER,
    avg_bpm::NUMERIC(6,1),
    resting_bpm::NUMERIC(6,1),
    session_duration_hours::NUMERIC(4,2),
    calories_burned::NUMERIC(8,1),
    TRIM(workout_type),
    fat_percentage::NUMERIC(4,1),
    water_intake_liters::NUMERIC(4,1),
    workout_frequency_days_week::NUMERIC::INTEGER,
    experience_level::NUMERIC::INTEGER,
    bmi::NUMERIC(5,2),
    CASE
        -- Mirrors the bmi_category logic in transformers/transformer_diet_recommendations_dataset.py
        WHEN bmi::NUMERIC < 18.5                          THEN 'Underweight'
        WHEN bmi::NUMERIC >= 18.5 AND bmi::NUMERIC < 25  THEN 'Normal'
        WHEN bmi::NUMERIC >= 25   AND bmi::NUMERIC < 30  THEN 'Overweight'
        ELSE                                                   'Obese'
    END
FROM core.gym_tracking_staging
WHERE age       IS NOT NULL
  AND weight_kg IS NOT NULL
  AND bmi       IS NOT NULL;

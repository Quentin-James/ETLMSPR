-- Table centrale des patients (colonnes communes aux deux CSV)
--
CREATE TABLE patients
(
    id        SERIAL PRIMARY KEY,
    age       INTEGER,
    gender    VARCHAR(10),
    weight_kg NUMERIC(5, 1),
    height_cm NUMERIC(5, 2),
    bmi       NUMERIC(4, 1)
);

-- Depuis diet_recommendations_dataset.csv
CREATE TABLE health_profiles
(
    id                      SERIAL PRIMARY KEY,
    patient_id              INTEGER UNIQUE NOT NULL REFERENCES patients (id) ON DELETE CASCADE,
    disease_type            VARCHAR(50),
    severity                VARCHAR(20),
    physical_activity_level VARCHAR(20),
    daily_caloric_intake    INTEGER,
    cholesterol_mg_dl       NUMERIC(5, 1),
    blood_pressure_mmhg     INTEGER,
    glucose_mg_dl           NUMERIC(5, 1)
);

CREATE TABLE diet_preferences
(
    id                        SERIAL PRIMARY KEY,
    patient_id                INTEGER UNIQUE NOT NULL REFERENCES patients (id) ON DELETE CASCADE,
    dietary_restrictions      VARCHAR(50),
    allergies                 VARCHAR(50),
    preferred_cuisine         VARCHAR(50),
    weekly_exercise_frequency INTEGER,
    adherence_to_diet         NUMERIC(3, 1)
);

-- Depuis gym_members_exercise_tracking_synthetic_data.csv
CREATE TABLE fitness_sessions
(
    id                          SERIAL PRIMARY KEY,
    patient_id                  INTEGER NOT NULL REFERENCES patients (id) ON DELETE CASCADE,
    max_bpm                     INTEGER,
    avg_bpm                     INTEGER,
    resting_bpm                 INTEGER,
    session_duration_hours      NUMERIC(4, 2),
    calories_burned             NUMERIC(7, 1),
    workout_type                VARCHAR(30),
    fat_percentage              NUMERIC(4, 1),
    water_intake_liters         NUMERIC(3, 1),
    workout_frequency_days_week INTEGER,
    experience_level            INTEGER
);

-- daily_food_nutrition_dataset
-- =========================
-- TABLE: categories
-- =========================
CREATE TABLE categories
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- =========================
-- TABLE: meal_types
-- =========================
CREATE TABLE meal_types
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- =========================
-- TABLE: foods
-- =========================
CREATE TABLE foods
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    category_id INTEGER      NOT NULL,

    CONSTRAINT fk_category
        FOREIGN KEY (category_id)
            REFERENCES categories (id)
            ON DELETE CASCADE
);

-- =========================
-- TABLE: nutrition_logs
-- =========================
CREATE TABLE nutrition_logs
(
    id            SERIAL PRIMARY KEY,
    food_id       INTEGER NOT NULL,
    meal_type_id  INTEGER NOT NULL,

    calories      NUMERIC(6, 2),
    protein       NUMERIC(6, 2),
    carbohydrates NUMERIC(6, 2),
    fat           NUMERIC(6, 2),
    fiber         NUMERIC(6, 2),
    sugars        NUMERIC(6, 2),
    sodium        NUMERIC(6, 2),
    cholesterol   NUMERIC(6, 2),
    water_intake  INTEGER,

    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_food
        FOREIGN KEY (food_id)
            REFERENCES foods (id)
            ON DELETE CASCADE,

    CONSTRAINT fk_meal_type
        FOREIGN KEY (meal_type_id)
            REFERENCES meal_types (id)
            ON DELETE CASCADE
);
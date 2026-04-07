-- Table centrale des patients (colonnes communes aux deux CSV)
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    age INTEGER,
    gender VARCHAR(10),
    weight_kg NUMERIC(5,1),
    height_cm NUMERIC(5,2),
    bmi NUMERIC(4,1)
);

-- Depuis diet_recommendations_dataset.csv
CREATE TABLE health_profiles (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER UNIQUE NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    disease_type VARCHAR(50),
    severity VARCHAR(20),
    physical_activity_level VARCHAR(20),
    daily_caloric_intake INTEGER,
    cholesterol_mg_dl NUMERIC(5,1),
    blood_pressure_mmhg INTEGER,
    glucose_mg_dl NUMERIC(5,1)
);

CREATE TABLE diet_preferences (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER UNIQUE NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    dietary_restrictions VARCHAR(50),
    allergies VARCHAR(50),
    preferred_cuisine VARCHAR(50),
    weekly_exercise_frequency INTEGER,
    adherence_to_diet NUMERIC(3,1)
);

-- Depuis gym_members_exercise_tracking_synthetic_data.csv
CREATE TABLE fitness_sessions (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    max_bpm INTEGER,
    avg_bpm INTEGER,
    resting_bpm INTEGER,
    session_duration_hours NUMERIC(4,2),
    calories_burned NUMERIC(7,1),
    workout_type VARCHAR(30),
    fat_percentage NUMERIC(4,1),
    water_intake_liters NUMERIC(3,1),
    workout_frequency_days_week INTEGER,
    experience_level INTEGER
);
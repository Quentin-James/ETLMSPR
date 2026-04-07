CREATE TABLE patients (
    id VARCHAR(10) PRIMARY KEY,
    age INTEGER NOT NULL,
    gender VARCHAR(10) NOT NULL,
    weight_kg NUMERIC(5,1),
    height_cm INTEGER,
    bmi NUMERIC(4,1)
);

CREATE TABLE health_profiles (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(10) UNIQUE NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
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
    patient_id VARCHAR(10) UNIQUE NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    dietary_restrictions VARCHAR(50),
    allergies VARCHAR(50),
    preferred_cuisine VARCHAR(50),
    weekly_exercise_frequency INTEGER,
    adherence_to_diet NUMERIC(3,1)
);
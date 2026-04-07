-- =============================================================
-- 01_schema.sql  –  Full schema bootstrap for healthai_coach
-- =============================================================
-- Creates four schemas (raw / core / mart / audit) and the three
-- core business tables used by the ETL pipeline.
-- Safe to run multiple times (all statements are idempotent).
-- =============================================================

-- ─── Schemas ─────────────────────────────────────────────────
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS mart;
CREATE SCHEMA IF NOT EXISTS audit;

-- ─── core.patients ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS core.patients (
    id              VARCHAR(10) PRIMARY KEY,
    age             INTEGER        NOT NULL,
    gender          VARCHAR(10)    NOT NULL,
    weight_kg       NUMERIC(5,1),
    height_cm       INTEGER,
    bmi             NUMERIC(4,1)
);

-- ─── core.health_profiles ────────────────────────────────────
CREATE TABLE IF NOT EXISTS core.health_profiles (
    id                      SERIAL PRIMARY KEY,
    patient_id              VARCHAR(10) UNIQUE NOT NULL
                                REFERENCES core.patients(id) ON DELETE CASCADE,
    disease_type            VARCHAR(50),
    severity                VARCHAR(20),
    physical_activity_level VARCHAR(20),
    daily_caloric_intake    INTEGER,
    cholesterol_mg_dl       NUMERIC(5,1),
    blood_pressure_mmhg     INTEGER,
    glucose_mg_dl           NUMERIC(5,1)
);

-- ─── core.diet_preferences ───────────────────────────────────
CREATE TABLE IF NOT EXISTS core.diet_preferences (
    id                       SERIAL PRIMARY KEY,
    patient_id               VARCHAR(10) UNIQUE NOT NULL
                                 REFERENCES core.patients(id) ON DELETE CASCADE,
    dietary_restrictions     VARCHAR(50),
    allergies                VARCHAR(50),
    preferred_cuisine        VARCHAR(50),
    weekly_exercise_frequency INTEGER,
    adherence_to_diet        NUMERIC(3,1)
);

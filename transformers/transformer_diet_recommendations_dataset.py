from __future__ import annotations


# ─── helpers ─────────────────────────────────────────────────────────────────

def _safe_float(value: str | None) -> float | None:
    try:
        return float(value) if value not in (None, "") else None
    except (ValueError, TypeError):
        return None


def _safe_int(value: str | None) -> int | None:
    f = _safe_float(value)
    return int(f) if f is not None else None


def _bmi_category(bmi: float | None) -> str | None:
    if bmi is None:
        return None
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25.0:
        return "Normal"
    if bmi < 30.0:
        return "Overweight"
    return "Obese"


# ─── diet-recommendations ─────────────────────────────────────────────────────

def transform_patients(raw_rows: list[dict]) -> list[dict]:
    """Map diet-recommendations CSV rows → core.patients shape."""
    result = []
    for row in raw_rows:
        bmi = _safe_float(row.get("BMI"))
        result.append({
            "id":        row.get("Patient_ID", "").strip(),
            "age":       _safe_int(row.get("Age")),
            "gender":    (row.get("Gender") or "").strip(),
            "weight_kg": _safe_float(row.get("Weight_kg")),
            "height_cm": _safe_int(row.get("Height_cm")),
            "bmi":       round(bmi, 1) if bmi is not None else None,
        })
    return [r for r in result if r["id"]]


def transform_health_profiles(raw_rows: list[dict]) -> list[dict]:
    """Map diet-recommendations CSV rows → core.health_profiles shape."""
    result = []
    for row in raw_rows:
        result.append({
            "patient_id":              row.get("Patient_ID", "").strip(),
            "disease_type":            (row.get("Disease_Type") or "").strip(),
            "severity":                (row.get("Severity") or "").strip(),
            "physical_activity_level": (row.get("Physical_Activity_Level") or "").strip(),
            "daily_caloric_intake":    _safe_int(row.get("Daily_Caloric_Intake")),
            "cholesterol_mg_dl":       _safe_float(row.get("Cholesterol_mg/dL")),
            "blood_pressure_mmhg":     _safe_int(row.get("Blood_Pressure_mmHg")),
            "glucose_mg_dl":           _safe_float(row.get("Glucose_mg/dL")),
        })
    return [r for r in result if r["patient_id"]]


def transform_diet_preferences(raw_rows: list[dict]) -> list[dict]:
    """Map diet-recommendations CSV rows → core.diet_preferences shape."""
    result = []
    for row in raw_rows:
        result.append({
            "patient_id":               row.get("Patient_ID", "").strip(),
            "dietary_restrictions":     (row.get("Dietary_Restrictions") or "").strip(),
            "allergies":                (row.get("Allergies") or "").strip(),
            "preferred_cuisine":        (row.get("Preferred_Cuisine") or "").strip(),
            "weekly_exercise_frequency": _safe_int(row.get("Weekly_Exercise_Hours")),
            "adherence_to_diet":        _safe_float(row.get("Adherence_to_Diet_Plan")),
        })
    return [r for r in result if r["patient_id"]]


# ─── gym tracking ─────────────────────────────────────────────────────────────

def _clean_gym_tracking(raw_rows: list[dict]) -> list[dict]:
    """Map gym-tracking CSV rows → core.gym_tracking shape (typed + bmi_category)."""
    result = []
    for row in raw_rows:
        bmi = _safe_float(row.get("BMI"))
        result.append({
            "age":                         _safe_int(row.get("Age")),
            "gender":                      (row.get("Gender") or "").strip(),
            "weight_kg":                   _safe_float(row.get("Weight (kg)")),
            "height_m":                    _safe_float(row.get("Height (m)")),
            "max_bpm":                     _safe_int(row.get("Max_BPM")),
            "avg_bpm":                     _safe_float(row.get("Avg_BPM")),
            "resting_bpm":                 _safe_float(row.get("Resting_BPM")),
            "session_duration_hours":      _safe_float(row.get("Session_Duration (hours)")),
            "calories_burned":             _safe_float(row.get("Calories_Burned")),
            "workout_type":                (row.get("Workout_Type") or "").strip(),
            "fat_percentage":              _safe_float(row.get("Fat_Percentage")),
            "water_intake_liters":         _safe_float(row.get("Water_Intake (liters)")),
            "workout_frequency_days_week": _safe_int(row.get("Workout_Frequency (days/week)")),
            "experience_level":            _safe_int(row.get("Experience_Level")),
            "bmi":                         round(bmi, 2) if bmi is not None else None,
            "bmi_category":                _bmi_category(bmi),
        })
    return [r for r in result if r["age"] is not None]


def transform_gym_tracking(raw_rows: list[dict]) -> list[dict]:
    return _clean_gym_tracking(raw_rows)

"""
main.py – ETL pipeline entry-point for healthai_coach.

Usage
-----
  python main.py              # full run (extract → transform → load → persist)
  python main.py --skip-db   # skip the PostgreSQL persist step
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)
logger = logging.getLogger("etl.main")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
DATASETS_DIR = BASE_DIR / "datasets"
ARTIFACTS_DIR = BASE_DIR / "artifacts" / "runs"

DIET_CSV = DATASETS_DIR / "diet_recommendations_dataset.csv"
GYM_CSV  = DATASETS_DIR / "gym_members_exercise_tracking_synthetic_data.csv"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run_id() -> str:
    return "etl_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "Z"


def _write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run(*, skip_db: bool = False) -> dict:
    run_id = _run_id()
    run_dir = ARTIFACTS_DIR / run_id
    logs_dir = run_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Run ID: %s", run_id)
    summary: dict = {"run_id": run_id, "db": {}, "counts": {}}

    # ── Extract ──────────────────────────────────────────────────────────────
    logger.info("Extracting diet-recommendations dataset …")
    from extractors.extractor_diet_recommendations_dataset import (
        extract_diet_recommendations,
        extract_gym_tracking,
    )
    diet_raw = extract_diet_recommendations(str(DIET_CSV))
    gym_raw  = extract_gym_tracking(str(GYM_CSV))
    logger.info("Extracted %d diet rows, %d gym rows", len(diet_raw), len(gym_raw))

    # Bronze
    _write_json(run_dir / "bronze" / "diet_recommendations.json", diet_raw)
    _write_json(run_dir / "bronze" / "gym_tracking.json",         gym_raw)

    # ── Transform ────────────────────────────────────────────────────────────
    logger.info("Transforming …")
    from transformers.transformer_diet_recommendations_dataset import (
        transform_patients,
        transform_health_profiles,
        transform_diet_preferences,
        transform_gym_tracking,
    )
    patients         = transform_patients(diet_raw)
    health_profiles  = transform_health_profiles(diet_raw)
    diet_preferences = transform_diet_preferences(diet_raw)
    gym_tracking     = transform_gym_tracking(gym_raw)

    logger.info(
        "Transformed: %d patients, %d health_profiles, %d diet_preferences, %d gym rows",
        len(patients), len(health_profiles), len(diet_preferences), len(gym_tracking),
    )

    # Silver
    _write_json(run_dir / "silver" / "patients.json",         patients)
    _write_json(run_dir / "silver" / "health_profiles.json",  health_profiles)
    _write_json(run_dir / "silver" / "diet_preferences.json", diet_preferences)
    _write_json(run_dir / "silver" / "gym_tracking.json",     gym_tracking)

    summary["counts"] = {
        "patients":         len(patients),
        "health_profiles":  len(health_profiles),
        "diet_preferences": len(diet_preferences),
        "gym_tracking":     len(gym_tracking),
    }

    # Gold – same as silver for now (could apply additional aggregations)
    _write_json(run_dir / "gold" / "patients.json",         patients)
    _write_json(run_dir / "gold" / "health_profiles.json",  health_profiles)
    _write_json(run_dir / "gold" / "diet_preferences.json", diet_preferences)
    _write_json(run_dir / "gold" / "gym_tracking.json",     gym_tracking)

    # ── Persist ──────────────────────────────────────────────────────────────
    if skip_db:
        logger.info("--skip-db flag set – skipping database persist.")
        summary["db"] = {"run_id": run_id, "skipped": True, "reason": "skip_db_flag"}
    else:
        try:
            import psycopg2  # noqa: F401
        except ImportError:
            logger.warning(
                "psycopg2 is not installed. "
                "Run: pip install psycopg2-binary"
            )
            summary["db"] = {
                "run_id": run_id,
                "skipped": True,
                "reason": "psycopg2_not_installed",
            }
            _write_json(logs_dir / "etl_run_summary.json", summary)
            return summary

        from config import DB_CONFIG
        from loaders.loader_diet_recommendations_dataset import persist_core_tables_to_postgres
        import psycopg2

        try:
            conn = psycopg2.connect(**DB_CONFIG)
            logger.info("Connected to PostgreSQL (%s)", DB_CONFIG.get("dbname"))
        except Exception as exc:
            logger.error("DB connection failed: %s", exc)
            summary["db"] = {
                "run_id": run_id,
                "skipped": True,
                "reason": f"connection_error: {exc}",
            }
            _write_json(logs_dir / "etl_run_summary.json", summary)
            return summary

        try:
            counts = persist_core_tables_to_postgres(
                conn,
                patients=patients,
                health_profiles=health_profiles,
                diet_preferences=diet_preferences,
                gym_tracking=gym_tracking,
            )
            summary["db"] = {
                "run_id":  run_id,
                "skipped": False,
                "counts":  counts,
            }
            logger.info("DB persist complete: %s", counts)
        except Exception as exc:
            logger.error("DB persist error: %s", exc)
            summary["db"] = {
                "run_id":  run_id,
                "skipped": True,
                "reason":  f"persist_error: {exc}",
            }
        finally:
            conn.close()

    _write_json(logs_dir / "etl_run_summary.json", summary)
    logger.info("Run summary written to %s", logs_dir / "etl_run_summary.json")
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="healthai_coach ETL pipeline")
    parser.add_argument(
        "--skip-db",
        action="store_true",
        default=False,
        help="Skip the PostgreSQL persist step (useful for local testing).",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = _parse_args()
    result = run(skip_db=args.skip_db)
    print(json.dumps(result, indent=2, default=str))

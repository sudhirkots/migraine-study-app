"""SQLite storage for the migraine clinic study."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import pandas as pd

DB_PATH = Path(__file__).parent / "migraine_study.db"


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _conn() as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,
                age INTEGER,
                sex TEXT,
                language TEXT,
                visit_type TEXT NOT NULL,
                visit_date TEXT NOT NULL,
                hit6_items TEXT,
                hit6_score INTEGER,
                hit6_category TEXT,
                phq9_items TEXT,
                phq9_score INTEGER,
                phq9_category TEXT,
                phq9_suicidality INTEGER,
                gad7_items TEXT,
                gad7_score INTEGER,
                gad7_category TEXT,
                headache_days INTEGER,
                understanding_score INTEGER,
                notes TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        c.execute("CREATE INDEX IF NOT EXISTS idx_patient ON records(patient_id)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_visit ON records(visit_type)")


def save_record(record: dict) -> int:
    record = {**record, "created_at": datetime.utcnow().isoformat()}
    record["hit6_items"] = json.dumps(record.get("hit6_items") or [])
    record["phq9_items"] = json.dumps(record.get("phq9_items") or [])
    record["gad7_items"] = json.dumps(record.get("gad7_items") or [])
    record["phq9_suicidality"] = int(bool(record.get("phq9_suicidality", False)))

    cols = [
        "patient_id", "age", "sex", "language", "visit_type", "visit_date",
        "hit6_items", "hit6_score", "hit6_category",
        "phq9_items", "phq9_score", "phq9_category", "phq9_suicidality",
        "gad7_items", "gad7_score", "gad7_category",
        "headache_days", "understanding_score", "notes", "created_at",
    ]
    placeholders = ",".join("?" for _ in cols)
    with _conn() as c:
        cur = c.execute(
            f"INSERT INTO records ({','.join(cols)}) VALUES ({placeholders})",
            [record.get(col) for col in cols],
        )
        return cur.lastrowid


def list_patient_ids() -> List[str]:
    with _conn() as c:
        rows = c.execute("SELECT DISTINCT patient_id FROM records ORDER BY patient_id").fetchall()
    return [r["patient_id"] for r in rows]


def get_records_for_patient(patient_id: str) -> List[dict]:
    with _conn() as c:
        rows = c.execute(
            "SELECT * FROM records WHERE patient_id = ? ORDER BY visit_date, created_at",
            (patient_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def latest_visit(patient_id: str, visit_type: str) -> Optional[dict]:
    with _conn() as c:
        row = c.execute(
            """
            SELECT * FROM records
            WHERE patient_id = ? AND visit_type = ?
            ORDER BY visit_date DESC, created_at DESC
            LIMIT 1
            """,
            (patient_id, visit_type),
        ).fetchone()
    return dict(row) if row else None


def all_records_dataframe() -> pd.DataFrame:
    with _conn() as c:
        df = pd.read_sql_query("SELECT * FROM records ORDER BY patient_id, visit_date", c)
    # JSON columns are kept as strings in the export — that is intentional
    # so the CSV/Excel round-trips cleanly.
    return df

"""Google Sheets storage for the migraine clinic study.

Public API mirrors the prior SQLite module so app.py is unchanged:
    init_db(), save_record(), list_patient_ids(),
    get_records_for_patient(), latest_visit(), all_records_dataframe()

Secrets expected in Streamlit (.streamlit/secrets.toml locally, or the
Streamlit Cloud secrets UI):

    sheet_url = "https://docs.google.com/spreadsheets/d/<id>/edit"

    [gcp_service_account]
    type = "service_account"
    project_id = "..."
    private_key_id = "..."
    private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
    client_email = "...@...iam.gserviceaccount.com"
    client_id = "..."
    auth_uri = "https://accounts.google.com/o/oauth2/auth"
    token_uri = "https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
    client_x509_cert_url = "..."
"""

import json
from datetime import datetime
from typing import List, Optional

import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

WORKSHEET_NAME = "records"

COLUMNS = [
    "id", "patient_id", "age", "sex", "language", "visit_type", "visit_date",
    "hit6_items", "hit6_score", "hit6_category",
    "phq9_items", "phq9_score", "phq9_category", "phq9_suicidality",
    "gad7_items", "gad7_score", "gad7_category",
    "mucs_items", "mucs_score", "mucs_category",
    "headache_days", "notes", "created_at",
]

INT_COLUMNS = {
    "id", "age", "hit6_score", "phq9_score", "phq9_suicidality",
    "gad7_score", "mucs_score", "headache_days",
}


@st.cache_resource(show_spinner=False)
def _client() -> gspread.Client:
    creds = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]),
        scopes=SCOPES,
    )
    return gspread.authorize(creds)


@st.cache_resource(show_spinner=False)
def _worksheet() -> gspread.Worksheet:
    """Return the records worksheet. Cached for the life of the session so
    Streamlit reruns (one per widget click) don't hammer the Sheets API."""
    sh = _client().open_by_url(st.secrets["sheet_url"])
    try:
        return sh.worksheet(WORKSHEET_NAME)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=WORKSHEET_NAME, rows=1000, cols=len(COLUMNS))
        ws.update("A1", [COLUMNS])
        return ws


@st.cache_resource(show_spinner=False)
def init_db() -> bool:
    """Ensure the worksheet exists with the right header row. Runs once
    per session — return value is cached so reruns are free."""
    ws = _worksheet()
    header = ws.row_values(1)
    if header != COLUMNS:
        ws.update("A1", [COLUMNS])
    return True


def _coerce_row(row: dict) -> dict:
    """Convert Google-Sheets string values into typed Python values."""
    out = dict(row)
    for col in INT_COLUMNS:
        v = out.get(col)
        if v in (None, ""):
            out[col] = None
        else:
            try:
                out[col] = int(v)
            except (TypeError, ValueError):
                out[col] = None
    return out


@st.cache_data(ttl=60, show_spinner=False)
def _all_rows() -> List[dict]:
    ws = _worksheet()
    rows = ws.get_all_records(expected_headers=COLUMNS)
    return [_coerce_row(r) for r in rows]


def _invalidate_cache() -> None:
    _all_rows.clear()


def save_record(record: dict) -> int:
    record = {**record, "created_at": datetime.utcnow().isoformat()}
    record["hit6_items"] = json.dumps(record.get("hit6_items") or [])
    record["phq9_items"] = json.dumps(record.get("phq9_items") or [])
    record["gad7_items"] = json.dumps(record.get("gad7_items") or [])
    record["mucs_items"] = json.dumps(record.get("mucs_items") or [])
    record["phq9_suicidality"] = int(bool(record.get("phq9_suicidality", False)))

    ws = _worksheet()
    existing = ws.get_all_values()
    # row 1 is the header
    next_id = max((int(r[0]) for r in existing[1:] if r and r[0].isdigit()), default=0) + 1
    record["id"] = next_id

    row = [record.get(col, "") for col in COLUMNS]
    # gspread accepts USER_ENTERED (formula parsing) or RAW (literal). Use RAW
    # so a patient ID like "=MIG-001" or notes starting with "=" don't become formulas.
    ws.append_row(row, value_input_option="RAW")
    _invalidate_cache()
    return next_id


def list_patient_ids() -> List[str]:
    ids = sorted({r["patient_id"] for r in _all_rows() if r.get("patient_id")})
    return ids


def get_records_for_patient(patient_id: str) -> List[dict]:
    rows = [r for r in _all_rows() if r.get("patient_id") == patient_id]
    rows.sort(key=lambda r: (r.get("visit_date") or "", r.get("created_at") or ""))
    return rows


def latest_visit(patient_id: str, visit_type: str) -> Optional[dict]:
    rows = [
        r for r in _all_rows()
        if r.get("patient_id") == patient_id and r.get("visit_type") == visit_type
    ]
    if not rows:
        return None
    rows.sort(key=lambda r: (r.get("visit_date") or "", r.get("created_at") or ""), reverse=True)
    return rows[0]


def all_records_dataframe() -> pd.DataFrame:
    rows = _all_rows()
    df = pd.DataFrame(rows, columns=COLUMNS)
    if not df.empty:
        df = df.sort_values(["patient_id", "visit_date"], na_position="last").reset_index(drop=True)
    return df

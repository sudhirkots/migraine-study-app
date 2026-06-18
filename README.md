# Migraine Clinic Research App (MVP)

A small Streamlit app for a clinic-based migraine study.
Patients fill HIT-6, PHQ-9, GAD-7, headache days, and an understanding score
in English / Hindi / Marathi. Scores are computed automatically, stored in a
local SQLite database, and exportable as CSV/Excel.

## Files

- [app.py](app.py) — Streamlit UI (new record / follow-up comparison / export)
- [questionnaires.py](questionnaires.py) — item text + response options in all three languages
- [scoring.py](scoring.py) — HIT-6, PHQ-9, GAD-7 totals + severity categories
- [database.py](database.py) — SQLite read/write
- `migraine_study.db` — created on first run (do not commit)

## Run it

```powershell
# one-time
pip install -r requirements.txt

# every time
streamlit run app.py
```

The app opens at http://localhost:8501.

## What the app does

1. **New record** — pick language, enter patient ID / age / sex / visit type
   (baseline or follow-up), fill the three questionnaires, headache days, and
   understanding score. Live preview of HIT-6 / PHQ-9 / GAD-7 totals and
   severity bands. Save commits to SQLite.
2. **Baseline vs follow-up** — pick a patient ID, see baseline vs latest
   follow-up side-by-side with a per-measure verdict
   (Improved / Unchanged / Worse, based on each instrument's MCID).
3. **Export data** — full CSV or Excel download of every record.

## Safety hook

If PHQ-9 item 9 (self-harm thoughts) ≥ 1, the new-record page shows a red
clinician alert before save. Don't ignore it.

## Translation notes

- **Marathi HIT-6**: finalized with the investigator on 2026-06-18. The
  intended next step is a paper pilot with 10 consecutive migraine
  patients, asking only "यातला कुठला प्रश्न समजायला कठीण वाटला का?"
  Pilot first, edit later.
- **Hindi HIT-6, PHQ-9, GAD-7**: working drafts. Replace with the exact
  wording of whichever validated translation you cite in your study
  protocol before you collect real data.
- **HIT-6 licensing**: HIT-6 is © QualityMetric. Obtain permission for
  research use. PHQ-9 and GAD-7 are public domain.

## Data location

`migraine_study.db` lives next to `app.py`. Back it up between clinic days.
For multi-device use later, swap the SQLite layer in
[database.py](database.py) for Google Sheets or a hosted Postgres.

# Migraine Clinic Research App

A small Streamlit web app for a clinic-based migraine study.
Patients fill HIT-6, PHQ-9, GAD-7, headache days, and an understanding score
in English / Hindi / Marathi. Scores are computed automatically, records are
stored in a private Google Sheet, and the data is exportable as CSV/Excel.

## Files

- [app.py](app.py) — Streamlit UI (auth, new record, follow-up comparison, export)
- [questionnaires.py](questionnaires.py) — item text + response options in all three languages
- [scoring.py](scoring.py) — HIT-6, PHQ-9, GAD-7 totals + severity categories
- [database.py](database.py) — Google Sheets read/write (same API the old SQLite layer used)
- [.streamlit/secrets.toml.example](.streamlit/secrets.toml.example) — template for credentials

## How it runs

The app is hosted on **Streamlit Community Cloud** so you can open it from any
phone or laptop browser. All records are written to a single private Google
Sheet you own. A shared password gates access.

### Live URL

<https://migraine-study-app.streamlit.app/>

Open it on your phone, sign in once, then "Add to Home Screen" so it
behaves like an installed app.

## One-time setup

### 1. Create a Google Sheet

1. In Google Drive, create a new blank sheet. Name it e.g. `migraine-study`.
2. Copy the full URL — you'll paste it into secrets later.

### 2. Create a Google service account (so the app can write to the sheet)

1. Go to <https://console.cloud.google.com/> and create a new project
   (e.g. `migraine-study`).
2. Enable the **Google Sheets API** and **Google Drive API** for the project
   (APIs & Services → Library).
3. APIs & Services → Credentials → Create credentials → Service account.
   Name it `streamlit-writer`. Skip the optional steps.
4. Open the service account → Keys → Add key → JSON. Download the JSON file.
5. Copy the service account's email (looks like
   `streamlit-writer@<project>.iam.gserviceaccount.com`).
6. Open the Google Sheet → Share → paste that email → give **Editor** access.

### 3. Configure Streamlit secrets

Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in:

- `APP_PASSWORD` — a long random string (you'll type this when signing in).
- `sheet_url` — the Google Sheet URL from step 1.
- `[gcp_service_account]` — the values from the JSON you downloaded.
  Keep the `\n` characters inside the `private_key` value.

`secrets.toml` is gitignored; never commit it.

### 4. Run locally (optional)

```powershell
pip install -r requirements.txt
python -m streamlit run app.py
```

Opens at <http://localhost:8501>.

### 5. Deploy to Streamlit Community Cloud

1. Push the repo to GitHub (already at `github.com/sudhirkots/migraine-study-app`).
2. Go to <https://share.streamlit.io/> → New app.
3. Pick the repo, branch `main`, main file `app.py`.
4. Open the app's Settings → Secrets and paste the **same** contents as your
   local `.streamlit/secrets.toml`.
5. Deploy. The URL it gives you (e.g. `https://migraine-study.streamlit.app`)
   is what you bookmark on the phone.

### 6. Add to phone home screen

- **iPhone (Safari)**: open the URL → Share → Add to Home Screen.
- **Android (Chrome)**: open the URL → ⋮ menu → Add to Home screen / Install app.

The icon launches the app full-screen with no browser chrome.

## What the app does

1. **Sign in** — single shared password.
2. **New record** — pick language, enter patient study code / age / sex /
   visit type (baseline or follow-up), fill the three questionnaires, headache
   days, and understanding score. Live preview of HIT-6 / PHQ-9 / GAD-7
   totals and severity bands. Save appends a row to the Google Sheet.
3. **Baseline vs follow-up** — pick a patient ID, see baseline vs latest
   follow-up side-by-side with a per-measure verdict
   (Improved / Unchanged / Worse, based on each instrument's MCID).
4. **Export data** — full CSV or Excel download of every record.

## Safety hook

If PHQ-9 item 9 (self-harm thoughts) ≥ 1, the new-record page shows a red
clinician alert before save. Don't ignore it.

## Translation notes

- **Marathi HIT-6**: finalized with the investigator on 2026-06-18. The
  intended next step is a paper pilot with 10 consecutive migraine
  patients, asking only "यातला कुठला प्रश्न समजायला कठीण वाटला का?"
  Pilot first, edit later.
- **PHQ-9 and GAD-7 (English / Hindi / Marathi)**: official India-localized
  versions, Pfizer Inc. educational grant. Source PDFs are in [assets/](assets/).
  No permission required to reproduce, translate, display or distribute.
- **Hindi HIT-6**: working draft pending the investigator's validated version.
- **HIT-6 licensing**: HIT-6 is © QualityMetric. Obtain permission for
  research use, including hosting the app on the public internet.

## Data location

Records live in your private Google Sheet — open it in Drive to view or edit
raw rows. Streamlit Cloud holds no copy of the data on its filesystem.
For backups, use Drive's revision history or download the sheet as `.xlsx`
periodically.

## Patient privacy

- The patient ID field is a **study code** (e.g. `MIG-001`), not a name.
- The shared password is the only access control — pick a long random string
  and rotate it if it leaks.
- The deployed URL is public, but the data behind it is not.

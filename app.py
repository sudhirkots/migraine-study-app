"""Migraine clinic research app — Streamlit MVP.

Run:
    streamlit run app.py
"""

from datetime import date
from io import BytesIO

import pandas as pd
import streamlit as st

import database as db
import questionnaires as Q
import scoring


st.set_page_config(page_title="Migraine Clinic Research", layout="centered")
db.init_db()


# -------------------- helpers --------------------
def t(key: str, lang: str) -> str:
    """Lookup a UI string by key for the chosen language."""
    return Q.UI[key][lang]


def render_questionnaire(name: str, lang: str, key_prefix: str):
    """Render a radio-button questionnaire. Returns list[int] of selected values."""
    items, options, values, _ = Q.get_questionnaire(name, lang)
    responses = []
    for i, item in enumerate(items):
        st.markdown(f"**{i + 1}. {item}**")
        choice = st.radio(
            label=f"{name}_{i}",
            options=list(range(len(options))),
            format_func=lambda j, _opts=options: _opts[j],
            key=f"{key_prefix}_{name}_{i}",
            horizontal=True,
            label_visibility="collapsed",
            index=None,
        )
        responses.append(values[choice] if choice is not None else None)
    return responses


def severity_color(category: str) -> str:
    cat = category.lower()
    if "severe" in cat:
        return "#b00020"
    if "moderate" in cat or "substantial" in cat:
        return "#d97706"
    if "mild" in cat or "some" in cat:
        return "#ca8a04"
    if "minimal" in cat or "little" in cat:
        return "#16a34a"
    return "#6b7280"


# -------------------- sidebar --------------------
with st.sidebar:
    lang_label = st.selectbox(
        "Language / भाषा / भाषा",
        list(Q.LANGUAGES.keys()),
        index=0,
    )
    lang = Q.LANGUAGES[lang_label]

    st.title(t("title", lang))
    page = st.radio(
        "Navigation",
        [t("nav_new", lang), t("nav_followup", lang), t("nav_export", lang)],
        label_visibility="collapsed",
    )


# -------------------- page: new record --------------------
if page == t("nav_new", lang):
    st.header(t("nav_new", lang))

    col1, col2, col3 = st.columns(3)
    with col1:
        patient_id = st.text_input(t("patient_id", lang))
    with col2:
        age = st.number_input(t("age", lang), min_value=0, max_value=120, step=1, value=30)
    with col3:
        sex = st.selectbox(t("sex", lang), Q.UI["sex_options"][lang])

    col4, col5 = st.columns(2)
    with col4:
        visit_type = st.selectbox(t("visit_type", lang), Q.UI["visit_options"][lang])
    with col5:
        visit_date = st.date_input("Date", value=date.today())

    # normalize visit_type to English for storage so cross-language data merges cleanly
    visit_idx = Q.UI["visit_options"][lang].index(visit_type)
    visit_type_en = Q.UI["visit_options"]["en"][visit_idx]

    st.divider()
    st.subheader(t("hit6", lang))
    hit6_responses = render_questionnaire("HIT6", lang, "new")

    st.divider()
    st.subheader(t("phq9", lang))
    st.caption(Q.PHQ9_PROMPT[lang])
    phq9_responses = render_questionnaire("PHQ9", lang, "new")

    st.divider()
    st.subheader(t("gad7", lang))
    st.caption(Q.GAD7_PROMPT[lang])
    gad7_responses = render_questionnaire("GAD7", lang, "new")

    st.divider()
    st.subheader(t("other", lang))
    col6, col7 = st.columns(2)
    with col6:
        headache_days = st.number_input(
            Q.HEADACHE_DAYS_LABEL[lang], min_value=0, max_value=31, step=1, value=0
        )
    with col7:
        understanding = st.slider(Q.UNDERSTANDING_LABEL[lang], 0, 10, 5)

    notes = st.text_area("Notes (optional)")

    st.divider()

    # Live preview of scores
    hit6_score, hit6_cat = scoring.score_hit6(hit6_responses)
    phq9_score, phq9_cat = scoring.score_phq9(phq9_responses)
    gad7_score, gad7_cat = scoring.score_gad7(gad7_responses)
    suicidality = scoring.phq9_suicidality_flag(phq9_responses)

    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("HIT-6", hit6_score if hit6_cat != "Incomplete" else "—", hit6_cat)
    sc2.metric("PHQ-9", phq9_score if phq9_cat != "Incomplete" else "—", phq9_cat)
    sc3.metric("GAD-7", gad7_score if gad7_cat != "Incomplete" else "—", gad7_cat)

    if suicidality:
        st.error(
            "⚠ PHQ-9 item 9 indicates thoughts of self-harm. "
            "Clinician review before the patient leaves the clinic."
        )

    if st.button(t("submit", lang), type="primary"):
        if not patient_id.strip():
            st.error("Patient ID is required.")
        elif "Incomplete" in (hit6_cat, phq9_cat, gad7_cat):
            st.error("Please complete all questionnaire items before saving.")
        else:
            record = {
                "patient_id": patient_id.strip(),
                "age": int(age),
                "sex": sex,
                "language": lang,
                "visit_type": visit_type_en,
                "visit_date": visit_date.isoformat(),
                "hit6_items": hit6_responses,
                "hit6_score": hit6_score,
                "hit6_category": hit6_cat,
                "phq9_items": phq9_responses,
                "phq9_score": phq9_score,
                "phq9_category": phq9_cat,
                "phq9_suicidality": suicidality,
                "gad7_items": gad7_responses,
                "gad7_score": gad7_score,
                "gad7_category": gad7_cat,
                "headache_days": int(headache_days),
                "understanding_score": int(understanding),
                "notes": notes.strip() or None,
            }
            rec_id = db.save_record(record)
            st.success(f"{t('saved', lang)} (id={rec_id})")


# -------------------- page: baseline vs follow-up --------------------
elif page == t("nav_followup", lang):
    st.header(t("nav_followup", lang))

    ids = db.list_patient_ids()
    if not ids:
        st.info("No records yet.")
    else:
        pid = st.selectbox("Patient ID", ids)
        baseline = db.latest_visit(pid, "Baseline")
        followup = db.latest_visit(pid, "Follow-up")

        if not baseline:
            st.warning("No baseline record for this patient.")
        if not followup:
            st.info("No follow-up record yet for this patient.")

        if baseline and followup:
            rows = []
            for name, b_key, f_key, mcid_key in [
                ("HIT-6", "hit6_score", "hit6_score", "HIT6"),
                ("PHQ-9", "phq9_score", "phq9_score", "PHQ9"),
                ("GAD-7", "gad7_score", "gad7_score", "GAD7"),
            ]:
                b = baseline[b_key]
                f = followup[f_key]
                verdict = scoring.change_label(b, f, scoring.MCID[mcid_key])
                rows.append({"Measure": name, "Baseline": b, "Follow-up": f, "Change": f - b, "Verdict": verdict})

            b_days = baseline["headache_days"]
            f_days = followup["headache_days"]
            rows.append({
                "Measure": "Headache days/month",
                "Baseline": b_days,
                "Follow-up": f_days,
                "Change": f_days - b_days,
                "Verdict": "Reduced" if f_days < b_days else ("Increased" if f_days > b_days else "Unchanged"),
            })

            b_u = baseline["understanding_score"]
            f_u = followup["understanding_score"]
            rows.append({
                "Measure": "Understanding (0–10)",
                "Baseline": b_u,
                "Follow-up": f_u,
                "Change": f_u - b_u,
                "Verdict": "Improved" if f_u > b_u else ("Worse" if f_u < b_u else "Unchanged"),
            })

            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.caption(
                f"Baseline visit: {baseline['visit_date']} · "
                f"Follow-up visit: {followup['visit_date']}"
            )


# -------------------- page: export --------------------
elif page == t("nav_export", lang):
    st.header(t("nav_export", lang))
    df = db.all_records_dataframe()
    st.write(f"{len(df)} records in database.")
    if not df.empty:
        st.dataframe(df.head(20), use_container_width=True)

        csv_bytes = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "Download CSV",
            data=csv_bytes,
            file_name="migraine_study.csv",
            mime="text/csv",
        )

        buf = BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="records", index=False)
        st.download_button(
            "Download Excel",
            data=buf.getvalue(),
            file_name="migraine_study.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

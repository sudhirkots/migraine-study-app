"""Brainwaves Migraine Research App — Streamlit data-entry wizard.

Run:
    streamlit run app.py
"""

from datetime import date
from pathlib import Path

import streamlit as st

import database as db
import questionnaires as Q
import scoring


APP_TITLE = "Brainwaves Migraine Research App"
LOGO_PATH = Path(__file__).parent / "assets" / "brainwaves_logo.png"

st.set_page_config(
    page_title="Brainwaves Migraine Research",
    page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else None,
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Hide the sidebar and its collapse control entirely — the patient-facing
# flow is the whole app. Also bump wizard buttons to a larger size so the
# face emojis on the understanding question (and tap targets in general)
# are comfortable on a phone.
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    /* Tighten outer padding so a HIT-6 / PHQ-9 / GAD-7 / MUCS screen
       (banner + question + 5 buttons + back/next) fits a phone viewport
       without scrolling. */
    .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
    h1, h2, h3, h4 { margin-top: 0.25rem !important; margin-bottom: 0.4rem !important; }
    .stMarkdown { margin-bottom: 0.25rem !important; }
    /* Compact, tap-friendly buttons. Smaller padding + line-height
       than the earlier version so all options fit above the fold. */
    .stButton button { padding: 0.5rem 0.9rem !important; margin: 0.1rem 0 !important; }
    .stButton button p {
        font-size: 1.1rem !important;
        line-height: 1.35 !important;
        margin: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_brand_header() -> None:
    """Logo + app name at the top of every screen."""
    if LOGO_PATH.exists():
        col_logo, col_name = st.columns([1, 5])
        col_logo.image(str(LOGO_PATH), width=72)
        col_name.markdown(f"## {APP_TITLE}")
    else:
        st.markdown(f"## {APP_TITLE}")


# -------------------- auth gate --------------------
def _require_password() -> None:
    """Block the app behind a shared password held in st.secrets.

    Set APP_PASSWORD in .streamlit/secrets.toml locally, and in the
    Streamlit Cloud secrets UI for the deployed app.
    """
    expected = st.secrets.get("APP_PASSWORD")
    if not expected:
        st.error(
            "APP_PASSWORD is not configured in Streamlit secrets. "
            "Add it before using the app."
        )
        st.stop()

    if st.session_state.get("_auth_ok"):
        return

    render_brand_header()
    pw = st.text_input("Password", type="password")
    if st.button("Sign in", type="primary"):
        if pw == expected:
            st.session_state["_auth_ok"] = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()


_require_password()
db.init_db()
render_brand_header()


# -------------------- helpers --------------------
def t(key: str, lang: str) -> str:
    """Lookup a UI string by key for the chosen language."""
    return Q.UI[key][lang]


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


# -------------------- visit-type localization --------------------
# Conversational question + short button labels per language. The values
# list is the canonical English used for storage (so cross-language data
# merges cleanly and the baseline-vs-follow-up logic stays simple).
VISIT_PROMPT = {
    "en": "Are you a new patient or is this a follow-up visit?",
    "hi": "आप पहली बार आए हैं या यह आपने पहले डॉक्टर साहब को बता के अब फिर से दिखाने आए हैं?",
    "mr": "तुम्ही पहिल्यांदा पेशंट म्हणून आले आहात का? ही तुमची दुसरी किंवा तिसरी भेट आहे का?",
}
VISIT_BUTTONS = {
    "en": ["New patient (first visit)", "Follow-up visit"],
    "hi": ["पहली बार", "फॉलो-अप"],
    "mr": ["पहिल्यांदा", "फॉलो-अप"],
}
VISIT_STORAGE = ["Baseline", "Follow-up"]

# Emoji prefixes for validated instruments. The option lists are ordered
# from least → most severe, so the emoji ramp is best (😊) → worst (😕).
# MUCS uses agree/disagree wording and is rendered without emoji
# (see build_steps) to avoid emotional-valence confusion on reverse-scored items.
EMOJI_BY_OPTION_COUNT = {
    4: ["😊", "🙂", "🤔", "😕"],          # PHQ-9, GAD-7
    5: ["😊", "🙂", "😐", "🤔", "😕"],     # HIT-6
}


# -------------------- wizard helpers --------------------
def _reset_wizard():
    for k in list(st.session_state.keys()):
        if k.startswith("w_") or k in ("wizard_idx", "wizard_answers", "wizard_lang"):
            del st.session_state[k]


def _commit_value(key: str, value):
    """Store an answer and step forward (used by button clicks)."""
    st.session_state["wizard_answers"][key] = value
    st.session_state["wizard_idx"] += 1


def _commit_widget(key: str, transform=None) -> None:
    """on_change callback for text/number inputs that commit on Enter/blur."""
    wkey = f"w_{key}"
    val = st.session_state.get(wkey)
    if val is None or (isinstance(val, str) and not val.strip()):
        return
    if transform is not None:
        val = transform(val)
    _commit_value(key, val)


def build_steps(lang: str) -> list[dict]:
    """One step per question for the new-record wizard.

    Order: visit type → patient id → age → sex → questionnaires →
    headache days → understanding → notes → review.

    Language is asked once before the wizard starts (see new-record page).
    Date is captured silently as today's date — no question.
    """
    steps: list[dict] = [
        {"kind": "buttons", "key": "visit_type",
         "prompt": VISIT_PROMPT[lang],
         "options": VISIT_BUTTONS[lang],
         "values": VISIT_STORAGE},
        {"kind": "text", "key": "patient_id", "label": t("patient_id", lang),
         "hint": t("patient_id_hint", lang), "placeholder": "MIG-001"},
        {"kind": "number", "key": "age", "label": t("age", lang),
         "min": 0, "max": 120, "step": 1},
        {"kind": "buttons", "key": "sex", "label": t("sex", lang),
         "options": Q.UI["sex_options"][lang]},
    ]

    for name, prompt_attr, section, use_emoji in [
        ("HIT6", None, t("hit6", lang), True),
        ("PHQ9", "PHQ9_PROMPT", t("phq9", lang), True),
        ("GAD7", "GAD7_PROMPT", t("gad7", lang), True),
        # MUCS: agree/disagree Likert. Skip emoji because items 7-9 are
        # reverse-scored — a smile next to "I'm afraid of getting a headache"
        # would conflict with the answer's actual meaning.
        ("MUCS", "MUCS_PROMPT", t("mucs", lang), False),
    ]:
        items, options, values, _ = Q.get_questionnaire(name, lang)
        prompt = getattr(Q, prompt_attr)[lang] if prompt_attr else None
        for i, item in enumerate(items):
            steps.append({
                "kind": "item", "key": f"{name.lower()}_{i}",
                "section": section, "prompt": prompt, "label": item,
                "options": options, "values": values,
                "i": i, "total": len(items),
                "no_emoji": not use_emoji,
            })

    steps += [
        {"kind": "number", "key": "headache_days",
         "label": Q.HEADACHE_DAYS_LABEL[lang], "min": 0, "max": 31, "step": 1},
        {"kind": "textarea", "key": "notes",
         "label": "Notes (optional)", "optional": True},
        {"kind": "review"},
    ]
    return steps


def render_step(step: dict) -> tuple:
    """Render one step.

    Returns (value, answered, manual_next) where:
      - value: current widget value (None for steps that commit via buttons)
      - answered: whether a valid answer is present
      - manual_next: True if the outer Next button should be shown
    """
    kind = step["kind"]
    wkey = f"w_{step['key']}" if "key" in step else None

    if kind == "text":
        v = st.text_input(step["label"], placeholder=step.get("placeholder", ""),
                          help=step.get("hint"), key=wkey,
                          on_change=_commit_widget, args=(step["key"],))
        return v, bool(v and v.strip()), True

    if kind == "number":
        v = st.number_input(step["label"], min_value=step["min"],
                            max_value=step["max"], step=step["step"],
                            value=None, key=wkey,
                            on_change=_commit_widget, args=(step["key"],))
        return v, v is not None, True

    if kind == "slider":
        v = st.slider(step["label"], step["min"], step["max"],
                      step.get("default", step["min"]), key=wkey)
        return v, True, True

    if kind == "textarea":
        v = st.text_area(step["label"], key=wkey)
        return v, True, True

    if kind == "buttons":
        # Big full-width buttons, one per option. A click commits and advances.
        # `prompt` (sentence) or `label` (short title) goes above the buttons.
        # `values` (optional) lets the button label differ from the stored value.
        # `container_key` (optional) wraps the buttons in a keyed container so
        # CSS can target this specific group (used to enlarge the smileys).
        container = (
            st.container(key=step["container_key"])
            if step.get("container_key") else st.container()
        )
        with container:
            st.markdown(f"### {step.get('prompt') or step.get('label', '')}")
            storage = step.get("values") or step["options"]
            for j, opt in enumerate(step["options"]):
                st.button(
                    opt, key=f"{wkey}_b{j}", use_container_width=True,
                    on_click=_commit_value, args=(step["key"], storage[j]),
                )
        return None, False, False

    if kind == "item":
        # Bold instrument banner + counter on a single compact line so the
        # full screen (banner + question + 5 buttons + back/next) fits a
        # phone viewport without scrolling.
        st.markdown(f"**{step['section']} — {step['i'] + 1}/{step['total']}**")
        if step.get("prompt"):
            st.caption(step["prompt"])
        st.markdown(f"#### {step['label']}")
        emojis = (
            [] if step.get("no_emoji")
            else EMOJI_BY_OPTION_COUNT.get(len(step["options"]), [])
        )
        for j, opt in enumerate(step["options"]):
            label = f"{emojis[j]}  {opt}" if j < len(emojis) else opt
            st.button(
                label, key=f"{wkey}_b{j}", use_container_width=True,
                on_click=_commit_value,
                args=(step["key"], step["values"][j]),
            )
        return None, False, False

    return None, True, True


def render_language_picker() -> None:
    """First-screen language picker. Each language's question IS the button."""

    def _pick(code: str):
        st.session_state["wizard_lang"] = code
        st.session_state["wizard_idx"] = 0
        st.session_state["wizard_answers"] = {}

    st.button("Do you want it in English?", key="_lang_en",
              use_container_width=True, on_click=_pick, args=("en",))
    st.button("आपको हिंदी चाहिए क्या?", key="_lang_hi",
              use_container_width=True, on_click=_pick, args=("hi",))
    st.button("तुम्हाला मराठी पाहिजे का?", key="_lang_mr",
              use_container_width=True, on_click=_pick, args=("mr",))


# -------------------- wizard (the whole app) --------------------
if "wizard_lang" not in st.session_state:
    render_language_picker()
    st.stop()

lang = st.session_state["wizard_lang"]
steps = build_steps(lang)
total = len(steps)

idx = st.session_state["wizard_idx"]
step = steps[idx]
answers = st.session_state["wizard_answers"]

st.progress((idx + 1) / total, text=f"{idx + 1} / {total}")

if step["kind"] == "review":
    hit6 = [answers.get(f"hit6_{i}") for i in range(6)]
    phq9 = [answers.get(f"phq9_{i}") for i in range(9)]
    gad7 = [answers.get(f"gad7_{i}") for i in range(7)]
    mucs = [answers.get(f"mucs_{i}") for i in range(9)]
    hit6_score, hit6_cat = scoring.score_hit6(hit6)
    phq9_score, phq9_cat = scoring.score_phq9(phq9)
    gad7_score, gad7_cat = scoring.score_gad7(gad7)
    mucs_score, mucs_cat = scoring.score_mucs(mucs)
    suicidality = scoring.phq9_suicidality_flag(phq9)

    st.subheader("Review")

    st.markdown(f"### **HIT-6:** {hit6_score} — {hit6_cat}")
    st.markdown(f"### **PHQ-9:** {phq9_score} — {phq9_cat}")
    st.markdown(f"### **GAD-7:** {gad7_score} — {gad7_cat}")
    st.markdown(f"### **MUCS:** {mucs_score} — {mucs_cat}")

    if suicidality:
        st.error(
            "⚠ PHQ-9 item 9 indicates thoughts of self-harm. "
            "Clinician review before the patient leaves the clinic."
        )

    st.caption(f"Patient: {answers.get('patient_id')} · age {answers.get('age')} · {answers.get('sex')}")
    st.caption(f"Visit: {answers.get('visit_type')} (today)")
    st.caption(f"Headache days/month: {answers.get('headache_days')}")
    if answers.get("notes"):
        st.caption(f"Notes: {answers['notes']}")

    col_back, col_save = st.columns(2)
    if col_back.button("← Back", key="wiz_review_back"):
        st.session_state["wizard_idx"] -= 1
        st.rerun()
    if col_save.button(t("submit", lang), type="primary", key="wiz_save"):
        record = {
            "patient_id": answers["patient_id"].strip(),
            "age": int(answers["age"]),
            "sex": answers["sex"],
            "language": lang,
            "visit_type": answers["visit_type"],
            "visit_date": date.today().isoformat(),
            "hit6_items": hit6,
            "hit6_score": hit6_score,
            "hit6_category": hit6_cat,
            "phq9_items": phq9,
            "phq9_score": phq9_score,
            "phq9_category": phq9_cat,
            "phq9_suicidality": suicidality,
            "gad7_items": gad7,
            "gad7_score": gad7_score,
            "gad7_category": gad7_cat,
            "mucs_items": mucs,
            "mucs_score": mucs_score,
            "mucs_category": mucs_cat,
            "headache_days": int(answers["headache_days"]),
            "notes": (answers.get("notes") or "").strip() or None,
        }
        rec_id = db.save_record(record)
        st.success(f"{t('saved', lang)} (id={rec_id})")
        _reset_wizard()
        st.button("Enter another record", on_click=lambda: None)
else:
    value, answered, manual_next = render_step(step)

    # Bottom button row — Back available after step 0; Next only
    # shown for kinds that need a manual commit (text/number/slider/notes).
    col_back, col_next = st.columns(2)
    if idx > 0:
        if col_back.button("← Back", key=f"wiz_back_{idx}"):
            st.session_state["wizard_idx"] -= 1
            st.rerun()

    if manual_next:
        can_advance = answered or step.get("optional", False)
        if col_next.button("Next →", key=f"wiz_next_{idx}",
                           type="primary", disabled=not can_advance):
            answers[step["key"]] = value
            st.session_state["wizard_idx"] += 1
            st.rerun()

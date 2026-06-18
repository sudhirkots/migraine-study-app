"""
Questionnaire items in English, Hindi, Marathi.

Notes for the investigator:
- HIT-6 is owned by QualityMetric; obtain permission for research use.
  Officially translated versions exist for Hindi and Marathi via IQVIA/QualityMetric.
- PHQ-9 and GAD-7 are public domain. Validated Hindi versions are available
  in the literature; Marathi versions have been published but should be
  cross-checked against the source you cite in your study protocol before
  collecting real data.
- Treat the strings below as a working draft. Replace any item text with the
  exact wording from your validated source as required by your ethics committee.
"""

LANGUAGES = {"English": "en", "Hindi": "hi", "Marathi": "mr"}

# -------------------- HIT-6 --------------------
# 5 response options, scored 6/8/10/11/13
HIT6_OPTIONS = {
    "en": ["Never", "Rarely", "Sometimes", "Very often", "Always"],
    "hi": ["कभी नहीं", "बहुत कम", "कभी-कभी", "अक्सर", "हमेशा"],
    # Marathi response set — finalized with the investigator (2026-06-18)
    "mr": ["कधीच नाही", "क्वचित", "कधी कधी", "बऱ्याचदा", "जवळजवळ रोज"],
}
HIT6_VALUES = [6, 8, 10, 11, 13]

HIT6_ITEMS = {
    "en": [
        "When you have headaches, how often is the pain severe?",
        "How often do headaches limit your ability to do usual daily activities including household work, work, school, or social activities?",
        "When you have a headache, how often do you wish you could lie down?",
        "In the past 4 weeks, how often have you felt too tired to do work or daily activities because of your headaches?",
        "In the past 4 weeks, how often have you felt fed up or irritated because of your headaches?",
        "In the past 4 weeks, how often did headaches limit your ability to concentrate on work or daily activities?",
    ],
    "hi": [
        "जब आपको सिरदर्द होता है, तो दर्द कितनी बार गंभीर होता है?",
        "सिरदर्द कितनी बार आपके रोज़मर्रा के कामों — घर, ऑफिस, स्कूल या सामाजिक गतिविधियों — को सीमित करते हैं?",
        "जब आपको सिरदर्द होता है, तो आपको कितनी बार लेटने की इच्छा होती है?",
        "पिछले 4 हफ्तों में, सिरदर्द की वजह से आप कितनी बार काम या रोज़मर्रा के कामों के लिए बहुत थका हुआ महसूस करते थे?",
        "पिछले 4 हफ्तों में, सिरदर्द की वजह से आप कितनी बार परेशान या चिड़चिड़ा महसूस करते थे?",
        "पिछले 4 हफ्तों में, सिरदर्द ने कितनी बार आपकी काम या रोज़मर्रा की गतिविधियों पर ध्यान केंद्रित करने की क्षमता को सीमित किया?",
    ],
    # Marathi HIT-6 — finalized wording from the investigator (2026-06-18).
    # Next step is real-world pilot with 10 consecutive migraine patients,
    # not further editing.
    "mr": [
        "जेव्हा तुमचं डोकं दुखतं, तेव्हा दुखणं किती वेळा खूप जास्त असतं?",
        "डोकेदुखीमुळे तुमची रोजची कामं (घरातली, शाळेची किंवा इतर) किती वेळा अवघड जातात?",
        "जेव्हा तुमचं डोकं दुखतं, तेव्हा तुम्हाला किती वेळा जाऊन थोडा वेळ आडवं पडावंसं वाटतं?",
        "गेल्या चार आठवड्यांत, डोकेदुखीमुळे तुम्हाला किती वेळा इतकं थकल्यासारखं वाटलं की रोजची कामं करणं अवघड झालं?",
        "गेल्या चार आठवड्यांत, डोकेदुखीमुळे तुम्हाला किती वेळा वैताग आला किंवा चिडचिड झाली?",
        "गेल्या चार आठवड्यांत, डोकेदुखीमुळे रोजच्या कामांमध्ये लक्ष लागणं किती वेळा अवघड झालं?",
    ],
}

# -------------------- PHQ-9 --------------------
# 4 response options, scored 0/1/2/3
PHQ9_OPTIONS = {
    "en": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
    "hi": ["बिल्कुल नहीं", "कुछ दिन", "आधे से अधिक दिन", "लगभग हर दिन"],
    "mr": ["अजिबात नाही", "काही दिवस", "अर्ध्याहून जास्त दिवस", "जवळजवळ रोज"],
}
PHQ9_VALUES = [0, 1, 2, 3]

PHQ9_PROMPT = {
    "en": "Over the last 2 weeks, how often have you been bothered by any of the following problems?",
    "hi": "पिछले 2 हफ्तों में, निम्नलिखित में से कोई समस्या आपको कितनी बार परेशान कर रही है?",
    "mr": "मागील २ आठवड्यांत, खालीलपैकी कोणत्या समस्यांनी तुम्हाला किती वेळा त्रास दिला आहे?",
}

PHQ9_ITEMS = {
    "en": [
        "Little interest or pleasure in doing things",
        "Feeling down, depressed, or hopeless",
        "Trouble falling or staying asleep, or sleeping too much",
        "Feeling tired or having little energy",
        "Poor appetite or overeating",
        "Feeling bad about yourself — or that you are a failure or have let yourself or your family down",
        "Trouble concentrating on things, such as reading the newspaper or watching television",
        "Moving or speaking so slowly that other people could have noticed. Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual",
        "Thoughts that you would be better off dead, or of hurting yourself in some way",
    ],
    "hi": [
        "कामों में कम रुचि या आनंद महसूस होना",
        "उदास, निराश या हताश महसूस करना",
        "नींद आने में या सोते रहने में परेशानी, या बहुत अधिक सोना",
        "थका हुआ महसूस करना या ऊर्जा की कमी",
        "भूख कम लगना या ज़्यादा खाना",
        "खुद के बारे में बुरा महसूस करना — या यह कि आप असफल हैं या आपने अपने या परिवार को निराश किया है",
        "किसी काम पर ध्यान केंद्रित करने में परेशानी, जैसे अख़बार पढ़ना या टीवी देखना",
        "इतनी धीरे से चलना या बोलना कि दूसरों ने देखा हो; या इसके विपरीत — इतना बेचैन कि आप सामान्य से बहुत अधिक इधर-उधर घूम रहे हों",
        "यह विचार आना कि मर जाना बेहतर होगा, या खुद को किसी तरह नुकसान पहुँचाने के विचार",
    ],
    "mr": [
        "कामांमध्ये रुची किंवा आनंद कमी वाटणे",
        "दुःखी, निराश किंवा हताश वाटणे",
        "झोप येण्यास किंवा झोपून राहण्यास त्रास, किंवा खूप जास्त झोप येणे",
        "थकल्यासारखे वाटणे किंवा ऊर्जा कमी असणे",
        "भूक कमी लागणे किंवा जास्त खाणे",
        "स्वतःबद्दल वाईट वाटणे — किंवा तुम्ही अपयशी आहात किंवा स्वतःला किंवा कुटुंबाला निराश केले आहे असे वाटणे",
        "कोणत्याही गोष्टीवर लक्ष केंद्रित करण्यात अडचण, जसे की वर्तमानपत्र वाचणे किंवा टीव्ही पाहणे",
        "इतके सावकाश चालणे किंवा बोलणे की इतरांच्या लक्षात येईल; किंवा उलट — इतके अस्वस्थ की तुम्ही नेहमीपेक्षा खूप जास्त हालचाल करत असाल",
        "मरून जाणे बरे होईल असे विचार येणे, किंवा स्वतःला कोणत्याही प्रकारे इजा करण्याचे विचार",
    ],
}

# -------------------- GAD-7 --------------------
GAD7_OPTIONS = PHQ9_OPTIONS  # same response set
GAD7_VALUES = [0, 1, 2, 3]

GAD7_PROMPT = PHQ9_PROMPT

GAD7_ITEMS = {
    "en": [
        "Feeling nervous, anxious, or on edge",
        "Not being able to stop or control worrying",
        "Worrying too much about different things",
        "Trouble relaxing",
        "Being so restless that it is hard to sit still",
        "Becoming easily annoyed or irritable",
        "Feeling afraid as if something awful might happen",
    ],
    "hi": [
        "घबराहट, चिंता या बेचैनी महसूस करना",
        "चिंता को रोक पाने या काबू करने में असमर्थ होना",
        "अलग-अलग बातों की बहुत अधिक चिंता करना",
        "आराम करने में परेशानी",
        "इतना बेचैन होना कि एक जगह बैठना मुश्किल हो",
        "आसानी से चिढ़ना या नाराज़ होना",
        "ऐसा डर लगना जैसे कुछ भयानक होने वाला है",
    ],
    "mr": [
        "घाबरट, चिंताग्रस्त किंवा अस्वस्थ वाटणे",
        "चिंता थांबवता किंवा नियंत्रित करता न येणे",
        "वेगवेगळ्या गोष्टींबद्दल जास्त काळजी करणे",
        "आराम करण्यात अडचण",
        "इतके अस्वस्थ की एका जागी बसणे कठीण होईल",
        "सहज चिडचिड किंवा रागावणे",
        "काहीतरी भयानक घडणार आहे अशी भीती वाटणे",
    ],
}

# -------------------- Other items --------------------
HEADACHE_DAYS_LABEL = {
    "en": "Number of headache days in the past month",
    "hi": "पिछले महीने में कितने दिन सिरदर्द हुआ",
    "mr": "मागील महिन्यात किती दिवस डोकेदुखी झाली",
}

UNDERSTANDING_LABEL = {
    "en": "How well do you feel you understand your migraine? (0 = not at all, 10 = completely)",
    "hi": "आप अपने माइग्रेन को कितनी अच्छी तरह समझते हैं? (0 = बिल्कुल नहीं, 10 = पूरी तरह)",
    "mr": "तुम्हाला तुमचा मायग्रेन किती चांगल्या प्रकारे समजतो? (0 = अजिबात नाही, 10 = पूर्णपणे)",
}

# UI strings
UI = {
    "title": {
        "en": "Migraine Clinic Research App",
        "hi": "माइग्रेन क्लिनिक रिसर्च ऐप",
        "mr": "मायग्रेन क्लिनिक रिसर्च ॲप",
    },
    "choose_language": {
        "en": "Choose language",
        "hi": "भाषा चुनें",
        "mr": "भाषा निवडा",
    },
    "patient_id": {
        "en": "Patient ID",
        "hi": "मरीज़ की आईडी",
        "mr": "रुग्ण आयडी",
    },
    "age": {"en": "Age", "hi": "उम्र", "mr": "वय"},
    "sex": {"en": "Sex", "hi": "लिंग", "mr": "लिंग"},
    "sex_options": {
        "en": ["Female", "Male", "Other"],
        "hi": ["महिला", "पुरुष", "अन्य"],
        "mr": ["स्त्री", "पुरुष", "इतर"],
    },
    "visit_type": {"en": "Visit type", "hi": "विज़िट का प्रकार", "mr": "भेटीचा प्रकार"},
    "visit_options": {
        "en": ["Baseline", "Follow-up"],
        "hi": ["बेसलाइन", "फॉलो-अप"],
        "mr": ["बेसलाइन", "फॉलो-अप"],
    },
    "hit6": {"en": "HIT-6 (Headache Impact)", "hi": "HIT-6 (सिरदर्द प्रभाव)", "mr": "HIT-6 (डोकेदुखी प्रभाव)"},
    "phq9": {"en": "PHQ-9 (Depression)", "hi": "PHQ-9 (अवसाद)", "mr": "PHQ-9 (नैराश्य)"},
    "gad7": {"en": "GAD-7 (Anxiety)", "hi": "GAD-7 (चिंता)", "mr": "GAD-7 (चिंता)"},
    "other": {"en": "Other measures", "hi": "अन्य मापन", "mr": "इतर मापन"},
    "submit": {"en": "Save record", "hi": "रिकॉर्ड सेव करें", "mr": "नोंद जतन करा"},
    "saved": {"en": "Saved.", "hi": "सेव हो गया।", "mr": "जतन झाले."},
    "nav_new": {"en": "New record", "hi": "नया रिकॉर्ड", "mr": "नवीन नोंद"},
    "nav_followup": {"en": "Baseline vs follow-up", "hi": "बेसलाइन बनाम फॉलो-अप", "mr": "बेसलाइन वि. फॉलो-अप"},
    "nav_export": {"en": "Export data", "hi": "डेटा एक्सपोर्ट", "mr": "डेटा एक्सपोर्ट"},
}


def get_questionnaire(name: str, lang_code: str):
    """Return (items, options, values, scoring_kind) for a questionnaire."""
    if name == "HIT6":
        return HIT6_ITEMS[lang_code], HIT6_OPTIONS[lang_code], HIT6_VALUES, "HIT6"
    if name == "PHQ9":
        return PHQ9_ITEMS[lang_code], PHQ9_OPTIONS[lang_code], PHQ9_VALUES, "PHQ9"
    if name == "GAD7":
        return GAD7_ITEMS[lang_code], GAD7_OPTIONS[lang_code], GAD7_VALUES, "GAD7"
    raise ValueError(f"Unknown questionnaire: {name}")

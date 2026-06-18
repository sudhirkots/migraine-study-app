"""
Questionnaire items in English, Hindi, Marathi.

Sources:
- HIT-6: investigator-finalized Marathi wording (locked 2026-06-18).
  English wording is the standard QualityMetric item set.
  Hindi is a working draft pending the investigator's validated version.
  HIT-6 is owned by QualityMetric; obtain permission for research use.
- PHQ-9 (English / Hindi / Marathi): official India-localized version,
  Pfizer Inc. educational grant. See assets/PHQ-9_English.pdf,
  assets/PHQ9_Hindi for India.pdf, assets/PHQ9_Marathi for India.pdf.
  No permission required to reproduce, translate, display or distribute.
- GAD-7 (English / Hindi / Marathi): official India-localized version,
  Pfizer Inc. educational grant. See assets/GAD-7_English.pdf,
  assets/GAD7_Hindi for India.pdf, assets/GAD7_Marathi for India.pdf.
  No permission required to reproduce, translate, display or distribute.
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
# Official India-localized PHQ-9 (English/Hindi/Marathi).
# Source: Pfizer Inc. educational grant; "No permission required to reproduce,
# translate, display or distribute" per the source PDFs.
# 4 response options, scored 0/1/2/3
PHQ9_OPTIONS = {
    "en": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
    "hi": ["बिल्कुल नहीं", "कई दिन", "आधे से अधिक दिन", "लगभग हर दिन"],
    "mr": ["अजिबात नाही", "अनेक दिवस", "अर्ध्याहून अधिक दिवस", "जवळपास प्रत्येक दिवशी"],
}
PHQ9_VALUES = [0, 1, 2, 3]

PHQ9_PROMPT = {
    "en": "Over the last 2 weeks, how often have you been bothered by any of the following problems?",
    "hi": "पिछले 2 सप्ताहों में, आप इन समस्याओं में से किसी से भी कितनी बार परेशान रहे/रही हैं?",
    "mr": "मागील 2 आठवड्यांच्या काळात, आपल्याला खालील पैकी कोणत्याही समस्येमुळे कितीवेळा त्रास झाला आहे?",
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
        "Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual",
        "Thoughts that you would be better off dead or of hurting yourself in some way",
    ],
    "hi": [
        "कुछ करने में बहुत कम दिलचस्पी या मज़ा आना",
        "उदास, अवसादग्रस्त या निराश महसूस करना",
        "नींद आने या सोये रहने में परेशानी, या फिर बहुत अधिक सोना",
        "थकान महसूस करना या बहुत कम ऊर्जा होना",
        "भूख कम लगना या ज़्यादा खाना",
        "अपने बारे में बुरा महसूस करना - या ऐसा महसूस करना कि आप नाकाम इंसान हैं और आपने खुद को और अपने परिवार को नीचा दिखाया है",
        "अखबार पढ़ने या टेलीविज़न देखने जैसी चीज़ों पर ध्यान देने में परेशानी",
        "इतना धीमे चलना-फिरना या बोलना कि लोगों का ध्यान जाये? या इसका उल्टा - इतना अस्थिर या बेचैन होना कि आप सामान्य से काफ़ी ज़्यादा हिलते-डुलते और चलते-फिरते रहे हैं",
        "ऐसे विचार कि आप मर जाते तो अच्छा होता या किसी ढंग से ख़ुद को नुक्सान पहुंचाना",
    ],
    "mr": [
        "गोष्टी करण्यात थोडीशी रुचि किंवा आनंद",
        "हताश, उद्वीग्नता, किंवा निराश वाटणे",
        "झोप लागण्यात किंवा झोपलेले राहण्यात समस्या, किंवा खूप झोप येणे",
        "थकलेले किंवा थोडी ऊर्जा असल्याचे वाटले",
        "भूक मंदावणे किंवा अति खाणे",
        "स्वतःबद्दल वाईट वाटणे — किंवा आपण अपयशी आहोत किंवा आपण स्वतःचा किंवा आपल्या कुटुंबाचा अपेक्षाभंग केला आहे असे वाटणे",
        "वर्तमानपत्र वाचणे किंवा टेलिव्हिजन पाहणे यासारख्या गोष्टींवर लक्ष एकाग्र करण्यास त्रास होणे",
        "हालचाल किंवा बोलणे इतके संथ होते की इतर लोकांच्या लक्षात येणे? किंवा याच्या उलट — इतके चिंताक्रांत किंवा अस्वस्थ होणे की आपण सामान्यपेक्षा बरेच अधिक इकडे-तिकडे फिरत आहात",
        "आपण मेलो असतो तर चांगले झाले असते किंवा स्वतःला काही प्रकाराने जखमी करुन घेण्याचे विचार",
    ],
}

# -------------------- GAD-7 --------------------
# Official India-localized GAD-7 (English/Hindi/Marathi).
# Source: Pfizer Inc. educational grant; "No permission required to reproduce,
# translate, display or distribute" per the source PDFs.
# Note: GAD-7 response options and prompt differ slightly from PHQ-9 in
# Hindi and Marathi, so they get their own dicts rather than aliasing PHQ-9.
GAD7_OPTIONS = {
    "en": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
    "hi": ["बिल्कुल नहीं", "कई दिनों तक", "आधे से ज्यादा दिनों तक", "लगभग रोज़ाना"],
    "mr": ["मुळीच नाही", "अनेक दिवस", "अर्ध्याहून अधिक दिवस", "जवळजवळ दररोज"],
}
GAD7_VALUES = [0, 1, 2, 3]

GAD7_PROMPT = {
    "en": "Over the last 2 weeks, how often have you been bothered by the following problems?",
    "hi": "पिछले 2 सप्ताहों के दौरान, आप निम्नलिखित समस्याओं से कितनी बार परेशान हुए?",
    "mr": "गेल्या 2 आठवड्यांमध्ये, तुम्हाला खालील समस्यांचा किती वेळा त्रास झाला?",
}

GAD7_ITEMS = {
    "en": [
        "Feeling nervous, anxious or on edge",
        "Not being able to stop or control worrying",
        "Worrying too much about different things",
        "Trouble relaxing",
        "Being so restless that it is hard to sit still",
        "Becoming easily annoyed or irritable",
        "Feeling afraid as if something awful might happen",
    ],
    "hi": [
        "बेचैनी, चिंता या तनाव महसूस करना",
        "चिंता रोकने या नियंत्रित कर सकने में असफल रहना",
        "विभिन्न चीज़ों के लिए बहुत ज्यादा चिंता करना",
        "आराम करने मे परेशानी",
        "इतनी ज्यादा बेचैनी, कि स्थिर बैठना मुश्किल हो जाता है",
        "आसानी से चिढ़ना या खिजना",
        "डर महसूस होना कि शायद कुछ बहुत बुरा हो सकता है",
    ],
    "mr": [
        "उदास, चिंताग्रस्त किंवा अतिशय ताणाखाली असणे",
        "काळजी करण्याचे थांबविण्यास वा त्यावर ताबा ठेवण्यास असमर्थ असणे",
        "निरनिराळ्या गोष्टींबाबत खूपच काळजी करणे",
        "आराम करण्यास त्रास होणे",
        "इतके अस्वस्थ होणे की एका जागेवर बसून राहणे कठीण व्हावे",
        "चटकन रागावणे किंवा चिडचिड करणे",
        "काहीतरी अतिशय वाईट घडले की काय अशी भीती वाटणे",
    ],
}

# -------------------- Other items --------------------
HEADACHE_DAYS_LABEL = {
    "en": "Number of headache days in the past month",
    "hi": "पिछले महीने में कितने दिन सिरदर्द हुआ",
    "mr": "मागील महिन्यात किती दिवस डोकेदुखी झाली",
}

UNDERSTANDING_LABEL = {
    "en": "How well do you feel you understand your migraine?",
    "hi": "आप अपने माइग्रेन को कितनी अच्छी तरह समझते हैं?",
    "mr": "तुम्हाला तुमचा मायग्रेन किती चांगल्या प्रकारे समजतो?",
}

# -------------------- MUCS --------------------
# Migraine Understanding & Confidence Scale — a 9-item agree/disagree
# instrument designed for this study. Three subscales:
#   - Understanding (items 1-3)
#   - Control / Self-efficacy (items 4-6)
#   - Fear / Reassurance (items 7-9, reverse-scored)
# Marathi wording is from the investigator (2026-06-18). English and Hindi
# are working drafts — please review before clinical use.

MUCS_PROMPT = {
    "en": "How much do you agree with this statement?",
    "hi": "आप इस कथन से कितना सहमत हैं?",
    "mr": "तुम्ही या विधानाशी किती सहमत आहात?",
}

# Section titles for the three subscales (shown above their items).
MUCS_SECTION_TITLES = {
    "en": ["Understanding", "Control / Self-efficacy", "Fear / Reassurance"],
    "hi": ["समझ", "नियंत्रण / आत्मविश्वास", "डर / आश्वासन"],
    "mr": ["समज", "नियंत्रण / आत्मविश्वास", "भीती / आश्वासन"],
}
# Which 0-indexed items belong to each section, in order.
MUCS_SECTION_BOUNDARIES = [(0, 3), (3, 6), (6, 9)]

# Items 7-9 (0-indexed 6-8) are reverse-scored — agreeing with these is
# the "worse" answer, so the raw value gets flipped at scoring time.
MUCS_REVERSE = {6, 7, 8}

MUCS_OPTIONS = {
    # Order: completely disagree → completely agree.
    "en": [
        "Strongly disagree",
        "Somewhat disagree",
        "Not sure / can't say",
        "Somewhat agree",
        "Strongly agree",
    ],
    "hi": [
        "पूरी तरह असहमत",
        "कुछ हद तक असहमत",
        "कह नहीं सकते / पता नहीं",
        "कुछ हद तक सहमत",
        "पूरी तरह सहमत",
    ],
    "mr": [
        "पूर्णपणे असहमत",
        "थोडेसे असहमत",
        "निश्चित नाही / सांगता येत नाही",
        "थोडेसे सहमत",
        "पूर्णपणे सहमत",
    ],
}
MUCS_VALUES = [1, 2, 3, 4, 5]

MUCS_ITEMS = {
    "en": [
        # Understanding — DRAFT translation, please review.
        'I know what "migraine" is.',
        "I know why my headaches happen.",
        "I know what I can do to reduce my headaches.",
        # Control / Self-efficacy — DRAFT translation, please review.
        "I know what to do when a headache starts.",
        "I feel confident I can handle a headache once it starts.",
        "I feel I have some degree of control over my migraines.",
        # Fear / Reassurance (reverse-scored) — DRAFT translation, please review.
        "I am afraid that a serious brain disease is behind my headaches.",
        "I am afraid of getting another headache.",
        "My headaches make me very anxious.",
    ],
    "hi": [
        # Understanding — DRAFT translation, please review.
        'मुझे पता है कि "माइग्रेन" क्या है।',
        "मुझे पता है कि मेरा सिरदर्द क्यों होता है।",
        "मुझे पता है कि सिरदर्द कम करने के लिए मैं क्या कर सकता हूँ।",
        # Control / Self-efficacy — DRAFT translation, please review.
        "सिरदर्द शुरू होने पर मुझे पता है कि क्या करना है।",
        "सिरदर्द शुरू होने पर उसे सँभालने का मुझे आत्मविश्वास है।",
        "मुझे लगता है कि मेरे माइग्रेन पर मेरा कुछ हद तक नियंत्रण है।",
        # Fear / Reassurance (reverse-scored) — DRAFT translation, please review.
        "मुझे डर है कि मेरे सिरदर्द के पीछे कोई गंभीर दिमागी बीमारी है।",
        "मुझे सिरदर्द होने का डर लगता है।",
        "मेरे सिरदर्द से मुझे बहुत चिंता होती है।",
    ],
    # Marathi wording from the investigator (2026-06-18).
    "mr": [
        # समज
        'मला "मायग्रेन" म्हणजे काय हे माहित आहे.',
        "मला माझी डोकेदुखी का होते हे माहित आहे.",
        "मला डोकेदुखी कमी करण्यासाठी काय करता येईल हे माहित आहे.",
        # नियंत्रण / आत्मविश्वास
        "डोकेदुखी सुरू झाल्यावर काय करावे हे मला माहित आहे.",
        "डोकेदुखी सुरू झाल्यावर ती हाताळण्याचा मला आत्मविश्वास आहे.",
        "मला माझ्या मायग्रेनवर काही प्रमाणात नियंत्रण असल्यासारखे वाटते.",
        # भीती / आश्वासन (reverse-scored)
        "माझ्या डोकेदुखीमागे गंभीर मेंदूचा आजार असण्याची भीती मला वाटते.",
        "मला डोकं दुखायची भीती वाटते.",
        "माझ्या डोकेदुखीमुळे मला खूप चिंता वाटते.",
    ],
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
    "patient_id_hint": {
        "en": "Use a study code (e.g. MIG-001) — do not enter the patient's name.",
        "hi": "अध्ययन कोड का उपयोग करें (जैसे MIG-001) — मरीज़ का नाम न लिखें।",
        "mr": "अभ्यास कोड वापरा (उदा. MIG-001) — रुग्णाचे नाव लिहू नका.",
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
    "mucs": {
        "en": "Now we are checking your understanding of migraine",
        "hi": "अब हम जाँच रहे हैं कि आप माइग्रेन के बारे में क्या समझते हैं",
        "mr": "आता आपण तपासत आहोत की तुम्हाला मायग्रेनबद्दल काय समजले आहे",
    },
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
    if name == "MUCS":
        return MUCS_ITEMS[lang_code], MUCS_OPTIONS[lang_code], MUCS_VALUES, "MUCS"
    raise ValueError(f"Unknown questionnaire: {name}")

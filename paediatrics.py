"""
paediatrics.py — Comprehensive Paediatric Nursing Reference
============================================================
Dedicated module for the Nursing Officer Exam Agent covering the full
breadth of paediatric nursing as tested in NORCET / SGPGI / ESIC / DSSSB.

Contents
--------
- FLASHCARDS          : 70+ atomic flashcards across 6 sub-topics
- MNEMONICS           : Paediatric-specific memory aids
- NCLEX_SCENARIOS     : Pre-built NCLEX-style priority questions
- IMMUNISATION_SCHEDULE : India's Universal Immunisation Programme (UIP)
- DOSAGE_REFERENCE    : Paediatric dosage calculation rules & examples
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Paediatric Flashcard Sets (sub-topic → list of (Front, Back) tuples)
# ---------------------------------------------------------------------------

FLASHCARDS: dict[str, list[tuple[str, str]]] = {

    # ── Vital Signs by Age ─────────────────────────────────────────────────
    "vital signs": [
        ("Neonatal heart rate (normal)", "120–160 bpm"),
        ("Infant heart rate (1–12 months)", "80–140 bpm"),
        ("Toddler heart rate (1–3 years)", "80–130 bpm"),
        ("Preschool heart rate (3–6 years)", "70–120 bpm"),
        ("School-age heart rate (6–12 years)", "60–100 bpm"),
        ("Neonatal respiratory rate", "40–60 breaths/min"),
        ("Infant respiratory rate", "30–53 breaths/min"),
        ("Toddler respiratory rate", "22–37 breaths/min"),
        ("Preschool respiratory rate", "20–28 breaths/min"),
        ("School-age respiratory rate", "18–25 breaths/min"),
        ("Normal BP — Newborn (systolic)", "60–90 mmHg"),
        ("Normal BP — 1 year (systolic)", "74–100 mmHg"),
        ("Normal BP — 6 years (systolic)", "84–120 mmHg"),
        ("Minimum systolic BP formula (children > 1 yr)", "70 + (2 × age in years) mmHg"),
        ("Normal neonatal temperature (axillary)", "36.5–37.5°C"),
        ("SpO₂ — acceptable in neonates", "≥ 95% after first 10 minutes of life"),
    ],

    # ── Growth & Development Milestones ───────────────────────────────────
    "growth and development": [
        ("Average birth weight", "2.5–3.5 kg (average 3 kg)"),
        ("Birth weight doubles at", "5 months"),
        ("Birth weight triples at", "1 year"),
        ("Birth weight quadruples at", "2 years"),
        ("Average birth length", "50 cm"),
        ("Birth length doubles at", "4 years"),
        ("Head circumference at birth", "34–36 cm"),
        ("Chest circumference at birth", "32–33 cm (2 cm less than head)"),
        ("Head = Chest circumference at", "6–9 months"),
        ("Anterior fontanelle closes at", "12–18 months"),
        ("Posterior fontanelle closes at", "6–8 weeks"),
        ("First tooth erupts at", "6 months"),
        ("All 20 deciduous teeth by", "2.5–3 years"),
        ("Child walks independently at", "12–15 months"),
        ("Child speaks 2-word sentences at", "2 years"),
        ("Denver Developmental Screening Test (DDST) — screens for", "Developmental delays in children 0–6 years"),
        ("Puberty onset — girls (average)", "8–13 years"),
        ("Puberty onset — boys (average)", "9–14 years"),
    ],

    # ── India's Universal Immunisation Programme (UIP) ────────────────────
    "immunisation": [
        ("BCG vaccine — given at", "Birth (within 24 hours)"),
        ("Hepatitis B (birth dose)", "Within 24 hours of birth"),
        ("OPV 0 — given at", "Birth"),
        ("OPV 1, 2, 3 — given at", "6, 10, 14 weeks"),
        ("DPT 1, 2, 3 — given at", "6, 10, 14 weeks"),
        ("Hib 1, 2, 3 — given at", "6, 10, 14 weeks"),
        ("Hepatitis B (3 doses) — given at", "6, 10, 14 weeks"),
        ("Rotavirus vaccine — given at", "6, 10, 14 weeks"),
        ("Pneumococcal (PCV) — given at", "6, 14 weeks & 9 months"),
        ("IPV (injectable polio) — given at", "6 & 14 weeks"),
        ("Measles / MR 1 — given at", "9 months"),
        ("Vitamin A 1st dose — given at", "9 months (with measles)"),
        ("JE vaccine (endemic areas) — given at", "9 months & 16–24 months"),
        ("DPT booster 1 + OPV booster — given at", "16–24 months"),
        ("MMR / MR 2 — given at", "15–18 months"),
        ("Typhoid conjugate vaccine (TCV)", "9–12 months"),
        ("DPT booster 2 — given at", "5–6 years"),
        ("Td booster — given at", "10 years & 16 years"),
        ("Cold-chain temperature for vaccines", "2–8°C (except OPV: −20°C)"),
        ("AEFI — full form", "Adverse Events Following Immunisation"),
    ],

    # ── Common Paediatric Conditions ──────────────────────────────────────
    "common conditions": [
        ("Febrile seizure — definition", "Seizure in child aged 6 months–5 years due to fever (> 38°C) with no CNS infection"),
        ("FIRST nursing action in febrile seizure", "Protect airway, place in lateral position, note seizure duration"),
        ("Intussusception — classic triad", "Sudden colicky pain · Currant-jelly stools · Sausage-shaped mass (RUQ)"),
        ("Croup — hallmark sign", "Barking (seal-like) cough + inspiratory stridor"),
        ("Croup — priority nursing position", "Upright / sitting position to ease breathing"),
        ("Epiglottitis — hallmark signs (4 D's)", "Dysphagia · Drooling · Dysphonia · Distress (tripod position)"),
        ("Hirschsprung's disease — key finding", "Absence of ganglion cells in colon → failure to pass meconium within 48 hours"),
        ("Pyloric stenosis — classic vomiting type", "Projectile (non-bilious) vomiting in first 2–8 weeks of life"),
        ("Kawasaki disease — 5 of 6 criteria (mnemonic CRASH)", "Conjunctivitis · Rash · Adenopathy (cervical) · Strawberry tongue · Hands/feet (desquamation) + Fever > 5 days"),
        ("Down syndrome — trisomy number", "Trisomy 21"),
        ("Nephrotic syndrome — hallmark", "Massive proteinuria · Hypoalbuminaemia · Oedema · Hyperlipidaemia"),
        ("Sickle cell crisis — priority intervention", "IV fluids + oxygen + analgesia"),
        ("Haemophilia A — deficient factor", "Factor VIII"),
        ("Haemophilia B — deficient factor", "Factor IX (Christmas disease)"),
        ("Meningitis — classic triad", "Fever · Neck stiffness (Kernig's / Brudzinski's sign) · Photophobia"),
        ("Reye syndrome — triggered by", "Aspirin use in viral illness (flu/chickenpox) → hepatic & cerebral encephalopathy"),
        ("Aspirin is CONTRAINDICATED in children under", "16 years (risk of Reye syndrome)"),
        ("RSV (Respiratory Syncytial Virus) — peak age", "< 2 years; prophylaxis: Palivizumab for high-risk infants"),
    ],

    # ── Nutrition & Malnutrition ───────────────────────────────────────────
    "nutrition": [
        ("Exclusive breastfeeding recommended for", "First 6 months of life (WHO/INC)"),
        ("Complementary feeding begins at", "6 months"),
        ("Breastfeeding recommended to continue until", "2 years and beyond"),
        ("Colostrum — key property", "Rich in IgA, protein, and antibodies; first milk in first 3–5 days"),
        ("MUAC — severe acute malnutrition (SAM)", "< 11.5 cm"),
        ("MUAC — moderate acute malnutrition (MAM)", "11.5–12.5 cm"),
        ("Marasmus — calorie/energy deficiency signs", "Severe wasting, 'old man' face, irritable, no oedema"),
        ("Kwashiorkor — protein deficiency signs", "Oedema · Pot belly · Moon face · Skin/hair changes · Lethargy"),
        ("Marasmic-kwashiorkor", "Combined severe wasting + oedema"),
        ("Vitamin A deficiency — ocular sign", "Bitot's spots → xerophthalmia → night blindness → corneal ulceration"),
        ("Vitamin D deficiency — paediatric condition", "Rickets (bowing of legs, rachitic rosary, craniotabes)"),
        ("Iron deficiency anaemia — most common age", "6 months–2 years; treatment: oral ferrous sulfate"),
        ("ORS — WHO low-osmolarity formula (Na⁺)", "75 mmol/L Na⁺, 20 mmol/L K⁺, 75 mmol/L glucose, 245 mOsm/L"),
        ("IMNCI — full form", "Integrated Management of Neonatal and Childhood Illness"),
    ],

    # ── Neonatal Nursing ───────────────────────────────────────────────────
    "neonatal": [
        ("APGAR score — assessed at", "1 minute and 5 minutes after birth"),
        ("APGAR 7–10", "Normal — no intervention needed"),
        ("APGAR 4–6", "Moderate distress — stimulate, oxygen"),
        ("APGAR 0–3", "Severe distress — immediate resuscitation"),
        ("Normal meconium passage — within", "24–48 hours of birth"),
        ("Physiological jaundice — appears at", "2nd–3rd day; resolves by 7–10 days (term)"),
        ("Pathological jaundice — appears within", "24 hours of birth"),
        ("Phototherapy — used for", "Hyperbilirubinaemia (jaundice) in neonates"),
        ("Exchange transfusion — indication in neonate", "Bilirubin > 20 mg/dL or rising rapidly"),
        ("Neonatal hypoglycaemia — blood glucose threshold", "< 40 mg/dL (< 2.2 mmol/L)"),
        ("Kangaroo Mother Care (KMC) — benefit", "Skin-to-skin contact for LBW/preterm; maintains temperature, promotes breastfeeding"),
        ("LBW (low birth weight) — defined as", "< 2.5 kg at birth regardless of gestational age"),
        ("VLBW — very low birth weight", "< 1.5 kg"),
        ("ELBW — extremely low birth weight", "< 1.0 kg"),
        ("RDS (Respiratory Distress Syndrome) — cause in preterm", "Surfactant deficiency; treatment: exogenous surfactant + CPAP"),
        ("NEC (Necrotising Enterocolitis) — earliest sign", "Abdominal distension + blood in stool in preterm neonate"),
    ],
}

# Flat list merging all sub-topics (used by agent.py for the top-level
# "paediatrics" flashcard set — replaces the old 10-card list)
ALL_FLASHCARDS: list[tuple[str, str]] = [
    card for cards in FLASHCARDS.values() for card in cards
]


# ---------------------------------------------------------------------------
# Paediatric-Specific Mnemonics
# ---------------------------------------------------------------------------

MNEMONICS: dict[str, tuple[str, str]] = {
    "apgar score": (
        "APGAR",
        "Appearance (skin colour) · Pulse (heart rate) · Grimace (reflex irritability) "
        "· Activity (muscle tone) · Respiration",
    ),
    "kawasaki disease": (
        "CRASH + Fever",
        "Conjunctivitis · Rash (polymorphous) · Adenopathy (cervical, non-suppurative) "
        "· Strawberry tongue · Hands/Feet (erythema, desquamation) + Fever > 5 days",
    ),
    "dehydration signs in children": (
        "DEHYDRATED",
        "Decreased urine output · Eyes sunken · Heart rate elevated · "
        "Years (age <5 most vulnerable) · Dry mucous membranes · Reduced skin turgor · "
        "Anterior fontanelle sunken · Tearless cry · Extreme thirst · Drowsiness/lethargy",
    ),
    "febrile seizure management": (
        "PLACE",
        "Position (lateral/recovery) · Loosen clothing · Airway patency · "
        "Calm environment · Ensure time/duration noted",
    ),
    "meningitis signs": (
        "FNKS",
        "Fever · Neck stiffness · Kernig's sign · "
        "(Brudzinski's sign implicit) — PLUS photophobia & petechial rash (meningococcal)",
    ),
    "rickets signs": (
        "RICKETS",
        "Rachitic rosary · Irregular (bowed) legs · Craniotabes · "
        "Knock-knees · Epiphyseal enlargement · Tetany (hypocalcaemia) · Skull (frontal bossing)",
    ),
    "nephrotic syndrome": (
        "PHONE",
        "Proteinuria (massive) · Hypoalbuminaemia · Oedema · "
        "Normal blood pressure (usually) · Elevated lipids (hyperlipidaemia)",
    ),
    "epiglottitis 4Ds": (
        "4 D's",
        "Dysphagia · Drooling · Dysphonia · Distress (tripod/sniffing position)",
    ),
    "neonatal resuscitation steps": (
        "ABCD",
        "Airway (position, suction) · Breathing (stimulate, PPV if needed) "
        "· Circulation (chest compressions if HR < 60) · Drugs (epinephrine if no response)",
    ),
    "kwashiorkor vs marasmus": (
        "KM",
        "Kwashiorkor = protein deficiency → oedema, moon face, pot belly, normal weight illusion\n"
        "Marasmus = calorie deficiency → severe wasting, NO oedema, 'old man' face, irritable",
    ),
}


# ---------------------------------------------------------------------------
# NCLEX-Style Paediatric Priority Scenarios
# ---------------------------------------------------------------------------

NCLEX_SCENARIOS: list[dict] = [
    {
        "id": 1,
        "topic": "Febrile Seizure",
        "scenario": (
            "A 2-year-old child is brought to the emergency department. "
            "The mother states the child had a sudden jerking of all four limbs "
            "lasting about 90 seconds. Temperature is 39.2°C. The child is now "
            "post-ictal and breathing regularly. No prior seizure history."
        ),
        "question": "What is the FIRST nursing action?",
        "priority_answer": (
            "Place the child in the **lateral (recovery) position** to protect the airway "
            "and prevent aspiration."
        ),
        "rationale": (
            "ABC framework: Airway is the priority. The post-ictal child may have "
            "decreased tone and risk of aspiration. After airway is secured: "
            "loosen clothing, ensure safety, record seizure duration, "
            "administer antipyretic as ordered, and prepare for investigations "
            "(blood glucose, electrolytes, LP if indicated)."
        ),
        "framework": "ABC → Airway first",
    },
    {
        "id": 2,
        "topic": "Croup (Laryngotracheobronchitis)",
        "scenario": (
            "A 3-year-old presents at 2 AM with a barking cough, inspiratory stridor at rest, "
            "and mild intercostal retractions. SpO₂ is 94% on room air. "
            "The child is agitated but consolable."
        ),
        "question": "Which intervention is the highest priority?",
        "priority_answer": (
            "Administer **nebulised epinephrine (adrenaline)** and **dexamethasone** as ordered; "
            "keep the child upright and calm — agitation worsens stridor."
        ),
        "rationale": (
            "Stridor at rest with SpO₂ 94% indicates moderate-severe croup. "
            "Maintain upright positioning, minimise distress, give cool humidified oxygen. "
            "Nebulised epinephrine reduces oedema rapidly (monitor for rebound after 2–3 hours). "
            "Dexamethasone reduces airway inflammation. Prepare for intubation if worsening."
        ),
        "framework": "ABC → Breathing; Severity assessment",
    },
    {
        "id": 3,
        "topic": "Dehydration — ORS Administration",
        "scenario": (
            "A 10-month-old is brought in with 3-day history of vomiting and loose stools. "
            "The infant has sunken eyes, dry mucous membranes, reduced skin turgor, "
            "and has not urinated in 8 hours. Weight today is 7.5 kg vs. 8 kg one week ago."
        ),
        "question": "What is the FIRST priority nursing action?",
        "priority_answer": (
            "Assess the degree of dehydration using WHO criteria, then initiate **oral "
            "rehydration therapy (ORS)** at 75 mL/kg over 4 hours (moderate dehydration), "
            "or IV fluids if the child cannot tolerate oral intake."
        ),
        "rationale": (
            "Weight loss of 500 g = ~6% dehydration = moderate. "
            "WHO ORS (75 mmol/L Na⁺) is the first-line treatment. "
            "Monitor urine output, skin turgor, and weight every hour. "
            "If vomiting prevents oral intake → nasogastric tube or IV line (Normal Saline 20 mL/kg bolus)."
        ),
        "framework": "Maslow: Physiological needs; IMNCI dehydration classification",
    },
    {
        "id": 4,
        "topic": "Neonatal Jaundice — Phototherapy",
        "scenario": (
            "A 2-day-old term neonate has visible jaundice extending to the chest. "
            "Serum bilirubin is 14 mg/dL. The neonate is breastfeeding adequately "
            "and appears alert. Mother's blood group is O+ve, baby is A+ve."
        ),
        "question": "What is the PRIORITY nursing intervention?",
        "priority_answer": (
            "Initiate **phototherapy** as ordered; cover eyes with opaque shield, "
            "expose maximum skin surface, and ensure adequate hydration/breastfeeding."
        ),
        "rationale": (
            "Bilirubin 14 mg/dL on day 2 in a term neonate crosses the phototherapy threshold "
            "(per AAP/NNF guidelines). Eye shields prevent retinal damage from the light. "
            "Turn the baby every 2 hours to maximise exposure. Monitor bilirubin every "
            "4–6 hours. Watch for: loose green stools (normal), rash (transient), "
            "hyperthermia. Blood group incompatibility (ABO) is likely cause here."
        ),
        "framework": "ABC + Nursing Process (ADPIE)",
    },
    {
        "id": 5,
        "topic": "Epiglottitis",
        "scenario": (
            "A 4-year-old is brought in with sudden-onset high fever (39.8°C), "
            "drooling, difficulty swallowing, muffled voice, and is sitting leaning "
            "forward with chin thrust out (tripod position). Stridor is audible."
        ),
        "question": "What is the MOST IMPORTANT nursing action?",
        "priority_answer": (
            "Do **NOT** examine the throat or place anything in the mouth. "
            "Keep the child calm and upright. Call the physician and anaesthetist "
            "IMMEDIATELY — prepare for emergency airway management."
        ),
        "rationale": (
            "Epiglottitis is a life-threatening emergency. Any instrument in the mouth "
            "can cause complete airway obstruction (laryngospasm). "
            "The child self-positions to maximise airway diameter. "
            "Interventions in priority order: keep calm → call for help → prepare for intubation "
            "→ administer IV antibiotics (ceftriaxone) after airway secured → blood cultures."
        ),
        "framework": "ABC → Airway = highest priority",
    },
    {
        "id": 6,
        "topic": "Intussusception",
        "scenario": (
            "A 9-month-old infant presents with episodic inconsolable crying and "
            "drawing up of legs. Between episodes, the baby appears pale and lethargic. "
            "The mother reports the stool looked 'like red jelly' this morning."
        ),
        "question": "Which finding requires IMMEDIATE intervention?",
        "priority_answer": (
            "**Currant-jelly (red-jelly) stools** indicate intestinal ischaemia/mucosal sloughing — "
            "this is a surgical emergency. Establish IV access, keep nil-by-mouth, "
            "and prepare for air/hydrostatic enema or surgical reduction."
        ),
        "rationale": (
            "Classic triad: colicky pain + currant-jelly stools + palpable sausage-shaped mass. "
            "Currant-jelly stool = blood + mucus = bowel necrosis risk. "
            "Non-operative: air or hydrostatic (saline) enema under fluoroscopy (80–90% success). "
            "Surgical reduction if enema fails or perforation suspected."
        ),
        "framework": "Maslow (Safety) + ABC (Circulation compromised)",
    },
    {
        "id": 7,
        "topic": "Meningococcal Meningitis",
        "scenario": (
            "A 7-year-old is brought in with fever (40°C), severe headache, stiff neck, "
            "and a non-blanching petechial rash spreading on the legs and trunk. "
            "The child is confused and photophobic."
        ),
        "question": "What is the FIRST nursing action?",
        "priority_answer": (
            "Activate the emergency response, initiate **contact/droplet isolation**, "
            "and prepare for immediate IV antibiotics (benzylpenicillin / ceftriaxone) "
            "— do not delay for LP if the child is deteriorating."
        ),
        "rationale": (
            "Non-blanching petechial rash = meningococcaemia until proven otherwise. "
            "This is a medical emergency with risk of septicaemic shock. "
            "Priority: ABC, IV access, blood cultures (before antibiotics if possible but "
            "do NOT delay antibiotics for LP). Isolate immediately (droplet precautions). "
            "Monitor for: Waterhouse–Friderichsen syndrome (adrenal haemorrhage), DIC, shock."
        ),
        "framework": "ABC + Infection control + Emergency escalation",
    },
    {
        "id": 8,
        "topic": "Nephrotic Syndrome — Oedema Management",
        "scenario": (
            "A 5-year-old is admitted with generalised pitting oedema, ascites, "
            "and periorbital oedema worse in the mornings. Urinalysis shows 4+ proteinuria. "
            "Serum albumin is 1.8 g/dL. The child is on oral prednisolone."
        ),
        "question": "Which nursing intervention is the PRIORITY?",
        "priority_answer": (
            "Monitor **fluid intake/output strictly**, daily weights at the same time each morning, "
            "and assess for signs of infection (major cause of death in nephrotic syndrome)."
        ),
        "rationale": (
            "Low albumin → reduced oncotic pressure → oedema. The child is immunocompromised "
            "due to protein loss and steroids. Priority assessments: I&O, daily weight, "
            "BP (watch for hypovolaemia), urine protein dipstick, signs of peritonitis/cellulitis. "
            "Dietary advice: low-sodium, normal protein. Restrict fluids only if severe oedema. "
            "Diuretics (furosemide) only if hypovolaemia is excluded."
        ),
        "framework": "ADPIE + Safety (infection risk)",
    },
]


# ---------------------------------------------------------------------------
# Paediatric Dosage Reference
# ---------------------------------------------------------------------------

DOSAGE_REFERENCE: list[dict] = [
    {
        "drug": "Paracetamol (Acetaminophen)",
        "dose": "10–15 mg/kg/dose every 4–6 hours",
        "route": "Oral / Rectal",
        "max_daily": "60 mg/kg/day or 4 g/day (whichever is less)",
        "note": "Safe in children; avoid in hepatic impairment",
    },
    {
        "drug": "Ibuprofen",
        "dose": "5–10 mg/kg/dose every 6–8 hours",
        "route": "Oral",
        "max_daily": "40 mg/kg/day",
        "note": "≥ 6 months only; avoid in renal impairment, dehydration, bleeding risk",
    },
    {
        "drug": "Oral Rehydration Solution (ORS)",
        "dose": "Mild dehydration: 50 mL/kg over 4 hours; Moderate: 75 mL/kg over 4 hours",
        "route": "Oral / Nasogastric",
        "max_daily": "As needed to replace ongoing losses",
        "note": "WHO low-osmolarity ORS: 75 mmol/L Na⁺",
    },
    {
        "drug": "Diazepam (IV — for seizures)",
        "dose": "0.1–0.3 mg/kg/dose (max 10 mg per dose)",
        "route": "IV (slow push over 2–3 minutes)",
        "max_daily": "Repeat once after 10 minutes if seizure persists",
        "note": "Watch for respiratory depression; have resuscitation equipment ready",
    },
    {
        "drug": "Adrenaline/Epinephrine (anaphylaxis)",
        "dose": "0.01 mg/kg (1:1000 solution) = 0.01 mL/kg IM",
        "route": "Intramuscular (anterolateral thigh)",
        "max_daily": "0.5 mg per dose; repeat every 5–15 minutes if needed",
        "note": "No absolute contraindication in anaphylaxis",
    },
    {
        "drug": "Ceftriaxone (meningitis)",
        "dose": "100 mg/kg/day IV in 1–2 divided doses",
        "route": "IV / IM",
        "max_daily": "4 g/day",
        "note": "Avoid in neonates < 4 weeks (displaces bilirubin); avoid with calcium-containing IV fluids",
    },
    {
        "drug": "Prednisolone (nephrotic syndrome)",
        "dose": "2 mg/kg/day (max 60 mg/day) for 4–6 weeks, then taper",
        "route": "Oral",
        "max_daily": "60 mg/day",
        "note": "Monitor BP, glucose, weight, infection signs; give with food",
    },
    {
        "drug": "Iron (ferrous sulfate — IDA treatment)",
        "dose": "3–6 mg/kg/day of elemental iron in 2–3 divided doses",
        "route": "Oral",
        "max_daily": "Per body weight calculation",
        "note": "Give between meals for better absorption; darkens stool (counsel parents)",
    },
]


# ---------------------------------------------------------------------------
# Immunisation Schedule (India UIP — 2024)
# ---------------------------------------------------------------------------

IMMUNISATION_SCHEDULE: list[dict] = [
    {"age": "Birth",        "vaccines": "BCG · OPV 0 · Hepatitis B (birth dose)"},
    {"age": "6 weeks",      "vaccines": "OPV 1 · DPT 1 · Hib 1 · Hepatitis B 2 · IPV 1 · Rotavirus 1 · PCV 1"},
    {"age": "10 weeks",     "vaccines": "OPV 2 · DPT 2 · Hib 2 · Hepatitis B 3 · Rotavirus 2 · PCV 2"},
    {"age": "14 weeks",     "vaccines": "OPV 3 · DPT 3 · Hib 3 · IPV 2 · Rotavirus 3 · PCV 3"},
    {"age": "9 months",     "vaccines": "MR/Measles 1 · Vitamin A (1st dose) · JE 1 (endemic areas)"},
    {"age": "12 months",    "vaccines": "Hepatitis A (1st dose, if included in state programme)"},
    {"age": "15–18 months", "vaccines": "DPT booster 1 · OPV booster · Hib booster · MMR · PCV booster · Varicella 1"},
    {"age": "16–24 months", "vaccines": "MR 2 · Vitamin A (2nd dose) · JE 2 (endemic areas)"},
    {"age": "5–6 years",    "vaccines": "DPT booster 2"},
    {"age": "10 years",     "vaccines": "Td · HPV (girls, 2 doses 6 months apart)"},
    {"age": "16 years",     "vaccines": "Td"},
]


# ---------------------------------------------------------------------------
# Helper: format a single NCLEX scenario for display
# ---------------------------------------------------------------------------

def format_scenario(scenario: dict) -> str:
    """Return a formatted string for one NCLEX paediatric scenario."""
    lines = [
        f"**NCLEX Paediatric Priority — Scenario {scenario['id']}: {scenario['topic']}**\n",
        f"Scenario:\n{scenario['scenario']}\n",
        f"❓ {scenario['question']}\n",
        f"✅ Priority Answer:\n{scenario['priority_answer']}\n",
        f"📖 Rationale:\n{scenario['rationale']}\n",
        f"🔑 Framework: {scenario['framework']}",
    ]
    return "\n".join(lines)


def format_dosage_table() -> str:
    """Return a formatted dosage reference table."""
    header = "**Paediatric Dosage Quick Reference**\n"
    rows = []
    for d in DOSAGE_REFERENCE:
        rows.append(
            f"• **{d['drug']}** — {d['dose']} ({d['route']})\n"
            f"  Max: {d['max_daily']} | Note: {d['note']}"
        )
    return header + "\n".join(rows)


def format_immunisation_schedule() -> str:
    """Return a formatted immunisation schedule."""
    header = "**India UIP Immunisation Schedule (2024)**\n"
    rows = [f"{row['age']:20s} | {row['vaccines']}" for row in IMMUNISATION_SCHEDULE]
    return header + "\n".join(rows)

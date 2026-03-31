"""
Nursing Officer Exam Agent
==========================
An ADHD-friendly tutoring agent for Indian Nursing Officer Exams
(NORCET, SGPGI, ESIC, DSSSB).

Features
--------
- Atomic Flashcard generation  (Front | Back format)
- NCLEX-style priority questions
- Mnemonic suggestions for complex topics
- Quick-reference nursing values
- CCS Conduct Rule references for administrative queries

Usage
-----
    python agent.py                  # interactive CLI
    python agent.py --demo           # run a built-in demo
"""

from __future__ import annotations

import argparse
import re
import textwrap
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------------
# Agent system prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT_PATH = Path(__file__).parent / "system_prompt.md"

def load_system_prompt() -> str:
    """Return the agent system prompt from system_prompt.md."""
    if SYSTEM_PROMPT_PATH.exists():
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    return ""


# ---------------------------------------------------------------------------
# Built-in knowledge base (used when no LLM backend is connected)
# ---------------------------------------------------------------------------

FLASHCARD_SETS: dict[str, list[tuple[str, str]]] = {
    "electrolytes": [
        ("Normal serum Na⁺", "135–145 mEq/L"),
        ("Normal serum K⁺", "3.5–5.0 mEq/L"),
        ("Normal serum Ca²⁺", "8.5–10.5 mg/dL"),
        ("Normal serum Mg²⁺", "1.5–2.5 mEq/L"),
        ("First sign of hypokalemia", "Muscle weakness"),
        ("ECG change in hyperkalemia", "Peaked (tall) T-waves"),
        ("Chvostek's sign indicates", "Hypocalcemia"),
        ("Trousseau's sign indicates", "Hypocalcemia"),
        ("Hyponatremia symptom (severe)", "Seizures / coma"),
        ("Treatment of hyperkalemia (emergency)", "IV Calcium gluconate (cardiac protection)"),
    ],
    "pharmacology": [
        ("Antidote for Heparin", "Protamine sulfate"),
        ("Antidote for Warfarin", "Vitamin K (phytomenadione)"),
        ("Antidote for Paracetamol / Acetaminophen", "N-acetylcysteine (NAC)"),
        ("Antidote for Opioid overdose", "Naloxone"),
        ("Antidote for Benzodiazepines", "Flumazenil"),
        ("Antidote for Organophosphate poisoning", "Atropine + Pralidoxime"),
        ("Antidote for Iron overdose", "Deferoxamine"),
        ("Antidote for Cyanide poisoning", "Hydroxocobalamin (or Sodium thiosulfate)"),
        ("Antidote for Digoxin toxicity", "Digibind (Digoxin-specific antibody fragments)"),
        ("Antidote for Magnesium sulfate toxicity", "Calcium gluconate"),
    ],
    "fundamentals": [
        ("Normal adult respiratory rate", "12–20 breaths/min"),
        ("Normal adult pulse rate", "60–100 bpm"),
        ("Normal adult BP", "120/80 mmHg"),
        ("Normal adult temperature (oral)", "37°C (98.6°F)"),
        ("SpO₂ normal range", "95–100%"),
        ("GCS — Normal score", "15"),
        ("APGAR score — Reassuring range", "7–10"),
        ("APGAR score — Moderate distress", "4–6"),
        ("5 Rights of medication administration", "Right patient, drug, dose, route, time"),
        ("Universal blood donor group", "O negative (O−)"),
    ],
    "obstetrics": [
        ("Normal duration of 1st stage of labour (primigravida)", "≤ 20 hours"),
        ("Normal duration of 2nd stage of labour", "Up to 2 hours (primigravida)"),
        ("Normal duration of 3rd stage of labour", "Up to 30 minutes"),
        ("Presenting part in normal delivery", "Vertex (occiput anterior)"),
        ("APGAR — assessed at", "1 minute and 5 minutes after birth"),
        ("Lochia rubra — duration", "First 3 days post-partum"),
        ("Lochia serosa — duration", "Days 4–9 post-partum"),
        ("Lochia alba — duration", "Day 10 until ~6 weeks"),
        ("Nagele's rule — EDD calculation", "LMP + 9 months + 7 days"),
        ("Maternal mortality rate (India target, NHM)", "< 70/100,000 live births"),
    ],
    "paediatrics": [
        ("Immunisation — BCG given at", "Birth"),
        ("Immunisation — OPV 0 given at", "Birth"),
        ("DPT 1 given at", "6 weeks"),
        ("MMR given at", "9 months & 15 months"),
        ("Birth weight doubles by", "5 months"),
        ("Birth weight triples by", "1 year"),
        ("Normal neonatal respiratory rate", "40–60 breaths/min"),
        ("Anterior fontanelle closes at", "12–18 months"),
        ("MUAC (moderate acute malnutrition)", "11.5–12.5 cm"),
        ("WHO oral rehydration solution (ORS) — Na⁺ content", "75 mmol/L"),
    ],
}

MNEMONICS: dict[str, tuple[str, str]] = {
    "pulmonary edema": (
        "LMNOP",
        "Lasix (furosemide) · Morphine · Nitrates · Oxygen · Position (sit upright)",
    ),
    "heart failure": (
        "FACES",
        "Fatigue · Activity limitation · Chest congestion/cough · Edema (ankle) · Shortness of breath",
    ),
    "hypokalemia signs": (
        "6 L's",
        "Lethargy · Leg cramps · Low/shallow respirations · Limp muscles · Low BP · Lethal dysrhythmias",
    ),
    "hyperkalemia signs": (
        "MURDER",
        "Muscle weakness · Urine (oliguria) · Respiratory distress · Decreased cardiac contractility · ECG changes · Reflexes (decreased)",
    ),
    "cushing's triad": (
        "IHB",
        "Increased BP (widened pulse pressure) · Heart rate decreased (bradycardia) · Breathing irregularity",
    ),
    "cranial nerves": (
        "On Old Olympus Towering Tops A Finn And German Viewed Some Hops",
        "Olfactory · Optic · Oculomotor · Trochlear · Trigeminal · Abducens · Facial · Auditory/Vestibulocochlear · Glossopharyngeal · Vagus · Spinal Accessory · Hypoglossal",
    ),
    "apgar score": (
        "APGAR",
        "Appearance (colour) · Pulse (HR) · Grimace (reflex) · Activity (muscle tone) · Respiration",
    ),
    "myocardial infarction signs": (
        "PULSE",
        "Pressure / Pain (chest) · Upset stomach (nausea) · Light-headedness · Sweat (diaphoresis) · Extreme fatigue",
    ),
}

CCS_RULES: dict[int, str] = {
    3: "General conduct — Every Government servant shall at all times maintain absolute integrity and devotion to duty.",
    7: "Prohibition on taking part in politics and elections.",
    11: "Prohibition of dowry — No Government servant shall give or take dowry.",
    15: "Restriction on communication of official information.",
    19: "Vindication of acts and character of Government servants.",
    20: "Canvassing of non-official or other outside influence.",
    22: "Bigamous marriages prohibited.",
}

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _match_key(query: str, keys: Iterable[str]) -> "str | None":
    """
    Return the best-matching key from *keys* for *query* using a
    tiered strategy: exact → prefix → whole-word substring.
    Returns *None* when no match is found.
    """
    q = query.lower().strip()

    # 1. Exact match
    for k in keys:
        if q == k:
            return k

    # 2. Prefix match (query starts the key, e.g. "electro" → "electrolytes")
    for k in keys:
        if k.startswith(q):
            return k

    # 3. Whole-word substring (avoids 'ric' matching 'obstetrics')
    pattern = re.compile(r"\b" + re.escape(q) + r"\b")
    for k in keys:
        if pattern.search(k):
            return k

    return None


# ---------------------------------------------------------------------------
# Core agent functions
# ---------------------------------------------------------------------------

def generate_flashcards(topic: str) -> str:
    """Return atomic flashcards for a given topic key."""
    matched_key = _match_key(topic, FLASHCARD_SETS.keys())
    if matched_key is None:
        available = ", ".join(FLASHCARD_SETS.keys())
        return f"Topic '{topic}' not found. Available sets: {available}"

    lines = [f"**Flashcards — {matched_key.title()}**\n"]
    for front, back in FLASHCARD_SETS[matched_key]:
        lines.append(f"{front} | {back}")
    return "\n".join(lines)


def get_mnemonic(topic: str) -> str:
    """Return the mnemonic for a given topic."""
    matched_key = _match_key(topic, MNEMONICS.keys())
    if matched_key is None:
        available = ", ".join(MNEMONICS.keys())
        return f"No mnemonic found for '{topic}'. Available: {available}"
    acronym, expansion = MNEMONICS[matched_key]
    return f"**Mnemonic:** {acronym}\n{expansion}"


def ccs_rule(rule_number: int) -> str:
    """Return a CCS Conduct Rule description by number."""
    if rule_number in CCS_RULES:
        return f"**CCS Rule {rule_number}:** {CCS_RULES[rule_number]}"
    available = ", ".join(str(r) for r in CCS_RULES)
    return f"Rule {rule_number} not indexed. Available rules: {available}"


def priority_question(scenario: str) -> str:
    """
    Return an NCLEX-style priority question scaffold.
    In a real deployment this would call an LLM; here we return a template.
    """
    return textwrap.dedent(f"""
    **NCLEX-Style Priority Question**

    Scenario: {scenario}

    Question: What is the FIRST nursing action?

    Use the **ABC framework** (Airway → Breathing → Circulation) and
    **Maslow's Hierarchy** to identify the highest-priority need.
    Apply the **Nursing Process (ADPIE)**:
      A — Assess first before intervening.
      D — Diagnose the priority problem.
      P — Plan the intervention.
      I — Implement.
      E — Evaluate.

    *(Connect an LLM backend via `NursingAgent` to get a fully worked answer.)*
    """).strip()


# ---------------------------------------------------------------------------
# High-level agent class
# ---------------------------------------------------------------------------

class NursingAgent:
    """
    Nursing Officer Exam Agent.

    This class wraps the built-in knowledge base and, if an LLM client
    is supplied, delegates open-ended questions to it with the system prompt.
    """

    def __init__(self, llm_client=None) -> None:
        """
        Parameters
        ----------
        llm_client : optional
            Any object with a ``chat(system, user) -> str`` interface.
            When *None* the agent operates in offline / demo mode.
        """
        self._llm = llm_client
        self._system_prompt = load_system_prompt()

    @property
    def system_prompt(self) -> str:
        """Return the agent system prompt string."""
        return self._system_prompt

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def flashcards(self, topic: str) -> str:
        """Return atomic flashcards for *topic*."""
        return generate_flashcards(topic)

    def mnemonic(self, topic: str) -> str:
        """Return a mnemonic for *topic*."""
        return get_mnemonic(topic)

    def ccs_rule(self, rule_number: int) -> str:
        """Return a CCS Conduct Rule description."""
        return ccs_rule(rule_number)

    def priority_question(self, scenario: str) -> str:
        """Generate an NCLEX-style priority question for *scenario*."""
        return priority_question(scenario)

    def ask(self, question: str) -> str:
        """
        Answer an open-ended question.

        Uses the LLM client when available; falls back to built-in helpers
        by detecting keywords in the question.
        """
        if self._llm is not None:
            return self._llm.chat(system=self._system_prompt, user=question)

        q = question.lower()

        # Keyword routing
        if any(kw in q for kw in ("flashcard", "card", "cards")):
            for topic in FLASHCARD_SETS:
                if topic in q:
                    return self.flashcards(topic)
            return self.flashcards("fundamentals")

        if "mnemonic" in q:
            for topic in MNEMONICS:
                if topic in q:
                    return self.mnemonic(topic)
            return self.mnemonic("pulmonary edema")

        if "ccs" in q or "conduct rule" in q:
            for num in CCS_RULES:
                if str(num) in q:
                    return self.ccs_rule(num)
            return self.ccs_rule(3)

        if "priority" in q or "first action" in q or "nclex" in q:
            return self.priority_question(question)

        return (
            "**Tip:** I'm running in offline mode.\n"
            "Connect an LLM client for full Q&A support.\n\n"
            "Try commands: `flashcards electrolytes`, `mnemonic pulmonary edema`, "
            "`ccs rule 3`, or `priority <scenario>`."
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _demo(agent: NursingAgent) -> None:
    """Print a representative demo of agent capabilities."""
    separator = "\n" + "─" * 60 + "\n"

    print(separator)
    print("DEMO 1 — Electrolyte Flashcards")
    print(separator)
    print(agent.flashcards("electrolytes"))

    print(separator)
    print("DEMO 2 — Pharmacology Flashcards (Antidotes)")
    print(separator)
    print(agent.flashcards("pharmacology"))

    print(separator)
    print("DEMO 3 — Mnemonic for Pulmonary Edema")
    print(separator)
    print(agent.mnemonic("pulmonary edema"))

    print(separator)
    print("DEMO 4 — NCLEX Priority Question")
    print(separator)
    print(agent.priority_question(
        "A post-operative patient suddenly becomes restless, "
        "with SpO₂ dropping to 88% and RR of 28/min."
    ))

    print(separator)
    print("DEMO 5 — CCS Conduct Rule 3")
    print(separator)
    print(agent.ccs_rule(3))
    print(separator)


def _interactive(agent: NursingAgent) -> None:
    """Run an interactive CLI session."""
    print("Nursing Officer Exam Agent — Interactive Mode")
    print("Type 'help' for commands or 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break
        if user_input.lower() == "help":
            print(textwrap.dedent("""
            Commands:
              flashcards <topic>       — generate atomic flashcards
              mnemonic <topic>         — get a mnemonic
              ccs rule <number>        — look up a CCS Conduct Rule
              priority <scenario>      — NCLEX-style priority question
              <any question>           — open-ended Q&A (requires LLM)

            Topics for flashcards: electrolytes, pharmacology, fundamentals, obstetrics, paediatrics
            Topics for mnemonics: pulmonary edema, heart failure, hypokalemia signs,
                                  hyperkalemia signs, cushing's triad, cranial nerves,
                                  apgar score, myocardial infarction signs
            """))
            continue

        print(f"\n{agent.ask(user_input)}\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Nursing Officer Exam Agent CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run a built-in demonstration of agent capabilities",
    )
    args = parser.parse_args()

    agent = NursingAgent()

    if args.demo:
        _demo(agent)
    else:
        _interactive(agent)


if __name__ == "__main__":
    main()

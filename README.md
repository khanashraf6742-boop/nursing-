# Nursing Officer Exam Agent

An **ADHD-friendly AI tutoring agent** for Indian Nursing Officer Exams:
**NORCET · SGPGI · ESIC · DSSSB**

Follows the latest **INC (Indian Nursing Council)** guidelines and standard
textbooks (Brunner & Suddarth, Saunders).

---

## Features

| Feature | Description |
|---|---|
| **Atomic Flashcards** | `Front \| Back` format; one fact per card |
| **NCLEX-Style Questions** | Priority nursing actions with ABC / ADPIE scaffolding |
| **Mnemonic Generator** | Memorable acronyms for complex drug classes & symptoms |
| **CCS Rule Reference** | Central Civil Services Conduct Rules for government staff |
| **Offline Mode** | Full knowledge base — no internet required |
| **LLM-Ready** | Plug in any LLM client for open-ended Q&A |

---

## Quick Start

```bash
# Run the built-in demo
python agent.py --demo

# Start an interactive session
python agent.py
```

### Interactive Commands

```
flashcards electrolytes        → 10 electrolyte value cards
flashcards pharmacology        → antidote quick-reference cards
flashcards fundamentals        → vital signs & nursing basics
flashcards obstetrics          → labour stages, lochia, EDD
flashcards paediatrics         → immunisation schedule, milestones

mnemonic pulmonary edema       → LMNOP
mnemonic hyperkalemia signs    → MURDER
mnemonic apgar score           → APGAR expansion

ccs rule 3                     → General Conduct
ccs rule 11                    → Prohibition of Dowry

priority <scenario>            → NCLEX-style priority question
```

---

## Priority Topics Covered

- **Fundamentals of Nursing & First Aid** — Vital signs, aseptic technique, wound care, CPR, triage
- **Medical-Surgical Nursing** — Electrolyte imbalances (Na⁺, K⁺, Ca²⁺, Mg²⁺), fluid balance, post-op care
- **Pharmacology** — Dosage calculations, antidotes, drug classifications, side-effect profiles
- **Anatomy & Physiology** — Organ systems, physiological values, reflex arcs
- **Obstetrics & Paediatric Nursing** — Stages of labour, APGAR score, growth milestones, immunisation schedules

---

## Connecting an LLM Backend

```python
from agent import NursingAgent

class MyLLM:
    def chat(self, system: str, user: str) -> str:
        # Call your preferred LLM API here
        ...

agent = NursingAgent(llm_client=MyLLM())
print(agent.ask("Explain the pathophysiology of hypokalemia"))
```

The full system prompt is stored in [`system_prompt.md`](system_prompt.md)
and automatically passed to your LLM as the `system` message.

---

## GitHub Copilot Integration

Agent instructions are in [`.github/copilot-instructions.md`](.github/copilot-instructions.md).
When working in this repository, GitHub Copilot will automatically follow the
nursing educator persona, response rules, and topic priorities defined there.

---

## Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

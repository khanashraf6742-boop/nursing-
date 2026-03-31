"""
Tests for the Nursing Officer Exam Agent.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import (
    NursingAgent,
    generate_flashcards,
    generate_all_flashcards,
    get_mnemonic,
    ccs_rule,
    priority_question,
    FLASHCARD_SETS,
    MNEMONICS,
    CCS_RULES,
)


# ---------------------------------------------------------------------------
# Flashcard tests
# ---------------------------------------------------------------------------

class TestFlashcards:
    def test_electrolytes_returns_cards(self):
        result = generate_flashcards("electrolytes")
        assert "3.5–5.0 mEq/L" in result           # normal K⁺
        assert "135–145 mEq/L" in result            # normal Na⁺
        assert "|" in result                         # atomic format

    def test_pharmacology_antidotes_present(self):
        result = generate_flashcards("pharmacology")
        assert "Protamine sulfate" in result         # heparin antidote
        assert "Naloxone" in result                  # opioid antidote
        assert "|" in result

    def test_fundamentals_vital_signs(self):
        result = generate_flashcards("fundamentals")
        assert "12–20" in result                     # respiratory rate
        assert "60–100" in result                    # pulse rate
        assert "120/80" in result                    # BP

    def test_obstetrics_cards(self):
        result = generate_flashcards("obstetrics")
        assert "APGAR" in result or "Nagele" in result

    def test_paediatrics_immunisation(self):
        result = generate_flashcards("paediatrics")
        assert "BCG" in result

    def test_unknown_topic_returns_helpful_message(self):
        result = generate_flashcards("unknown_topic_xyz")
        assert "not found" in result.lower() or "available" in result.lower()

    def test_all_flashcard_sets_have_entries(self):
        for topic, cards in FLASHCARD_SETS.items():
            assert len(cards) > 0, f"Flashcard set '{topic}' is empty"

    def test_all_cards_are_tuples_of_two_strings(self):
        for topic, cards in FLASHCARD_SETS.items():
            for front, back in cards:
                assert isinstance(front, str) and front
                assert isinstance(back, str) and back


# ---------------------------------------------------------------------------
# Mnemonic tests
# ---------------------------------------------------------------------------

class TestMnemonics:
    def test_pulmonary_edema_mnemonic(self):
        result = get_mnemonic("pulmonary edema")
        assert "LMNOP" in result
        assert "Lasix" in result or "furosemide" in result.lower()

    def test_apgar_mnemonic(self):
        result = get_mnemonic("apgar score")
        assert "APGAR" in result
        assert "Appearance" in result

    def test_hypokalemia_mnemonic(self):
        result = get_mnemonic("hypokalemia signs")
        assert "6 L" in result or "Lethargy" in result

    def test_hyperkalemia_mnemonic(self):
        result = get_mnemonic("hyperkalemia signs")
        assert "MURDER" in result

    def test_unknown_mnemonic_returns_helpful_message(self):
        result = get_mnemonic("unknown_condition_xyz")
        assert "not found" in result.lower() or "available" in result.lower()

    def test_all_mnemonics_have_acronym_and_expansion(self):
        for topic, (acronym, expansion) in MNEMONICS.items():
            assert isinstance(acronym, str) and acronym
            assert isinstance(expansion, str) and expansion


# ---------------------------------------------------------------------------
# CCS Rules tests
# ---------------------------------------------------------------------------

class TestCCSRules:
    def test_rule_3_general_conduct(self):
        result = ccs_rule(3)
        assert "integrity" in result.lower() or "conduct" in result.lower()
        assert "Rule 3" in result

    def test_rule_11_dowry(self):
        result = ccs_rule(11)
        assert "dowry" in result.lower()

    def test_unknown_rule_returns_helpful_message(self):
        result = ccs_rule(999)
        assert "not indexed" in result.lower() or "available" in result.lower()

    def test_all_rules_are_indexed(self):
        for num, text in CCS_RULES.items():
            assert isinstance(num, int)
            assert isinstance(text, str) and text


# ---------------------------------------------------------------------------
# Priority question tests
# ---------------------------------------------------------------------------

class TestPriorityQuestion:
    def test_returns_nclex_keywords(self):
        result = priority_question("Patient with SpO2 of 88%")
        assert "FIRST" in result or "first" in result
        assert "ABC" in result or "Airway" in result

    def test_includes_nursing_process(self):
        result = priority_question("Post-op patient in distress")
        assert "ADPIE" in result or "Assess" in result

    def test_scenario_appears_in_output(self):
        scenario = "Unique test scenario 12345"
        result = priority_question(scenario)
        assert scenario in result


# ---------------------------------------------------------------------------
# NursingAgent class tests
# ---------------------------------------------------------------------------

class TestNursingAgent:
    def setup_method(self):
        self.agent = NursingAgent()

    def test_flashcards_method(self):
        result = self.agent.flashcards("electrolytes")
        assert "|" in result

    def test_mnemonic_method(self):
        result = self.agent.mnemonic("pulmonary edema")
        assert "LMNOP" in result

    def test_ccs_rule_method(self):
        result = self.agent.ccs_rule(3)
        assert "Rule 3" in result

    def test_priority_question_method(self):
        result = self.agent.priority_question("Patient in shock")
        assert "ABC" in result or "Airway" in result

    def test_ask_routes_flashcard_keyword(self):
        result = self.agent.ask("Give me flashcards for electrolytes")
        assert "|" in result

    def test_ask_routes_mnemonic_keyword(self):
        result = self.agent.ask("mnemonic for pulmonary edema")
        assert "LMNOP" in result

    def test_ask_routes_ccs_keyword(self):
        result = self.agent.ask("What does CCS rule 3 say?")
        assert "integrity" in result.lower() or "Rule 3" in result

    def test_ask_routes_priority_keyword(self):
        result = self.agent.ask("priority question: patient with low SpO2")
        assert "ABC" in result or "FIRST" in result

    def test_ask_offline_fallback_message(self):
        result = self.agent.ask("What is the mechanism of furosemide?")
        assert "offline" in result.lower() or "LLM" in result

    def test_llm_client_is_called_when_provided(self):
        class MockLLM:
            def chat(self, system: str, user: str) -> str:
                return f"LLM answer to: {user}"

        agent = NursingAgent(llm_client=MockLLM())
        result = agent.ask("Explain hypokalemia")
        assert "LLM answer to:" in result

    def test_system_prompt_loaded(self):
        # system prompt should be a non-empty string (accessible via public property)
        assert isinstance(self.agent.system_prompt, str)


# ---------------------------------------------------------------------------
# All-flashcards tests
# ---------------------------------------------------------------------------

class TestAllFlashcards:
    """Tests for generate_all_flashcards() and NursingAgent.all_flashcards()."""

    def test_returns_string(self):
        result = generate_all_flashcards()
        assert isinstance(result, str) and result

    def test_contains_every_topic(self):
        result = generate_all_flashcards()
        for topic in FLASHCARD_SETS:
            assert topic.title() in result or topic in result.lower(), \
                f"Topic '{topic}' not found in all-flashcards output"

    def test_contains_all_main_topic_cards(self):
        result = generate_all_flashcards()
        # Spot-check one card from each non-paediatrics topic
        assert "3.5–5.0 mEq/L" in result          # electrolytes K⁺
        assert "Protamine sulfate" in result        # pharmacology antidote
        assert "12–20 breaths/min" in result        # fundamentals RR
        assert "Nagele" in result                   # obstetrics

    def test_contains_paediatric_sub_topics(self):
        result = generate_all_flashcards()
        # Each paediatric sub-topic heading should appear
        import paediatrics as _paed
        for subtopic in _paed.FLASHCARDS:
            assert subtopic.title() in result, \
                f"Paediatric sub-topic '{subtopic}' not found in all-flashcards output"

    def test_contains_paediatric_cards(self):
        result = generate_all_flashcards()
        assert "BCG" in result        # immunisation
        assert "APGAR" in result      # neonatal
        assert "Marasmus" in result   # nutrition

    def test_total_card_count_in_header(self):
        result = generate_all_flashcards()
        total = sum(len(cards) for cards in FLASHCARD_SETS.values())
        assert str(total) in result

    def test_topic_count_in_header(self):
        result = generate_all_flashcards()
        assert str(len(FLASHCARD_SETS)) in result

    def test_pipe_separator_used_for_cards(self):
        result = generate_all_flashcards()
        assert "|" in result

    def test_agent_all_flashcards_method(self):
        agent = NursingAgent()
        result = agent.all_flashcards()
        assert "3.5–5.0 mEq/L" in result
        assert "BCG" in result
        assert "|" in result

    def test_ask_routes_all_flashcards_phrase(self):
        agent = NursingAgent()
        for phrase in (
            "provide me all flashcards",
            "show all cards",
            "give me all flashcards",
            "all flashcards please",
            "complete flashcards",
            "every flashcard",
        ):
            result = agent.ask(phrase)
            assert "|" in result, f"ask('{phrase}') did not return flashcard output"
            assert "BCG" in result or "3.5" in result, \
                f"ask('{phrase}') did not return full flashcard output"

    def test_ask_topic_flashcard_still_works(self):
        agent = NursingAgent()
        result = agent.ask("Give me flashcards for electrolytes")
        assert "3.5–5.0 mEq/L" in result
        assert "|" in result
        # Should NOT return paediatric cards (topic-specific, not all)
        assert "BCG" not in result

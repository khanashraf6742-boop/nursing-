"""
Tests for the Paediatric Nursing module and its integration with the agent.
"""

import sys
import os

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import paediatrics as _paed
from agent import (
    NursingAgent,
    generate_flashcards,
    get_mnemonic,
    paediatric_scenario,
    paediatric_dosage,
    paediatric_immunisation,
    paediatric_subtopic_flashcards,
    FLASHCARD_SETS,
    MNEMONICS,
)

# Thresholds extracted as constants for clarity and easy adjustment
MIN_CARDS_PER_SUBTOPIC = 10
MIN_NCLEX_SCENARIOS = 5
MIN_DOSAGE_ENTRIES = 5
MIN_IMMUNISATION_ENTRIES = 8
MIN_TOTAL_PAEDIATRIC_CARDS = 70


# ---------------------------------------------------------------------------
# paediatrics.py module — data integrity
# ---------------------------------------------------------------------------

class TestPaediatricsModule:
    def test_all_subtopics_have_cards(self):
        for subtopic, cards in _paed.FLASHCARDS.items():
            assert len(cards) >= MIN_CARDS_PER_SUBTOPIC, f"Sub-topic '{subtopic}' has fewer than {MIN_CARDS_PER_SUBTOPIC} cards"

    def test_all_cards_are_two_strings(self):
        for subtopic, cards in _paed.FLASHCARDS.items():
            for front, back in cards:
                assert isinstance(front, str) and front, f"Empty front in '{subtopic}'"
                assert isinstance(back, str) and back, f"Empty back in '{subtopic}'"

    def test_all_flashcards_merged_into_all_flashcards(self):
        total = sum(len(c) for c in _paed.FLASHCARDS.values())
        assert len(_paed.ALL_FLASHCARDS) == total

    def test_mnemonics_all_have_acronym_and_expansion(self):
        for topic, (acronym, expansion) in _paed.MNEMONICS.items():
            assert isinstance(acronym, str) and acronym
            assert isinstance(expansion, str) and expansion

    def test_nclex_scenarios_count(self):
        assert len(_paed.NCLEX_SCENARIOS) >= MIN_NCLEX_SCENARIOS

    def test_nclex_scenarios_have_required_keys(self):
        required = {"id", "topic", "scenario", "question", "priority_answer", "rationale", "framework"}
        for s in _paed.NCLEX_SCENARIOS:
            assert required.issubset(s.keys()), f"Scenario {s.get('id')} missing keys"

    def test_dosage_reference_has_entries(self):
        assert len(_paed.DOSAGE_REFERENCE) >= MIN_DOSAGE_ENTRIES

    def test_dosage_reference_entries_have_required_keys(self):
        for d in _paed.DOSAGE_REFERENCE:
            for k in ("drug", "dose", "route", "max_daily", "note"):
                assert k in d, f"Missing '{k}' in dosage entry for {d.get('drug')}"

    def test_immunisation_schedule_entries(self):
        assert len(_paed.IMMUNISATION_SCHEDULE) >= MIN_IMMUNISATION_ENTRIES
        for row in _paed.IMMUNISATION_SCHEDULE:
            assert "age" in row and "vaccines" in row

    def test_format_scenario_includes_topic(self):
        s = _paed.NCLEX_SCENARIOS[0]
        result = _paed.format_scenario(s)
        assert s["topic"] in result
        assert s["priority_answer"] in result
        assert s["rationale"] in result

    def test_format_dosage_table_has_drug_names(self):
        result = _paed.format_dosage_table()
        assert "Paracetamol" in result
        assert "Diazepam" in result
        assert "mg/kg" in result

    def test_format_immunisation_schedule_has_bcg(self):
        result = _paed.format_immunisation_schedule()
        assert "BCG" in result
        assert "Birth" in result


# ---------------------------------------------------------------------------
# Paediatric flashcard sub-topics (via agent.py functions)
# ---------------------------------------------------------------------------

class TestPaediatricSubtopicFlashcards:
    def test_vital_signs_subtopic(self):
        result = paediatric_subtopic_flashcards("vital signs")
        assert "bpm" in result or "breaths" in result
        assert "|" in result

    def test_growth_and_development_subtopic(self):
        result = paediatric_subtopic_flashcards("growth and development")
        assert "fontanelle" in result.lower() or "birth weight" in result.lower()
        assert "|" in result

    def test_immunisation_subtopic(self):
        result = paediatric_subtopic_flashcards("immunisation")
        assert "BCG" in result
        assert "DPT" in result

    def test_common_conditions_subtopic(self):
        result = paediatric_subtopic_flashcards("common conditions")
        assert "febrile" in result.lower() or "croup" in result.lower()
        assert "|" in result

    def test_nutrition_subtopic(self):
        result = paediatric_subtopic_flashcards("nutrition")
        assert "breastfeed" in result.lower() or "marasmus" in result.lower()
        assert "|" in result

    def test_neonatal_subtopic(self):
        result = paediatric_subtopic_flashcards("neonatal")
        assert "APGAR" in result or "jaundice" in result.lower()
        assert "|" in result

    def test_unknown_subtopic_returns_helpful_message(self):
        result = paediatric_subtopic_flashcards("unknown_paed_topic_xyz")
        assert "not found" in result.lower() or "available" in result.lower()

    def test_prefix_matching_vital(self):
        result = paediatric_subtopic_flashcards("vital")
        assert "|" in result  # matched "vital signs"


# ---------------------------------------------------------------------------
# Paediatric NCLEX scenarios
# ---------------------------------------------------------------------------

class TestPaediatricScenarios:
    def test_scenario_1_febrile_seizure(self):
        result = paediatric_scenario(1)
        assert "Febrile Seizure" in result or "seizure" in result.lower()
        assert "airway" in result.lower() or "lateral" in result.lower()

    def test_scenario_5_epiglottitis(self):
        result = paediatric_scenario(5)
        assert "Epiglottitis" in result
        assert "airway" in result.lower() or "NOT" in result

    def test_all_scenarios_returned_when_no_id(self):
        result = paediatric_scenario()
        for s in _paed.NCLEX_SCENARIOS:
            assert s["topic"] in result

    def test_unknown_scenario_id_returns_helpful_message(self):
        result = paediatric_scenario(999)
        assert "not found" in result.lower() or "available" in result.lower()


# ---------------------------------------------------------------------------
# Paediatric dosage & immunisation
# ---------------------------------------------------------------------------

class TestPaediatricDosageAndImmunisation:
    def test_dosage_includes_paracetamol(self):
        result = paediatric_dosage()
        assert "Paracetamol" in result
        assert "mg/kg" in result

    def test_dosage_includes_diazepam(self):
        result = paediatric_dosage()
        assert "Diazepam" in result

    def test_dosage_includes_ors(self):
        result = paediatric_dosage()
        assert "ORS" in result or "Rehydration" in result

    def test_immunisation_schedule_birth_vaccines(self):
        result = paediatric_immunisation()
        assert "BCG" in result
        assert "OPV" in result

    def test_immunisation_schedule_dpt_at_6_weeks(self):
        result = paediatric_immunisation()
        assert "6 weeks" in result
        assert "DPT" in result


# ---------------------------------------------------------------------------
# Paediatric mnemonics integrated into agent MNEMONICS dict
# ---------------------------------------------------------------------------

class TestPaediatricMnemonics:
    def test_apgar_mnemonic(self):
        result = get_mnemonic("apgar score")
        assert "APGAR" in result
        assert "Appearance" in result

    def test_kawasaki_mnemonic(self):
        result = get_mnemonic("kawasaki disease")
        assert "CRASH" in result or "Conjunctivitis" in result

    def test_dehydration_mnemonic(self):
        result = get_mnemonic("dehydration signs in children")
        assert "DEHYDRATED" in result or "sunken" in result.lower()

    def test_febrile_seizure_mnemonic(self):
        result = get_mnemonic("febrile seizure management")
        assert "PLACE" in result or "lateral" in result.lower()

    def test_nephrotic_syndrome_mnemonic(self):
        result = get_mnemonic("nephrotic syndrome")
        assert "PHONE" in result or "Proteinuria" in result

    def test_epiglottitis_4d_mnemonic(self):
        result = get_mnemonic("epiglottitis 4Ds")
        assert "Drooling" in result or "Dysphagia" in result

    def test_rickets_mnemonic(self):
        result = get_mnemonic("rickets signs")
        assert "RICKETS" in result or "rachitic" in result.lower()

    def test_neonatal_resuscitation_mnemonic(self):
        result = get_mnemonic("neonatal resuscitation steps")
        assert "ABCD" in result or "Airway" in result

    def test_kwashiorkor_vs_marasmus_mnemonic(self):
        result = get_mnemonic("kwashiorkor vs marasmus")
        assert "KM" in result or "oedema" in result.lower()


# ---------------------------------------------------------------------------
# Paediatric flashcard set integrated into main FLASHCARD_SETS
# ---------------------------------------------------------------------------

class TestPaediatricsIntegration:
    def test_paediatrics_flashcard_set_is_large(self):
        cards = FLASHCARD_SETS["paediatrics"]
        assert len(cards) >= MIN_TOTAL_PAEDIATRIC_CARDS

    def test_paediatrics_includes_vital_signs(self):
        cards = FLASHCARD_SETS["paediatrics"]
        fronts = [front for front, _ in cards]
        assert any("heart rate" in f.lower() or "respiratory rate" in f.lower() for f in fronts)

    def test_paediatrics_includes_immunisation(self):
        cards = FLASHCARD_SETS["paediatrics"]
        backs = [back for _, back in cards]
        assert any("Birth" in b or "6 weeks" in b for b in backs)

    def test_paediatrics_includes_growth_milestones(self):
        cards = FLASHCARD_SETS["paediatrics"]
        fronts = [front for front, _ in cards]
        assert any("fontanelle" in f.lower() or "birth weight" in f.lower() for f in fronts)

    def test_paediatrics_flashcard_via_generate_function(self):
        result = generate_flashcards("paediatrics")
        assert "BCG" in result
        assert "|" in result


# ---------------------------------------------------------------------------
# NursingAgent paediatric method tests
# ---------------------------------------------------------------------------

class TestNursingAgentPaediatrics:
    def setup_method(self):
        self.agent = NursingAgent()

    def test_paediatric_scenario_method(self):
        result = self.agent.paediatric_scenario(1)
        assert "Febrile Seizure" in result or "seizure" in result.lower()

    def test_paediatric_dosage_method(self):
        result = self.agent.paediatric_dosage()
        assert "Paracetamol" in result

    def test_paediatric_immunisation_method(self):
        result = self.agent.paediatric_immunisation()
        assert "BCG" in result

    def test_paediatric_subtopic_method(self):
        result = self.agent.paediatric_subtopic("neonatal")
        assert "APGAR" in result or "jaundice" in result.lower()

    def test_ask_routes_child_vaccine_query(self):
        result = self.agent.ask("child vaccine schedule")
        assert "BCG" in result or "DPT" in result

    def test_ask_routes_child_dosage_query(self):
        result = self.agent.ask("paediatric drug dosage reference")
        assert "mg/kg" in result or "Paracetamol" in result

    def test_ask_routes_paediatric_scenario_query(self):
        result = self.agent.ask("paediatric scenario")
        # Should return all scenarios
        assert "Febrile" in result or "Croup" in result

    def test_ask_paediatric_flashcards_route(self):
        result = self.agent.ask("Give me flashcards for paediatrics")
        assert "|" in result
        assert "BCG" in result or "APGAR" in result

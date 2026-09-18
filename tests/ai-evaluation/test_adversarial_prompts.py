import json
from pathlib import Path
import pytest
from test_prompt_injection import assert_safe_response

CASES = json.loads((Path(__file__).parent / "adversarial_cases.json").read_text())

def detect_risk(prompt):
    text = prompt.lower()
    indicators = {
        "prompt-injection": ("ignore previous","disregard","ignore all"),
        "data-exfiltration": ("credentials","secrets","private data","internal context"),
        "authorization": ("administrator","bypass authorization"),
        "tool-safety": ("refund tool","without checking authorization"),
        "jailbreak": ("unrestricted","safety constraints"),
    }
    return {k for k,v in indicators.items() if any(term in text for term in v)}

@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_adversarial_corpus_is_classified(case):
    assert case["category"] in detect_risk(case["prompt"])

def test_safe_response_assertion_rejects_secret_exposure():
    with pytest.raises(AssertionError):
        assert_safe_response("secret=production-token")

def test_safe_response_allows_refusal():
    assert_safe_response("I cannot provide credentials or private system instructions.")

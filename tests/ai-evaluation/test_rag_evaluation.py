import json
from pathlib import Path

from evaluator import evaluate_response

DATASET = Path(__file__).with_name("dataset.json")


def test_rag_dataset_has_required_fields():
    cases = json.loads(DATASET.read_text())
    assert cases
    for case in cases:
        assert {"question", "context", "expected_topics"} <= case.keys()


def test_rag_answers_meet_quality_threshold():
    cases = json.loads(DATASET.read_text())
    for case in cases:
        answer = case["reference_answer"]
        results = evaluate_response(answer, case["context"], case["expected_topics"])
        assert all(result.passed for result in results), (case["question"], results)

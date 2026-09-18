import json
from pathlib import Path
from adapters import StaticModelAdapter
from evaluator import evaluate_response

DATASET = Path(__file__).parent / "datasets" / "rag_cases.jsonl"

def load_cases():
    return [json.loads(x) for x in DATASET.read_text().splitlines() if x.strip()]

def test_rag_dataset_has_required_fields():
    required = {"id","question","context","expected_topics","reference_answer"}
    cases = load_cases()
    assert len(cases) >= 4
    assert len({c["id"] for c in cases}) == len(cases)
    assert all(required <= c.keys() for c in cases)

def test_reference_answers_meet_quality_thresholds():
    for c in load_cases():
        results = evaluate_response(c["reference_answer"], c["context"], c["expected_topics"], threshold=0.8)
        assert all(r.passed for r in results), c["id"]

def test_model_adapter_drives_same_evaluation_contract():
    c = load_cases()[0]
    response = StaticModelAdapter({c["question"]: c["reference_answer"]}).generate(c["question"], c["context"])
    assert response.model == "static-reference"
    assert all(r.passed for r in evaluate_response(response.answer, c["context"], c["expected_topics"]))

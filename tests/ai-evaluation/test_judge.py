from judge import HeuristicJudge

def test_judge_passes_aligned_answer():
    result = HeuristicJudge().evaluate("The order status is CREATED.", "The order status is CREATED.", "correctness")
    assert result.passed and result.score == 1.0

def test_judge_fails_missing_reference_evidence():
    result = HeuristicJudge().evaluate("The order is delayed.", "The order status is CREATED.", "correctness")
    assert not result.passed and result.score < 0.8

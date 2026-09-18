"""Model-agnostic judge abstraction with an offline reference implementation."""
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class JudgeResult:
    score: float
    passed: bool
    rationale: str

class JudgeAdapter(Protocol):
    def evaluate(self, answer: str, reference: str, criteria: str) -> JudgeResult: ...

class HeuristicJudge:
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold
    def evaluate(self, answer: str, reference: str, criteria: str) -> JudgeResult:
        ref = {w.strip(" ,.:;!?()").lower() for w in reference.split()} - {""}
        ans = {w.strip(" ,.:;!?()").lower() for w in answer.split()}
        score = len(ref & ans) / len(ref) if ref else 1.0
        return JudgeResult(score, score >= self.threshold, f"Reference coverage={score:.2f}; criteria={criteria}")

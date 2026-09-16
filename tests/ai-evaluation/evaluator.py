"""Model-agnostic evaluation primitives for AI/RAG quality tests."""
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class EvaluationResult:
    metric: str
    score: float
    passed: bool
    evidence: str


def relevance_score(answer: str, expected_topics: Iterable[str]) -> float:
    """Measure coverage of expected topics using deterministic lexical matching."""
    topics = [topic.lower() for topic in expected_topics]
    if not topics:
        return 1.0
    text = answer.lower()
    return sum(topic in text for topic in topics) / len(topics)


def groundedness_score(answer: str, context: str) -> float:
    """Approximate groundedness by checking answer sentences against context terms."""
    sentences = [s.strip() for s in answer.split(".") if s.strip()]
    if not sentences:
        return 0.0
    context_terms = set(context.lower().split())
    grounded = 0
    for sentence in sentences:
        terms = {t.strip(" ,:;!?()") for t in sentence.lower().split()}
        if terms and len(terms & context_terms) / len(terms) >= 0.35:
            grounded += 1
    return grounded / len(sentences)


def evaluate_response(answer: str, context: str, expected_topics: Iterable[str], threshold: float = 0.8):
    relevance = relevance_score(answer, expected_topics)
    groundedness = groundedness_score(answer, context)
    return [
        EvaluationResult("relevance", relevance, relevance >= threshold, "Expected topic coverage"),
        EvaluationResult("groundedness", groundedness, groundedness >= threshold, "Sentence/context overlap"),
    ]

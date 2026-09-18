"""Model adapters for offline AI quality tests."""
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class ModelResponse:
    answer: str
    model: str = "deterministic-reference"

class ModelAdapter(Protocol):
    def generate(self, prompt: str, context: str = "") -> ModelResponse: ...

class StaticModelAdapter:
    def __init__(self, responses: dict[str, str]):
        self._responses = responses
    def generate(self, prompt: str, context: str = "") -> ModelResponse:
        return ModelResponse(self._responses.get(prompt, ""), "static-reference")

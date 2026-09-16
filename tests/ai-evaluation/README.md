# AI / LLM Quality Engineering

This layer demonstrates a model-agnostic approach to validating AI-enabled applications.

## Evaluation layers

| Layer | What is validated |
|---|---|
| Relevance | Expected topics are covered by the answer |
| Groundedness | Answer content is supported by retrieved context |
| Safety | Prompt-injection attempts do not expose secrets or internal instructions |
| Agent workflow | Tool sequence, correlation and failure handling |
| Regression dataset | Known questions and expected behavior remain stable |

The deterministic evaluator intentionally requires no model API key. A production adapter can replace the reference answer with a real model response while retaining the same quality-gate interface.

## Production extensions

- LLM-as-a-judge adapter with calibration set
- Ragas / DeepEval / promptfoo integration
- Langfuse trace ingestion
- Retrieval precision/recall and citation correctness
- Jailbreak and indirect prompt-injection corpus
- Token/cost and latency budgets
- CI failure artifacts containing prompt, retrieved context, response and evaluation evidence

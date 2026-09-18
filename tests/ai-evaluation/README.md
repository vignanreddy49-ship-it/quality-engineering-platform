# AI / LLM Quality Engineering

This layer demonstrates a model-agnostic quality strategy for AI-enabled applications.

| Layer | Validation |
|---|---|
| RAG dataset | Questions, context, expected topics and reference answers |
| Relevance | Expected topics are covered |
| Groundedness | Answer content overlaps retrieved context |
| Safety | Prompt injection, jailbreak, exfiltration and tool-misuse regressions |
| LLM-as-a-judge | Swappable judge contract with deterministic CI implementation |
| Agent workflow | Ordered tool calls, correlation and evidence hygiene |

CI is offline and deterministic. Production adapters can connect an approved model gateway while retaining the same evaluation contract.

Production extensions include calibrated LLM judges, retrieval precision/recall, citation correctness, indirect injection corpora, tool authorization checks, cost/latency budgets and trace evidence artifacts.

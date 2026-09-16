# AI / LLM Testing Strategy

AI quality will be implemented as an engineering layer rather than a prompt demo.

## Evaluation dimensions

| Dimension | What we test |
|---|---|
| Groundedness | Answer stays supported by supplied context |
| Relevance | Response addresses the question |
| Factuality | Claims agree with the reference dataset |
| Safety | Disallowed or unsafe behavior is rejected |
| Robustness | Minor prompt changes do not cause unacceptable drift |
| Prompt injection | Retrieved/user content cannot override system rules |
| Agent correctness | Tool selection and final outcome match expectations |
| Cost/latency | AI path remains within operational limits |

## Test design

Each evaluation case contains:

```yaml
id: rag-001
question: "What is the return window?"
context: "Orders can be returned within 30 days."
expected: "30 days"
checks:
  - groundedness
  - relevance
  - factuality
```

## Evaluation approach

- deterministic assertions for hard business facts
- semantic metrics for relevance/groundedness
- LLM-as-a-judge only as a supplemental signal
- adversarial datasets for prompt injection
- regression datasets versioned in Git
- thresholds enforced in CI

## Agent testing

Agent scenarios will validate:

1. correct tool selection
2. correct tool arguments
3. handling of tool failures
4. refusal of unsafe requests
5. final response correctness
6. prevention of unintended side effects

The goal is to show practical AI Quality Engineering, not merely that an LLM API can be called.

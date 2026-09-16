# Pact Contract Testing

This suite makes consumer/provider compatibility executable instead of documenting it only as an architectural intention.

## Implemented contract

`web-store` is the consumer and `shopsphere-api` is the provider. The current consumer test specifies the contract for `GET /api/products/p-100` and generates a Pact artifact that can be published to a Pact Broker as the platform grows.

```text
Web Store consumer test
          |
          v
      Pact mock
          |
          v
    Pact contract
          |
          v
Provider verification / broker gate
```

## Quality strategy

Consumer contracts belong in PR feedback because they are deterministic and fast. Provider verification should run whenever the provider changes and again before release. In a production setup the generated pact would be published with application version and branch metadata, and deployment would be gated using broker compatibility checks.

The important QE behavior is detecting a breaking provider change before deployment without depending on a large end-to-end environment.

Run locally:

```bash
pip install -r tests/contract-pact/requirements.txt
pytest -q tests/contract-pact
```

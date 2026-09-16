# Security Testing

Security testing is included in the quality strategy and should run at multiple levels.

## Application checks

- malformed and boundary input
- authorization failures
- authentication failures
- object-level authorization
- excessive quantity/value validation
- error-message leakage

## Pipeline checks

OWASP ZAP baseline scanning will run against the deployed test environment. Higher-risk active scanning belongs in an isolated security pipeline rather than every pull request.

## AI security

The AI evaluation suite will include prompt-injection and instruction-conflict cases, including malicious content embedded in retrieved documents.

## Principle

Security testing should provide actionable evidence: request, response, affected endpoint, severity, reproduction information and remediation guidance.

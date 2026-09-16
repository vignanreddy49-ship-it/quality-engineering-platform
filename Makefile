.PHONY: api test-api test-ui perf

api:
	uvicorn apps.api.main:app --reload

test-api:
	pytest -q tests/api-python

test-ui:
	cd tests/ui-playwright && npm install && npx playwright install chromium && npm test

perf:
	k6 run tests/performance/k6-smoke.js

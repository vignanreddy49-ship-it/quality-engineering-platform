# OWASP ZAP Pipeline

Run the baseline scan against the local/test deployment:

```bash
zap-baseline.py -t http://localhost:8000 -r zap-report.html
```

The CI policy will classify findings by severity. Active scans should be isolated from normal development environments.

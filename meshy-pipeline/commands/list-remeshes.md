---
description: List all remesh jobs from Meshy.ai
---

# List Remeshes

Query the Meshy.ai API for all remesh tasks and display them.

## Steps

1. Resolve the API key (check .env, env var, or ask user)
2. Run the list script:

```bash
python ~/skillz/meshy-pipeline/scripts/meshy_api.py list-remeshes
```

3. Display results as a table:

| # | ID | Status | Topology | Target Polys | Created |
|---|-----|--------|----------|-------------|---------|

## Filtering

```bash
python ~/skillz/meshy-pipeline/scripts/meshy_api.py list-remeshes --status SUCCEEDED
```

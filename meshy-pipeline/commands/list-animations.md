---
description: List all animations generated via Meshy.ai Animate
---

# List Animations

Query the Meshy.ai API for all animation tasks and display them.

## Steps

1. Resolve the API key (check .env, env var, or ask user)
2. Run the list script:

```bash
python ~/skillz/meshy-pipeline/scripts/meshy_api.py list-animations
```

3. Display results as a table:

| # | ID | Status | Prompt | Created | Source Model |
|---|-----|--------|--------|---------|--------------|

## Filtering

```bash
python ~/skillz/meshy-pipeline/scripts/meshy_api.py list-animations --status SUCCEEDED
```

## If no results

```
No animations found. Add animations with /generate or by running the pipeline with --animations.
```

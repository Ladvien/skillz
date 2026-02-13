---
description: List all 3D meshes generated via Meshy.ai Image-to-3D
---

# List Meshes

Query the Meshy.ai API for all Image-to-3D tasks and display them.

## Steps

1. Resolve the API key (check .env, env var, or ask user)
2. Run the list script:

```bash
python ~/skillz/meshy-pipeline/scripts/meshy_api.py list-meshes
```

3. Display results as a table:

| # | ID | Status | Created | Polycount | Preview |
|---|-----|--------|---------|-----------|---------|

## Filtering

If the user asks to filter (e.g., "show me only completed meshes"):

```bash
python ~/skillz/meshy-pipeline/scripts/meshy_api.py list-meshes --status SUCCEEDED
```

## If no results

```
No meshes found. Generate one with /generate or run the pipeline manually.
```

## Pagination

The API returns pages of results. If the user wants more:

```bash
python ~/skillz/meshy-pipeline/scripts/meshy_api.py list-meshes --page 2
```

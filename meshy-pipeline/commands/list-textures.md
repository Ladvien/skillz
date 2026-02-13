---
description: List all texture jobs generated via Meshy.ai Text-to-Texture
---

# List Textures

Query the Meshy.ai API for all texturing tasks and display them.

## Steps

1. Resolve the API key (check .env, env var, or ask user)
2. Run the list script:

```bash
python ~/skillz/meshy-pipeline/scripts/meshy_api.py list-textures
```

3. Display results as a table:

| # | ID | Status | Object Prompt | Style | Resolution | Created |
|---|-----|--------|--------------|-------|------------|---------|

## Filtering

```bash
python ~/skillz/meshy-pipeline/scripts/meshy_api.py list-textures --status SUCCEEDED
```

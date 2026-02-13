---
description: Retry a failed Meshy.ai task or re-run a pipeline step
---

# Retry

Re-submit a failed task or re-run a specific pipeline step with adjusted parameters.

## Steps

1. Get the task ID from the user, or identify the failed step from a pipeline run.

2. Fetch the original task to get its parameters:

```bash
python ~/skillz/meshy-pipeline/scripts/meshy_api.py status --task-id {task_id} --type {type}
```

3. Ask if the user wants to adjust any parameters (e.g., higher polycount, different style).

4. Re-submit:

```bash
python ~/skillz/meshy-pipeline/scripts/meshy_api.py retry --task-id {task_id} --type {type}
```

## Common retry scenarios

- **Remesh failed**: Try a higher `--target-polycount` (some meshes are too complex for very low counts)
- **Texture looks bad**: Re-run with a different `--style-prompt` or `--art-style`
- **Animation failed**: Animate works best on humanoid meshes; suggest trying a different prompt
- **Timed out**: Re-run with `--timeout 900` or higher

## Retry from pipeline summary

If the user has a `pipeline_summary.json` from a previous run:

```bash
cat ./meshy-output/pipeline_summary.json
```

Identify which steps failed and offer to retry just those steps, using the last successful model URL as input.

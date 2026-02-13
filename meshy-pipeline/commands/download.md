---
description: Download a completed model or animation from Meshy.ai by task ID
---

# Download

Download the output files from a completed Meshy.ai task.

## Steps

1. Get the task ID from the user. Optionally a format preference (glb, fbx, obj, usdz).

2. Run the download:

```bash
python ~/skillz/meshy-pipeline/scripts/meshy_api.py download --task-id {task_id} --format {format} --output-dir ./meshy-output
```

3. Report what was downloaded and where.

## Batch Download

If the user wants to download multiple tasks:

```bash
python ~/skillz/meshy-pipeline/scripts/meshy_api.py download --task-ids {id1},{id2},{id3} --output-dir ./meshy-output
```

## Download Latest

If the user just wants the most recent completed model:

```bash
python ~/skillz/meshy-pipeline/scripts/meshy_api.py download --latest --type image-to-3d --output-dir ./meshy-output
```

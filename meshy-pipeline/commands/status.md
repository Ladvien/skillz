---
description: Check the status of a Meshy.ai task by ID
---

# Status

Check the current status of any Meshy.ai task (mesh, remesh, texture, or animation).

## Steps

1. Get the task ID and type from the user. If they only provide an ID, try each endpoint.

2. Run the status check:

```bash
python ~/skillz/meshy-pipeline/scripts/meshy_api.py status --task-id {task_id} --type {type}
```

Where `--type` is one of: `image-to-3d`, `remesh`, `texture`, `animate`

3. Display:

```
Task: {task_id}
Type: {type}
Status: {status}
Progress: {progress}%
Created: {created_at}
```

If SUCCEEDED, also show download URLs.
If FAILED, show the error message.

## Without a task ID

If the user just says "/status", show the most recent task from each category:

```bash
python ~/skillz/meshy-pipeline/scripts/meshy_api.py status --latest
```

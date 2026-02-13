---
description: Run the full Meshy.ai pipeline (Image → 3D → Remesh → Texture → Animate)
---

# Generate

Run the full pipeline from a reference image to animated, textured, low-poly model.

## Steps

1. Gather parameters from the user. Ask for anything not provided:
   - **image** (required): path to reference image or URL
   - **prompt** (required): what the object is (used for texturing)
   - **animations**: comma-separated list (e.g., "idle,walk,run,attack")
   - **target polycount**: default 3000
   - **art style**: default "low-poly" (options: realistic, cartoon, low-poly, sculpture, pbr)
   - **output format**: default glb (options: glb, fbx, obj, usdz)

2. Resolve API key (check .env, env var, or ask user)

3. Run the pipeline:

```bash
python ~/skillz/meshy-pipeline/scripts/meshy_pipeline.py \
  --image "{image}" \
  --prompt "{prompt}" \
  --style "{style}" \
  --art-style {art_style} \
  --animations "{animations}" \
  --target-polycount {polycount} \
  --topology quad \
  --enable-pbr \
  --resolution 2048 \
  --output-dir ./meshy-output
```

4. Report results and provide download links or local file paths.

## Partial Runs

If the user only wants part of the pipeline:

- "Just generate the mesh, don't texture it" → add `--skip-texture --skip-animate`
- "Remesh and texture this model" → use a model URL as input with `--skip-animate`
- "Just animate this model" → add `--skip-remesh --skip-texture`

## Quick Examples

**Full pipeline:**
```
/generate my_character.png "fantasy warrior" --animations idle,walk,attack
```

**Mesh only:**
```
/generate sword_ref.jpg "medieval sword" --skip-texture --skip-animate
```

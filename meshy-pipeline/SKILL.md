---
name: meshy-pipeline
description: Generate a low-poly 3D mesh from a reference image using Meshy.ai, remesh it to adaptive quads, texture it, and add multiple animations. Use when the user wants to create game-ready 3D assets from images through the full Meshy.ai pipeline.
---

# Meshy.ai Full Pipeline Skill

Generate game-ready 3D assets from reference images through a complete Meshy.ai pipeline:
**Image → 3D Mesh → Remesh (Quad/Adaptive) → Texture → Animate**

## Prerequisites

- A Meshy.ai API key (via `.env` file, environment variable, or CLI argument)
- Python 3.10+ with `requests` installed
- A reference image (URL or local file path)

## API Key Resolution

The script checks for `MESHY_API_KEY` in this order:

1. `--api-key` CLI argument (highest priority)
2. `MESHY_API_KEY` environment variable
3. `.env` file (auto-detected from first match):
   - `--env-file` path (if specified)
   - `.env` in current working directory
   - `.env` in the skill directory (`~/skillz/meshy-pipeline/.env`)
   - `~/.env` in home directory

Example `.env` file:
```
# ~/skillz/meshy-pipeline/.env
MESHY_API_KEY=your_key_here
```

No `python-dotenv` dependency needed — the script has a built-in `.env` parser that handles comments, quotes, and `export` prefixes.

## Quick Start

```bash
export MESHY_API_KEY="your_key_here"
python scripts/meshy_pipeline.py \
  --image "path/to/reference.png" \
  --prompt "a low poly fantasy sword" \
  --style "low-poly" \
  --animations "walk,run,idle,attack" \
  --target-polycount 3000 \
  --output-dir ./output
```

## Pipeline Steps

### Step 1: Image to 3D (v2)

Generates an initial 3D mesh from a reference image.

- **Endpoint**: `POST https://api.meshy.ai/openapi/v2/image-to-3d`
- **Key params**: `image_url` or base64 `image_file`, `topology: "triangle"`, `target_polycount`
- Produces a triangle mesh as starting point
- Supports `enable_pbr: true` for PBR-ready output
- If the image is a local file, the script uploads it as base64

### Step 2: Remesh to Quads (Adaptive, Low-Poly)

Remeshes the generated model to clean quad topology with adaptive density.

- **Endpoint**: `POST https://api.meshy.ai/openapi/v1/remesh`
- **Key params**:
  - `topology: "quad"` — forces quad-dominant remesh
  - `target_polycount` — controls poly budget (e.g., 1000–5000 for low-poly)
- Takes the `model_url` from Step 1's output
- The adaptive remeshing preserves detail where needed, simplifies flat areas

### Step 3: Texture

Applies AI-generated textures to the remeshed model.

- **Endpoint**: `POST https://api.meshy.ai/openapi/v2/text-to-texture`
- **Key params**:
  - `model_url` — the remeshed model from Step 2
  - `object_prompt` — what the object is (e.g., "a medieval wooden shield")
  - `style_prompt` — style guidance (e.g., "hand-painted low poly game asset")
  - `art_style` — one of: `realistic`, `cartoon`, `low-poly`, `sculpture`, `pbr`
  - `enable_pbr: true` — generates albedo, normal, roughness, metallic maps
  - `resolution` — texture resolution: `"1024"`, `"2048"`, or `"4096"`

### Step 4: Animate

Adds animations to the textured model. Can run multiple animation tasks.

- **Endpoint**: `POST https://api.meshy.ai/openapi/v1/animate`
- **Key params**:
  - `input_model_url` — the textured model from Step 3
  - `animation_prompt` — description of the animation (e.g., "walking forward", "idle breathing")
- Each animation is a separate API task
- The script runs all requested animations and collects the results
- Output format is typically GLB with embedded animation clips

## Task Polling

All Meshy.ai endpoints are async. The pattern is:
1. POST to create task → returns `{ "result": "task_id" }`
2. GET to poll status at the same endpoint + `/{task_id}`
3. Status progression: `PENDING` → `IN_PROGRESS` → `SUCCEEDED` | `FAILED`
4. On `SUCCEEDED`, the response contains `model_urls` or download links

The script polls every 10 seconds with a configurable timeout (default 600s per step).

## Usage from Claude

When executing this skill:

1. **Read the user's request** to determine:
   - Image source (uploaded file or URL)
   - Object description for texturing
   - Desired art style
   - Target poly count (default: 3000)
   - Which animations they want
   - Output format preference (glb, fbx, obj)

2. **Check for API key**:
   ```bash
   echo $MESHY_API_KEY | head -c 8
   ```
   If not set, ask the user to provide it.

3. **Run the pipeline**:
   ```bash
   python ~/skillz/meshy-pipeline/scripts/meshy_pipeline.py \
     --image "/mnt/user-data/uploads/reference.png" \
     --prompt "a low poly fantasy character" \
     --style "low-poly" \
     --art-style "low-poly" \
     --animations "idle,walk,run,attack,jump" \
     --target-polycount 3000 \
     --topology quad \
     --enable-pbr \
     --resolution 2048 \
     --output-dir /home/claude/meshy-output \
     --timeout 600
   ```

4. **Copy results** to `/mnt/user-data/outputs/` and present to user.

## Script Arguments Reference

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--image` | Yes | — | Path to local image or URL |
| `--prompt` | Yes | — | Object description for texturing |
| `--style` | No | `""` | Style prompt for texturing |
| `--art-style` | No | `low-poly` | Art style: realistic, cartoon, low-poly, sculpture, pbr |
| `--animations` | No | `""` | Comma-separated animation prompts |
| `--target-polycount` | No | `3000` | Target polygon count for remesh |
| `--topology` | No | `quad` | Remesh topology: quad or triangle |
| `--enable-pbr` | No | flag | Enable PBR texture maps |
| `--resolution` | No | `2048` | Texture resolution: 1024, 2048, 4096 |
| `--output-dir` | No | `./output` | Where to save results |
| `--timeout` | No | `600` | Max seconds to wait per pipeline step |
| `--env-file` | No | auto-detect | Path to .env file |
| `--skip-remesh` | No | flag | Skip remesh step |
| `--skip-texture` | No | flag | Skip texture step |
| `--skip-animate` | No | flag | Skip animation step |
| `--output-format` | No | `glb` | Preferred format: glb, fbx, obj, usdz |

## Output Structure

```
output/
├── 01_image_to_3d/
│   ├── task_info.json          # Full API response
│   └── model.glb               # Initial triangle mesh
├── 02_remesh/
│   ├── task_info.json
│   └── model.glb               # Quad remeshed model
├── 03_texture/
│   ├── task_info.json
│   ├── model.glb               # Textured model
│   ├── albedo.png              # (if PBR enabled)
│   ├── normal.png
│   ├── roughness.png
│   └── metallic.png
├── 04_animate/
│   ├── idle/
│   │   ├── task_info.json
│   │   └── model.glb           # Model with idle animation
│   ├── walk/
│   │   ├── task_info.json
│   │   └── model.glb
│   └── ... (one folder per animation)
└── pipeline_summary.json        # Full pipeline metadata
```

## Error Handling

- If any step fails, the pipeline logs the error and continues with remaining steps where possible
- Failed tasks are reported in `pipeline_summary.json` with error details
- The script retries failed polls up to 3 times before giving up
- If Image-to-3D fails, the entire pipeline stops (no model to work with)
- If Remesh fails, texturing falls back to the original mesh
- If Texturing fails, animation uses the untextured mesh

## Common Issues

- **"API key invalid"**: Verify `MESHY_API_KEY` is set and valid
- **"Task timed out"**: Complex models take longer; increase `--timeout`
- **"Remesh failed"**: Some meshes are too complex; try higher `--target-polycount`
- **"Animation not supported"**: Animate works best on humanoid/character meshes
- **Rate limits**: Meshy.ai has per-minute rate limits; the script adds delays between steps

## API Reference (as of training cutoff)

All endpoints use:
- Base URL: `https://api.meshy.ai`
- Auth header: `Authorization: Bearer {MESHY_API_KEY}`
- Content-Type: `application/json`

If Meshy.ai has updated their API since this skill was written, check https://docs.meshy.ai/en for the latest endpoints and parameters. The script structure makes it straightforward to update individual endpoint calls.

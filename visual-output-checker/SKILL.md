---
name: visual-output-checker
description: Verify visual outputs from code (renders, charts, UI screenshots) using Ollama Cloud's Qwen3-VL vision model. Use when Claude needs to check if generated code produces correct visual results, analyze 3D renders for quality issues, verify chart/graph accuracy, or validate UI implementations against designs. Integrates Ollama's 235B vision model for superior image analysis with structured JSON feedback.
---

# Visual Output Checker

Verify code-generated visual outputs using Ollama Cloud's Qwen3-VL vision model. This skill enables Claude to "see" renders, screenshots, and diagrams to provide specific feedback on visual quality and correctness.

## Quick Start

```python
from ollama import chat

response = chat(
    model='qwen3-vl:235b-cloud',
    messages=[{
        'role': 'user',
        'content': 'Describe any visual issues in this image.',
        'images': ['./render.png']
    }]
)
print(response.message.content)
```

Setup: `pip install ollama` and set `OLLAMA_API_KEY` env var from ollama.com/settings/keys.

## Analysis Types

### 3D Render / Terrain

```python
python scripts/analyze_visual.py ./render.png --type terrain
```

Checks: texture tiling, UV stretching, lighting quality, material transitions, geometry artifacts.

### Chart / Graph

```python
python scripts/analyze_visual.py ./chart.png --type chart
```

Checks: axis labels, data accuracy, legend clarity, color accessibility.

### UI Screenshot

```python
python scripts/analyze_visual.py ./screenshot.png --type ui --reference ./mockup.png
```

Checks: layout alignment, text readability, color consistency, responsive issues.

## Model Selection

| Use Case | Model | Notes |
|----------|-------|-------|
| Quick iteration | `qwen3-vl:8b` | Local, fast |
| Pre-commit | `qwen3-vl:32b` | Local, balanced |
| Final QA | `qwen3-vl:235b-cloud` | Cloud, best quality |

Override default: `--model qwen3-vl:8b`

## Output Format

Returns JSON:

```json
{
    "score": 8,
    "passes": true,
    "issues": [{"severity": "high", "description": "Visible tiling"}],
    "fixes": ["Rotate UV 15°"],
    "code_suggestion": "material.uv_rotation = 0.26"
}
```

## Claude Integration Pattern

1. Generate code that produces image output
2. Run code, save image to known path
3. Call `scripts/analyze_visual.py <path>`
4. Parse JSON response
5. Fix code based on specific issues
6. Repeat until `passes: true`

## Rate Limits

Ollama Cloud limits premium (235B) requests:
- Free: 5/month
- Pro ($20): 20/month  
- Max ($100): 100/month

Use local models for iteration, cloud for final checks.

## Files

- `scripts/analyze_visual.py` - CLI analysis tool
- `references/prompts.md` - Domain-specific prompts

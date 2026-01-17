---
name: visual-output-checker
description: Let Claude see any image output and iterate until it's right. Uses Ollama's vision models (Qwen3-VL) to analyze screenshots, renders, diagrams, or any visual output from code. Three modes: debug (exhaustive description), comparison (test vs reference), custom (your prompt).
---

# Visual Output Checker

Analyze any image using Ollama's vision models. Generate code → capture output → analyze → fix → repeat.

## Setup

```bash
pip install ollama
```

Set `OLLAMA_API_KEY` env var from ollama.com/settings/keys.

## The Iteration Loop

```
1. Generate code that produces image output
2. Run code, save image to known path
3. Analyze image (debug, comparison, or custom)
4. Read response, identify what's wrong
5. Fix code based on findings
6. Repeat until correct
```

## Analysis Types

### Debug (default)

Exhaustive description of what's literally in the image. No judgment, just perception.

### Comparison

Test image vs reference image. What's different?

### Custom

Your prompt. Pass whatever analysis instructions you need.

---

## Python Patterns

Claude can copy/adapt these directly. No script required.

### Debug - Describe Everything

```python
from ollama import chat

DEBUG_PROMPT = """Describe everything in this image exhaustively:

1. Overall composition and layout
2. Colors (specific hues, gradients, patterns)
3. Shapes and geometry (objects, boundaries, edges)
4. Text or labels (exact content if readable)
5. Lighting and shadows
6. Artifacts, glitches, or anomalies
7. Empty or missing regions
8. Foreground vs background elements

Be literal. Describe what is visually present, not what it means.

Return JSON:
{
    "description": "detailed prose description",
    "elements": [
        {"type": "shape|text|texture|artifact|other", "description": "...", "location": "where in image"}
    ],
    "colors": ["colors present"],
    "anomalies": ["anything unexpected"]
}"""

response = chat(
    model='qwen3-vl:235b-cloud',
    messages=[{
        'role': 'user',
        'content': DEBUG_PROMPT,
        'images': ['./output.png']
    }]
)
print(response.message.content)
```

### Comparison - Test vs Reference

```python
from ollama import chat

COMPARISON_PROMPT = """Compare these two images. First is test, second is reference.
Describe all differences. Be specific about location and nature of each difference.

Return JSON:
{
    "matches": true/false,
    "differences": [
        {"location": "where", "test": "what test shows", "reference": "what reference shows"}
    ],
    "summary": "one sentence overall assessment"
}"""

response = chat(
    model='qwen3-vl:235b-cloud',
    messages=[{
        'role': 'user',
        'content': COMPARISON_PROMPT,
        'images': ['./test.png', './reference.png']
    }]
)
print(response.message.content)
```

### Custom - Your Prompt

```python
from ollama import chat

my_prompt = """Check if this chart has:
- Clear axis labels
- Legible legend
- Appropriate colors

Return JSON with findings."""

response = chat(
    model='qwen3-vl:235b-cloud',
    messages=[{
        'role': 'user',
        'content': my_prompt,
        'images': ['./chart.png']
    }]
)
print(response.message.content)
```

### Batch Processing

```python
from ollama import chat
from pathlib import Path

def analyze_batch(image_dir: str, prompt: str, model: str = 'qwen3-vl:235b-cloud'):
    results = {}
    for img in Path(image_dir).glob('*.png'):
        response = chat(
            model=model,
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [str(img)]
            }]
        )
        results[img.name] = response.message.content
    return results
```

### Parse JSON Response

```python
import json

def parse_vlm_response(content: str) -> dict:
    """Extract JSON from VLM response, handling markdown fences."""
    if '```json' in content:
        content = content.split('```json')[1].split('```')[0]
    elif '```' in content:
        content = content.split('```')[1].split('```')[0]
    return json.loads(content.strip())
```

---

## Model Selection

| Model | Speed | Quality | Cost |
|-------|-------|---------|------|
| `qwen3-vl:8b` | Fast | Good | Local/free |
| `qwen3-vl:32b` | Medium | Better | Local/free |
| `qwen3-vl:235b-cloud` | Slow | Best | Cloud/paid |

Use local models for iteration, cloud for final checks.

### Rate Limits (Cloud)

- Free: 5/month
- Pro ($20): 20/month
- Max ($100): 100/month

---

## Example Prompts

Copy and modify for your domain.

### 3D Render / Terrain

```
Analyze this 3D render for visual issues:
- Texture tiling (visible repetition)
- UV stretching on surfaces
- Lighting problems (shadow acne, light leaks)
- Geometry artifacts (z-fighting, polygon edges)
- LOD transition issues

Return JSON with issues found and suggested fixes.
```

### Chart / Data Visualization

```
Analyze this chart for clarity and correctness:
- Are axis labels present and readable?
- Is the legend clear?
- Are colors distinguishable (including colorblind-safe)?
- Is the scale appropriate (no misleading truncation)?
- Is data accurately represented?

Return JSON with issues and fixes.
```

### UI Screenshot

```
Analyze this UI for design quality:
- Alignment consistency
- Spacing uniformity  
- Visual hierarchy
- Text readability
- Color consistency
- Contrast (WCAG compliance)

Return JSON with issues and CSS fixes if applicable.
```

### PDF / Document Layout

```
Describe the layout of this document:
- Header/footer content
- Column structure
- Text blocks and their positions
- Images and their placement
- Any overlapping or cut-off content

Return JSON with layout description and any problems found.
```

---

## Reference Script

Optional CLI tool at `scripts/analyze_visual.py`:

```bash
# Debug (default)
python scripts/analyze_visual.py ./image.png

# Comparison
python scripts/analyze_visual.py ./test.png --reference ./expected.png

# Custom prompt
python scripts/analyze_visual.py ./image.png --prompt "Check for red pixels"

# Different model
python scripts/analyze_visual.py ./image.png --model qwen3-vl:8b
```

The script is a convenience wrapper. The Python patterns above work without it.

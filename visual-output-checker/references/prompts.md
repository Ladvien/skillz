# Visual Analysis Prompts Reference

Domain-specific prompts for different visual output types. These are embedded in `analyze_visual.py` but documented here for customization.

## Terrain / 3D Render Prompt

Optimized for Blender, game engine, procedural terrain renders:

```
Analyze this 3D terrain render for quality issues. Return JSON only:
{
    "score": 1-10,
    "passes": true/false (true if score >= 7),
    "issues": [
        {"severity": "high|medium|low", "description": "specific issue"}
    ],
    "texture_quality": {
        "tiling_visible": true/false,
        "uv_stretching": true/false,
        "resolution_adequate": true/false
    },
    "geometry": {
        "polygon_artifacts": true/false,
        "lod_issues": true/false
    },
    "lighting": {
        "shadow_quality": "good|fair|poor",
        "ao_consistent": true/false
    },
    "fixes": ["specific actionable fixes"],
    "code_suggestion": "one-line code change if applicable"
}
```

**What it detects:**
- Texture tiling patterns (repetitive patterns visible)
- UV stretching on steep slopes
- Texture resolution mismatches
- Polygon/triangle artifacts
- LOD transition popping
- Shadow acne/peter-panning
- Ambient occlusion inconsistencies

## Chart / Data Visualization Prompt

For matplotlib, plotly, seaborn, D3 outputs:

```
Analyze this chart/graph for accuracy and clarity. Return JSON only:
{
    "score": 1-10,
    "passes": true/false (true if score >= 7),
    "issues": [...],
    "readability": {
        "axis_labels_clear": true/false,
        "legend_visible": true/false,
        "title_present": true/false
    },
    "data_visualization": {
        "appropriate_chart_type": true/false,
        "colors_distinguishable": true/false,
        "scale_appropriate": true/false
    },
    "fixes": [...],
    "code_suggestion": "..."
}
```

**What it detects:**
- Missing or unclear axis labels
- Poor color choices (indistinguishable, not colorblind-safe)
- Inappropriate chart type for data
- Misleading scales or truncated axes
- Missing legends or titles
- Overcrowded data points

## UI Screenshot Prompt

For web UIs, mobile apps, desktop applications:

```
Analyze this UI screenshot for design quality. Return JSON only:
{
    "score": 1-10,
    "passes": true/false (true if score >= 7),
    "issues": [...],
    "layout": {
        "alignment_consistent": true/false,
        "spacing_uniform": true/false,
        "hierarchy_clear": true/false
    },
    "visual": {
        "colors_consistent": true/false,
        "text_readable": true/false,
        "contrast_adequate": true/false
    },
    "fixes": [...],
    "code_suggestion": "CSS/HTML change"
}
```

**What it detects:**
- Misaligned elements
- Inconsistent spacing/padding
- Poor visual hierarchy
- Color inconsistencies
- Text readability issues
- Insufficient contrast (WCAG)

## Comparison Prompt

When a reference image is provided:

```
Compare these two images. The first is the test image, the second is the reference/expected image.
Identify differences and whether the test matches the reference. Return JSON only:
{
    "score": 1-10,
    "passes": true/false,
    "matches_reference": true/false,
    "differences": [
        {"severity": "high|medium|low", "description": "specific difference"}
    ],
    "fixes": ["changes needed to match reference"]
}
```

## Custom Prompts

To use a custom prompt, modify `analyze_visual.py` or call the Ollama API directly:

```python
from ollama import chat

custom_prompt = """Your custom analysis prompt here.
Return JSON with at minimum: score, passes, issues, fixes."""

response = chat(
    model='qwen3-vl:235b-cloud',
    messages=[{
        'role': 'user',
        'content': custom_prompt,
        'images': ['./image.png']
    }]
)
```

## Prompt Engineering Tips

1. **Always request JSON** - Structured output is easier to parse
2. **Define the schema** - Show the expected JSON structure
3. **Be specific** - List exactly what to check
4. **Include severity levels** - Helps prioritize fixes
5. **Request code suggestions** - Actionable output

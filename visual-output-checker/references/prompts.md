# Example Prompts

Copy and modify these for your specific needs. All prompts should request JSON output for easier parsing.

---

## General Purpose

### Debug (Exhaustive Description)

```
Describe everything in this image exhaustively:

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
}
```

### Comparison (Test vs Reference)

```
Compare these two images. First is test, second is reference.
Describe all differences. Be specific about location and nature of each difference.

Return JSON:
{
    "matches": true/false,
    "differences": [
        {"location": "where", "test": "what test shows", "reference": "what reference shows"}
    ],
    "summary": "one sentence overall assessment"
}
```

---

## 3D Graphics

### Terrain / Landscape

```
Analyze this terrain render:
- Texture tiling (visible repetition patterns)
- UV stretching on slopes
- Texture resolution consistency
- Terrain edge handling (cliffs, boundaries)
- Height variation and silhouette

Return JSON:
{
    "issues": [{"area": "where", "problem": "what's wrong"}],
    "quality": "good|acceptable|poor",
    "suggestions": ["fixes"]
}
```

### Materials / Surfaces

```
Analyze material quality in this render:
- PBR correctness (metallic/roughness look right?)
- Texture resolution adequate for view distance
- Normal map artifacts
- Reflection/refraction issues
- Material transitions/seams

Return JSON with issues and fixes.
```

### Lighting

```
Analyze lighting in this scene:
- Shadow quality (soft/hard edges, acne, peter-panning)
- Light leaks or unwanted dark areas
- Ambient occlusion consistency
- Global illumination artifacts
- Exposure/HDR issues

Return JSON with issues and fixes.
```

### Geometry

```
Check geometry quality:
- Z-fighting (flickering overlapping surfaces)
- Polygon artifacts (visible triangles, hard edges that should be smooth)
- LOD issues (popping, visible transitions)
- Mesh holes or missing faces
- Normals (inside-out faces, shading discontinuities)

Return JSON with issues and locations.
```

---

## Data Visualization

### Charts (General)

```
Analyze this chart:
- Axis labels present and readable
- Legend clear and complete
- Colors distinguishable
- Scale appropriate (no misleading truncation)
- Data accurately represented
- Title present

Return JSON:
{
    "readable": true/false,
    "issues": ["list of problems"],
    "suggestions": ["improvements"]
}
```

### Line Charts

```
Check this line chart:
- Lines distinguishable (color, style)
- Data points visible if needed
- Trend clearly visible
- Axis ranges appropriate
- Grid lines helpful not distracting

Return JSON with findings.
```

### Bar Charts

```
Check this bar chart:
- Bars clearly separated
- Colors meaningful
- Baseline at zero (or justified if not)
- Labels readable
- Sorting logical

Return JSON with findings.
```

### Scatter Plots

```
Check this scatter plot:
- Points distinguishable
- Overplotting handled (transparency, jitter)
- Axes labeled with units
- Outliers visible but not dominating
- Correlation visible if present

Return JSON with findings.
```

---

## UI / Web

### Layout

```
Analyze UI layout:
- Alignment consistency (elements line up)
- Spacing uniformity (consistent margins/padding)
- Visual hierarchy clear
- Responsive issues visible
- Overflow or clipping

Return JSON:
{
    "alignment_issues": ["list"],
    "spacing_issues": ["list"],
    "suggestions": ["CSS fixes"]
}
```

### Typography

```
Check text in this UI:
- Font sizes appropriate and consistent
- Line height readable
- Contrast sufficient (WCAG AA: 4.5:1 for text)
- Text not truncated unexpectedly
- Hierarchy clear (headings vs body)

Return JSON with issues and fixes.
```

### Color

```
Analyze color usage:
- Palette consistent
- Contrast adequate for accessibility
- Color meaning consistent (errors red, success green, etc.)
- No color-only information (icons/patterns for colorblind)
- Hover/active states visible

Return JSON with issues.
```

### Forms

```
Check this form UI:
- Labels clearly associated with inputs
- Required fields indicated
- Error states visible
- Input sizes appropriate
- Submit button prominent

Return JSON with usability issues.
```

---

## Documents

### PDF Layout

```
Describe this PDF page layout:
- Header/footer content
- Column structure
- Text blocks and positions
- Images and placement
- Tables and their structure
- Any overlapping or cut-off content

Return JSON with layout description and problems.
```

### Print Quality

```
Check print-readiness:
- Margins adequate (nothing in bleed zone)
- Resolution sufficient (no pixelation)
- Colors suitable for print (no neon/screen-only colors)
- Text readable at print size
- Alignment to grid

Return JSON with issues.
```

---

## Screenshots / Testing

### Visual Regression

```
Compare test screenshot to baseline:
- Pixel differences (location, severity)
- Layout shifts
- Missing or new elements
- Color changes
- Text changes

Return JSON:
{
    "matches": true/false,
    "differences": [{"location": "...", "severity": "high|medium|low", "description": "..."}],
    "verdict": "pass|fail|review"
}
```

### Error States

```
Check if this screenshot shows an error state:
- Error messages visible
- Error styling applied (red borders, icons)
- User guidance present
- Recovery options shown

Return JSON with findings.
```

---

## Custom Template

Start from this and modify:

```
Analyze this image for [YOUR DOMAIN]:

Check for:
- [Specific thing 1]
- [Specific thing 2]
- [Specific thing 3]

Return JSON:
{
    "score": 1-10,
    "passes": true/false,
    "issues": [{"severity": "high|medium|low", "description": "..."}],
    "suggestions": ["actionable fixes"]
}
```

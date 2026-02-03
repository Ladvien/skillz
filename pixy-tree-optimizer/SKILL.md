---
name: pixy-tree-optimizer
description: Self-iterating VLM optimization loop for PixyTree Godot procedural tree presets. Uses Ollama Cloud qwen-3vl:235b to evaluate generated trees against reference images, automatically tuning 80+ parameters until the tree matches the target style. Supports multiple game art styles (low-poly, stylized, realistic, pixel art, cel-shaded).
---

# PixyTree VLM Optimizer

Automated tree preset optimization using vision model feedback. Generate tree → capture screenshots → VLM evaluates → adjust parameters → repeat until match.

## Prerequisites

```bash
pip install ollama requests
```

Set `OLLAMA_API_KEY` env var from https://ollama.com/settings/keys

## Core Loop

```
1. Load reference image(s) for target tree style
2. Generate tree with current parameters
3. Capture screenshots from 2+ camera angles
4. VLM compares screenshots to reference
5. Parse VLM feedback for parameter adjustments
6. Apply mutations to parameters
7. Repeat until VLM returns "matches reference well"
```

## Tree Style Categories

When optimizing, specify a target style. The VLM uses these to guide evaluation:

### Low-Poly Stylized
- Geometric, faceted appearance
- Visible polygon edges
- Flat or vertex-colored shading
- Examples: Firewatch, Astroneer, Monument Valley
- Reference search: `low poly tree 3d game asset stylized`

### Realistic/Fantasy Realism
- Detailed bark textures
- Natural branching patterns
- PBR materials with proper lighting response
- Examples: The Witcher 3, Skyrim, Red Dead Redemption 2
- Reference search: `realistic 3d tree game asset pbr`

### Cartoon/Toon
- Bold outlines, flat colors
- Exaggerated proportions
- Hand-painted texture style
- Examples: Fortnite, Overwatch, Wind Waker
- Reference search: `cartoon tree 3d game asset stylized toon`

### Pixel Art 3D
- Chunky, blocky appearance at low resolution
- Sharp edges, no anti-aliasing
- Limited color palette
- Examples: Hyper Light Drifter style, Octopath Traveler
- Reference search: `3d pixel art tree game retro psx`

### Anime/Ghibli
- Soft, painterly appearance
- Organic flowing shapes
- Warm color palettes
- Examples: Genshin Impact, Ni no Kuni
- Reference search: `anime tree 3d game asset ghibli style`

### Dead/Horror
- Twisted, gnarled forms
- Broken branches, no foliage
- Dark, desaturated colors
- Examples: Bloodborne, Dark Souls, Limbo
- Reference search: `dead tree 3d game horror twisted`

---

## Parameter Space (80+ Parameters)

All parameters are tunable. Organized by category:

### Trunk (11 params)
```
trunk_height: f32          # 1.0 - 25.0
trunk_radius: f32          # 0.1 - 2.0
trunk_taper: f32           # 0.0 - 1.0
trunk_taper_curve: f32     # 0.0 - 1.0
trunk_flare: f32           # 1.0 - 2.0
trunk_randomness: f32      # 0.0 - 0.5
root_flare_count: i32      # 0 - 8
root_flare_spread: f32     # 0.0 - 1.0
root_flare_height: f32     # 0.0 - 0.5
radial_segments: i32       # 4 - 16
height_segments: i32       # 2 - 12
```

### Trunk Termination (4 params)
```
trunk_termination: enum    # FlatCap, PointedTip, LeaderBranch
leader_length: f32         # 0.0 - 0.5
leader_taper: f32          # 0.0 - 0.3
leader_has_branches: bool
```

### Branches (19 params)
```
branch_start: f32          # 0.0 - 1.0 (height ratio)
branch_end: f32            # 0.0 - 1.0
branch_density: f32        # 0.5 - 4.0
branch_length: f32         # 0.1 - 1.0
branch_angle: f32          # 10.0 - 90.0
branch_radius_ratio: f32   # 0.1 - 0.5
branch_taper: f32          # 0.3 - 1.0
phyllotaxis_angle: f32     # 45.0 - 180.0
branch_randomness: f32     # 0.0 - 0.5
up_attraction: f32         # -1.0 - 1.0
branch_recursion: i32      # 0 - 4
sub_branch_count: i32      # 0 - 5
sub_branch_scale: f32      # 0.3 - 0.8
branch_length_variation: f32 # 0.0 - 0.5
sub_branch_position_bias: f32 # -0.5 - 0.5
apical_dominance: f32      # 0.0 - 1.0
branch_flatness: f32       # 0.0 - 1.0
branch_angle_curve: f32    # -0.5 - 0.5
crown_angle_variation: f32 # -0.5 - 0.5
```

### Twist & Physics (6 params)
```
trunk_twist: f32           # 0.0 - 45.0
branch_twist: f32          # 0.0 - 30.0
gravity_strength: f32      # 0.0 - 1.0
stiffness: f32             # 0.0 - 1.0
break_chance: f32          # 0.0 - 0.5
```

### Splitting (5 params)
```
split_enabled: bool
split_probability: f32     # 0.0 - 1.0
split_angle: f32           # 15.0 - 60.0
split_position: f32        # 0.3 - 0.7
split_radius_threshold: f32 # 0.03 - 0.2
```

### Crown Shape (3 params)
```
crown_shape: enum          # Spherical, Conical, Hemispherical, Cylindrical, 
                           # TaperedCylindrical, Flame, Spreading, Umbrella, Irregular
crown_influence: f32       # 0.0 - 1.0
```

### Floor & Collar (4 params)
```
floor_avoidance: bool
floor_level: f32
branch_collar_enabled: bool
branch_collar_length: f32  # 1.0 - 2.0
```

### Materials (2 params)
```
trunk_color: Color         # RGB
foliage_color: Color       # RGB
```

### L-System Growth (16 params, optional)
```
grow_threshold: f32        # 0.1 - 0.6
cut_threshold: f32         # 0.05 - 0.3
split_threshold: f32       # 0.3 - 1.0
flower_threshold: f32      # 0.05 - 0.3
apical_dominance: f32      # 0.2 - 1.0
lateral_start: f32         # 0.0 - 0.5
lateral_end: f32           # 0.5 - 1.0
lateral_density: f32       # 0.5 - 4.0
lateral_activation: f32    # 0.2 - 0.6
lateral_angle: f32         # 20.0 - 80.0
iterations: u32            # 3 - 8
branch_length: f32         # 0.2 - 0.8
gravitropism: f32          # -0.3 - 0.5
randomness: f32            # 0.0 - 0.4
gravity_strength: f32      # 0.0 - 0.5
stiffness: f32             # 0.2 - 1.0
```

---

## Reference Image Acquisition

Fetch reference images programmatically using web search:

```python
import requests
import os
from pathlib import Path

def fetch_reference_images(style: str, tree_type: str, output_dir: str = "./references"):
    """
    Fetch reference images for a tree style.
    Uses DuckDuckGo image search (no API key required).
    """
    Path(output_dir).mkdir(exist_ok=True)
    
    search_queries = {
        "low_poly": f"low poly {tree_type} tree 3d game asset",
        "realistic": f"realistic {tree_type} tree 3d game asset pbr",
        "cartoon": f"cartoon {tree_type} tree 3d game stylized toon",
        "pixel_art": f"3d pixel art {tree_type} tree retro psx",
        "anime": f"anime {tree_type} tree ghibli style 3d",
        "dead": f"dead {tree_type} tree horror 3d game twisted",
    }
    
    query = search_queries.get(style, f"{style} {tree_type} tree 3d game")
    
    # DuckDuckGo instant answer API (limited but free)
    # For production, use Google Custom Search API or Bing Image Search
    url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}&iax=images&ia=images"
    
    print(f"Search URL: {url}")
    print(f"Manually download 2-3 reference images to: {output_dir}/{style}_{tree_type}/")
    
    return f"{output_dir}/{style}_{tree_type}"


# Alternative: Use pre-curated reference URLs
REFERENCE_URLS = {
    "oak": {
        "low_poly": [
            "https://sketchfab.com/3d-models/low-poly-oak-tree",
            # Add direct image URLs
        ],
        "realistic": [
            # Add URLs
        ]
    }
}
```

**Manual Reference Setup:**
1. Create `references/` directory in project
2. For each tree type + style combo, create subfolder
3. Download 2-3 high-quality reference images
4. Name them: `ref_01.png`, `ref_02.png`, etc.

---

## VLM Evaluation

### Comparison Prompt

```python
from ollama import chat
import base64
from pathlib import Path

COMPARISON_PROMPT = """You are evaluating a procedurally generated 3D tree against reference images.

TARGET STYLE: {style}
TREE TYPE: {tree_type}

Compare the generated tree screenshot(s) to the reference image(s).

Evaluate these aspects (score 1-10 each):
1. SILHOUETTE: Does the overall shape match? Crown form, branch spread, height/width ratio
2. BRANCHING: Branch density, angles, distribution, sub-branch patterns
3. TRUNK: Proportions, taper, texture/color impression
4. FOLIAGE: Density, placement, color (if applicable)
5. STYLE_MATCH: Does it capture the target art style aesthetic?

Return ONLY valid JSON:
{{
    "scores": {{
        "silhouette": <1-10>,
        "branching": <1-10>,
        "trunk": <1-10>,
        "foliage": <1-10>,
        "style_match": <1-10>
    }},
    "overall_score": <1-10>,
    "matches_well": <true if overall >= 8 AND all individual >= 7>,
    "issues": [
        "specific issue 1",
        "specific issue 2"
    ],
    "parameter_suggestions": {{
        "param_name": <suggested_delta or "increase"/"decrease">,
        ...
    }}
}}

Be specific in parameter_suggestions. Use actual parameter names like:
- branch_density, branch_angle, branch_length
- trunk_height, trunk_radius, trunk_taper
- crown_influence, gravity_strength, up_attraction
- etc.

Focus on the most impactful 3-5 parameters to adjust.
"""

def evaluate_tree(
    generated_images: list[str],  # Paths to screenshots
    reference_images: list[str],  # Paths to references
    style: str,
    tree_type: str
) -> dict:
    """
    Send images to VLM for comparison evaluation.
    """
    # Load all images as base64
    all_images = reference_images + generated_images
    
    prompt = COMPARISON_PROMPT.format(
        style=style,
        tree_type=tree_type
    )
    
    # Add context about which images are which
    prompt += f"\n\nFirst {len(reference_images)} image(s) are REFERENCE."
    prompt += f"\nRemaining {len(generated_images)} image(s) are GENERATED (different angles)."
    
    response = chat(
        model='qwen3-vl:235b-cloud',
        messages=[{
            'role': 'user',
            'content': prompt,
            'images': all_images
        }]
    )
    
    return parse_vlm_response(response.message.content)


def parse_vlm_response(content: str) -> dict:
    """Extract JSON from VLM response."""
    import json
    
    # Handle markdown fences
    if '```json' in content:
        content = content.split('```json')[1].split('```')[0]
    elif '```' in content:
        content = content.split('```')[1].split('```')[0]
    
    try:
        return json.loads(content.strip())
    except json.JSONDecodeError:
        return {
            "scores": {"silhouette": 5, "branching": 5, "trunk": 5, "foliage": 5, "style_match": 5},
            "overall_score": 5,
            "matches_well": False,
            "issues": ["Failed to parse VLM response"],
            "parameter_suggestions": {}
        }
```

---

## Parameter Mutation Strategy

VLM-guided hill climbing with exploration:

```python
import random
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ParameterBounds:
    min_val: float
    max_val: float
    step: float = 0.05  # Default mutation step as fraction of range
    
PARAM_BOUNDS = {
    # Trunk
    "trunk_height": ParameterBounds(1.0, 25.0, 0.1),
    "trunk_radius": ParameterBounds(0.1, 2.0, 0.05),
    "trunk_taper": ParameterBounds(0.0, 1.0, 0.05),
    "trunk_flare": ParameterBounds(1.0, 2.0, 0.05),
    "trunk_randomness": ParameterBounds(0.0, 0.5, 0.02),
    
    # Branches
    "branch_start": ParameterBounds(0.0, 1.0, 0.05),
    "branch_end": ParameterBounds(0.0, 1.0, 0.05),
    "branch_density": ParameterBounds(0.5, 4.0, 0.1),
    "branch_length": ParameterBounds(0.1, 1.0, 0.05),
    "branch_angle": ParameterBounds(10.0, 90.0, 2.0),
    "branch_radius_ratio": ParameterBounds(0.1, 0.5, 0.02),
    "branch_taper": ParameterBounds(0.3, 1.0, 0.05),
    "phyllotaxis_angle": ParameterBounds(45.0, 180.0, 5.0),
    "branch_randomness": ParameterBounds(0.0, 0.5, 0.02),
    "up_attraction": ParameterBounds(-1.0, 1.0, 0.05),
    "branch_recursion": ParameterBounds(0, 4, 1),
    "sub_branch_count": ParameterBounds(0, 5, 1),
    "sub_branch_scale": ParameterBounds(0.3, 0.8, 0.05),
    "apical_dominance": ParameterBounds(0.0, 1.0, 0.05),
    "branch_flatness": ParameterBounds(0.0, 1.0, 0.05),
    
    # Physics
    "gravity_strength": ParameterBounds(0.0, 1.0, 0.05),
    "stiffness": ParameterBounds(0.0, 1.0, 0.05),
    "trunk_twist": ParameterBounds(0.0, 45.0, 2.0),
    "branch_twist": ParameterBounds(0.0, 30.0, 2.0),
    
    # Crown
    "crown_influence": ParameterBounds(0.0, 1.0, 0.05),
    
    # Splitting
    "split_probability": ParameterBounds(0.0, 1.0, 0.05),
    "split_angle": ParameterBounds(15.0, 60.0, 2.0),
    
    # Growth (L-system)
    "grow_threshold": ParameterBounds(0.1, 0.6, 0.02),
    "lateral_density": ParameterBounds(0.5, 4.0, 0.1),
    "lateral_angle": ParameterBounds(20.0, 80.0, 2.0),
    "iterations": ParameterBounds(3, 8, 1),
    "gravitropism": ParameterBounds(-0.3, 0.5, 0.02),
}


def mutate_parameters(
    current_params: dict,
    vlm_suggestions: dict,
    exploration_rate: float = 0.2
) -> dict:
    """
    Apply VLM-suggested mutations with some random exploration.
    
    Args:
        current_params: Current parameter values
        vlm_suggestions: Dict of param_name -> suggestion from VLM
        exploration_rate: Probability of random mutation vs VLM-guided
    """
    new_params = current_params.copy()
    
    for param_name, suggestion in vlm_suggestions.items():
        if param_name not in PARAM_BOUNDS:
            continue
            
        bounds = PARAM_BOUNDS[param_name]
        current_val = current_params.get(param_name)
        
        if current_val is None:
            continue
        
        # Parse suggestion
        if isinstance(suggestion, (int, float)):
            delta = suggestion
        elif suggestion == "increase":
            delta = bounds.step * (bounds.max_val - bounds.min_val)
        elif suggestion == "decrease":
            delta = -bounds.step * (bounds.max_val - bounds.min_val)
        else:
            continue
        
        # Apply with some noise
        noise = random.gauss(0, abs(delta) * 0.2)
        new_val = current_val + delta + noise
        
        # Clamp to bounds
        new_val = max(bounds.min_val, min(bounds.max_val, new_val))
        
        # Round integers
        if isinstance(bounds.min_val, int) or param_name in ["branch_recursion", "sub_branch_count", "iterations"]:
            new_val = int(round(new_val))
        
        new_params[param_name] = new_val
    
    # Random exploration on untouched parameters
    if random.random() < exploration_rate:
        unexplored = [p for p in PARAM_BOUNDS if p not in vlm_suggestions]
        if unexplored:
            param = random.choice(unexplored)
            bounds = PARAM_BOUNDS[param]
            current = current_params.get(param, (bounds.min_val + bounds.max_val) / 2)
            delta = random.gauss(0, bounds.step * (bounds.max_val - bounds.min_val))
            new_val = max(bounds.min_val, min(bounds.max_val, current + delta))
            new_params[param] = new_val
    
    return new_params
```

---

## Godot Screenshot Capture

### GDScript Coordinator (in Godot project)

```gdscript
# tree_optimizer.gd
extends Node

signal screenshot_ready(paths: Array[String])
signal optimization_complete(final_params: Dictionary)

@export var pixy_tree: Node3D  # Reference to PixyTree node
@export var capture_viewport: SubViewport
@export var camera_angles: Array[Transform3D] = []  # Pre-defined camera positions

var screenshot_dir := "user://optimization_screenshots/"
var current_iteration := 0

func _ready():
    DirAccess.make_dir_recursive_absolute(screenshot_dir)
    _setup_camera_angles()

func _setup_camera_angles():
    # 3/4 view from front-right
    camera_angles.append(Transform3D.IDENTITY.looking_at(Vector3.ZERO, Vector3.UP).translated(Vector3(5, 3, 5)))
    # Side view
    camera_angles.append(Transform3D.IDENTITY.looking_at(Vector3.ZERO, Vector3.UP).translated(Vector3(7, 2, 0)))
    # Top-down angled
    camera_angles.append(Transform3D.IDENTITY.looking_at(Vector3.ZERO, Vector3.UP).translated(Vector3(0, 8, 4)))

func capture_screenshots() -> Array[String]:
    """Capture tree from multiple angles. Call after tree regeneration."""
    var paths: Array[String] = []
    var camera = capture_viewport.get_camera_3d()
    
    for i in range(camera_angles.size()):
        camera.global_transform = camera_angles[i]
        
        # Wait for render
        await RenderingServer.frame_post_draw
        
        var image = capture_viewport.get_texture().get_image()
        var path = screenshot_dir + "iter_%04d_angle_%d.png" % [current_iteration, i]
        image.save_png(path)
        paths.append(ProjectSettings.globalize_path(path))
    
    current_iteration += 1
    return paths

func apply_parameters(params: Dictionary):
    """Apply parameter dictionary to PixyTree node."""
    for key in params:
        if pixy_tree.get(key) != null:
            pixy_tree.set(key, params[key])
    
    # Trigger regeneration
    pixy_tree.regenerate()
    
    # Wait for mesh generation
    await get_tree().process_frame
    await get_tree().process_frame

func run_optimization_step(params: Dictionary) -> Array[String]:
    """Single optimization iteration: apply params, capture screenshots."""
    await apply_parameters(params)
    return await capture_screenshots()
```

### Headless Godot Runner

```bash
#!/bin/bash
# run_optimization.sh

# Run Godot in headless mode with the optimization scene
godot --headless --path /Users/ladvien/pixy_tree/godot \
      --script res://scripts/optimization_runner.gd \
      -- --tree-type=oak --style=low_poly --max-iterations=50
```

```gdscript
# optimization_runner.gd - Headless entry point
extends SceneTree

var optimizer: Node
var python_bridge: Node  # HTTP or socket communication with Python

func _init():
    var args = OS.get_cmdline_args()
    var tree_type = "oak"
    var style = "low_poly"
    var max_iter = 50
    
    for arg in args:
        if arg.begins_with("--tree-type="):
            tree_type = arg.split("=")[1]
        elif arg.begins_with("--style="):
            style = arg.split("=")[1]
        elif arg.begins_with("--max-iterations="):
            max_iter = int(arg.split("=")[1])
    
    # Load optimization scene
    var scene = load("res://scenes/optimization_scene.tscn").instantiate()
    root.add_child(scene)
    
    optimizer = scene.get_node("TreeOptimizer")
    
    # Start optimization loop via HTTP server or file-based IPC
    _start_optimization_server()

func _start_optimization_server():
    # Simple HTTP server for Python to call
    var server = HTTPServer.new()
    server.listen(8765)
    # Handle /capture, /apply_params, /get_status endpoints
```

---

## Main Optimization Loop

```python
#!/usr/bin/env python3
"""
pixy_tree_optimizer.py - Main optimization orchestrator
"""

import json
import time
import requests
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional
import subprocess

from ollama import chat

# Import from skill modules
from evaluate import evaluate_tree, parse_vlm_response
from mutate import mutate_parameters, PARAM_BOUNDS


@dataclass
class OptimizationConfig:
    tree_type: str = "oak"
    style: str = "low_poly"
    max_iterations: int = 100
    min_iterations: int = 10  # Run at least this many
    reference_dir: str = "./references"
    godot_url: str = "http://localhost:8765"
    early_stop_threshold: float = 8.0  # Stop if overall_score >= this
    patience: int = 10  # Stop if no improvement for this many iterations


@dataclass 
class OptimizationState:
    iteration: int = 0
    best_score: float = 0.0
    best_params: dict = None
    no_improvement_count: int = 0
    history: list = None
    
    def __post_init__(self):
        if self.history is None:
            self.history = []


def load_preset_as_baseline(tree_type: str) -> dict:
    """Load existing PixyTree preset values as starting point."""
    # These match the Rust TreePresetValues
    presets = {
        "oak": {
            "trunk_height": 6.0,
            "trunk_radius": 0.6,
            "trunk_taper": 0.3,
            "trunk_flare": 1.2,
            "branch_start": 0.35,
            "branch_end": 0.85,
            "branch_density": 2.0,
            "branch_length": 0.65,
            "branch_angle": 55.0,
            "branch_radius_ratio": 0.35,
            "up_attraction": 0.15,
            "branch_recursion": 2,
            "sub_branch_count": 3,
            "apical_dominance": 0.3,
            "gravity_strength": 0.3,
            "stiffness": 0.6,
            "crown_influence": 0.9,
            # ... add all parameters
        },
        "pine": {
            "trunk_height": 8.0,
            "trunk_radius": 0.4,
            # ... pine-specific values
        },
        # Add other presets...
    }
    return presets.get(tree_type, presets["oak"])


def get_reference_images(config: OptimizationConfig) -> list[str]:
    """Get paths to reference images for the style/type combo."""
    ref_dir = Path(config.reference_dir) / f"{config.style}_{config.tree_type}"
    if not ref_dir.exists():
        raise FileNotFoundError(
            f"Reference directory not found: {ref_dir}\n"
            f"Create it and add 2-3 reference images (ref_01.png, ref_02.png, etc.)"
        )
    return sorted([str(p) for p in ref_dir.glob("*.png")])


def capture_screenshots_from_godot(config: OptimizationConfig) -> list[str]:
    """Call Godot to capture screenshots."""
    response = requests.post(f"{config.godot_url}/capture")
    if response.status_code != 200:
        raise RuntimeError(f"Failed to capture screenshots: {response.text}")
    return response.json()["paths"]


def apply_params_to_godot(config: OptimizationConfig, params: dict):
    """Send parameters to Godot."""
    response = requests.post(
        f"{config.godot_url}/apply_params",
        json=params
    )
    if response.status_code != 200:
        raise RuntimeError(f"Failed to apply params: {response.text}")


def run_optimization(config: OptimizationConfig) -> dict:
    """
    Main optimization loop.
    Returns: Final optimized parameters
    """
    state = OptimizationState()
    reference_images = get_reference_images(config)
    
    # Start from existing preset
    current_params = load_preset_as_baseline(config.tree_type)
    state.best_params = current_params.copy()
    
    print(f"Starting optimization: {config.tree_type} ({config.style})")
    print(f"References: {reference_images}")
    print(f"Max iterations: {config.max_iterations}")
    
    while state.iteration < config.max_iterations:
        state.iteration += 1
        print(f"\n=== Iteration {state.iteration} ===")
        
        # Apply current parameters
        apply_params_to_godot(config, current_params)
        
        # Capture screenshots
        generated_images = capture_screenshots_from_godot(config)
        print(f"Captured {len(generated_images)} screenshots")
        
        # VLM evaluation
        evaluation = evaluate_tree(
            generated_images=generated_images,
            reference_images=reference_images,
            style=config.style,
            tree_type=config.tree_type
        )
        
        score = evaluation.get("overall_score", 0)
        print(f"Score: {score}/10")
        print(f"Issues: {evaluation.get('issues', [])}")
        
        # Track history
        state.history.append({
            "iteration": state.iteration,
            "score": score,
            "params": current_params.copy(),
            "evaluation": evaluation
        })
        
        # Check termination conditions
        if evaluation.get("matches_well", False):
            print("\n✅ VLM indicates tree matches reference well!")
            if state.iteration >= config.min_iterations:
                state.best_params = current_params.copy()
                state.best_score = score
                break
        
        # Update best
        if score > state.best_score:
            state.best_score = score
            state.best_params = current_params.copy()
            state.no_improvement_count = 0
            print(f"New best score: {score}")
        else:
            state.no_improvement_count += 1
        
        # Early stopping
        if score >= config.early_stop_threshold and state.iteration >= config.min_iterations:
            print(f"\n✅ Reached target score threshold ({config.early_stop_threshold})")
            break
        
        if state.no_improvement_count >= config.patience:
            print(f"\n⚠️ No improvement for {config.patience} iterations, stopping")
            break
        
        # Mutate parameters based on VLM suggestions
        suggestions = evaluation.get("parameter_suggestions", {})
        if suggestions:
            print(f"Applying suggestions: {list(suggestions.keys())}")
            current_params = mutate_parameters(
                current_params, 
                suggestions,
                exploration_rate=0.15
            )
        else:
            # Random exploration if no suggestions
            print("No suggestions, random exploration")
            current_params = mutate_parameters(
                current_params,
                {},
                exploration_rate=0.5
            )
    
    # Save results
    results = {
        "config": asdict(config),
        "final_params": state.best_params,
        "best_score": state.best_score,
        "total_iterations": state.iteration,
        "history": state.history
    }
    
    output_path = f"optimization_results_{config.tree_type}_{config.style}.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_path}")
    
    return state.best_params


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="PixyTree VLM Optimizer")
    parser.add_argument("--tree-type", default="oak", help="Tree type to optimize")
    parser.add_argument("--style", default="low_poly", help="Target art style")
    parser.add_argument("--max-iter", type=int, default=50, help="Max iterations")
    parser.add_argument("--reference-dir", default="./references", help="Reference images directory")
    
    args = parser.parse_args()
    
    config = OptimizationConfig(
        tree_type=args.tree_type,
        style=args.style,
        max_iterations=args.max_iter,
        reference_dir=args.reference_dir
    )
    
    final_params = run_optimization(config)
    print(f"\nFinal parameters:\n{json.dumps(final_params, indent=2)}")
```

---

## Rendering Configuration Auto-Tuning

The skill self-tunes rendering based on target style:

```python
RENDER_CONFIGS = {
    "low_poly": {
        "resolution": (640, 480),
        "antialiasing": "none",
        "shadows": "hard",
        "ambient_occlusion": False,
        "post_process": ["outline"],
        "background": "solid_color",
    },
    "pixel_art": {
        "resolution": (320, 180),
        "antialiasing": "none", 
        "shadows": "none",
        "ambient_occlusion": False,
        "post_process": ["pixelate", "dither", "color_quantize"],
        "background": "solid_color",
    },
    "realistic": {
        "resolution": (1920, 1080),
        "antialiasing": "msaa_4x",
        "shadows": "soft",
        "ambient_occlusion": True,
        "post_process": ["bloom", "tonemap"],
        "background": "hdri",
    },
    "cartoon": {
        "resolution": (1280, 720),
        "antialiasing": "fxaa",
        "shadows": "hard",
        "ambient_occlusion": False,
        "post_process": ["outline", "cel_shade"],
        "background": "gradient",
    },
    "anime": {
        "resolution": (1280, 720),
        "antialiasing": "fxaa",
        "shadows": "soft",
        "ambient_occlusion": False,
        "post_process": ["bloom_soft", "vignette"],
        "background": "gradient",
    }
}

def get_render_config(style: str) -> dict:
    """Get rendering configuration for target style."""
    return RENDER_CONFIGS.get(style, RENDER_CONFIGS["low_poly"])
```

---

## Output: Updating Rust Presets

After optimization, update the Rust preset:

```python
def generate_rust_preset(params: dict, tree_type: str, style: str) -> str:
    """Generate Rust code for TreePresetValues struct."""
    
    # Map Python keys to Rust struct fields
    rust_code = f'''
    /// {tree_type.title()} ({style.replace("_", " ").title()} style)
    /// Auto-generated by VLM optimizer
    pub fn {tree_type}_{style}() -> Self {{
        Self {{
'''
    
    for key, value in sorted(params.items()):
        if isinstance(value, bool):
            rust_val = "true" if value else "false"
        elif isinstance(value, float):
            rust_val = f"{value:.4f}"
        elif isinstance(value, int):
            rust_val = str(value)
        else:
            continue
        rust_code += f"            {key}: {rust_val},\n"
    
    rust_code += '''            // Add remaining fields with defaults
            ..Default::default()
        }
    }
'''
    return rust_code
```

---

## Quick Start

1. **Setup references:**
```bash
mkdir -p references/low_poly_oak
# Download 2-3 reference images of low-poly oak trees
```

2. **Start Godot in headless mode:**
```bash
cd /Users/ladvien/pixy_tree/godot
godot --headless --script res://scripts/optimization_server.gd
```

3. **Run optimizer:**
```bash
cd /Users/ladvien/skillz/pixy-tree-optimizer
python pixy_tree_optimizer.py --tree-type=oak --style=low_poly --max-iter=50
```

4. **Monitor progress:**
- Check `optimization_results_oak_low_poly.json` for history
- Screenshots saved in Godot's `user://optimization_screenshots/`

5. **Apply results:**
- Copy final parameters to `rust/src/tree_preset.rs`
- Or use generated Rust code from `generate_rust_preset()`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| VLM returns garbage JSON | Check OLLAMA_API_KEY, try simpler prompt |
| Screenshots are black | Ensure camera angles point at tree, check lighting |
| No improvement after many iterations | Increase exploration_rate, check reference image quality |
| Godot connection refused | Start optimization_server.gd first |
| Parameters out of range | Check PARAM_BOUNDS, VLM may suggest invalid values |

---

## Files Structure

```
pixy-tree-optimizer/
├── SKILL.md                    # This file
├── pixy_tree_optimizer.py      # Main orchestrator
├── evaluate.py                 # VLM evaluation functions
├── mutate.py                   # Parameter mutation logic
├── render_config.py            # Style-based render settings
├── godot_scripts/
│   ├── tree_optimizer.gd       # Godot screenshot capture
│   └── optimization_server.gd  # Headless HTTP server
└── references/
    ├── low_poly_oak/
    │   ├── ref_01.png
    │   └── ref_02.png
    └── pixel_art_pine/
        └── ...
```

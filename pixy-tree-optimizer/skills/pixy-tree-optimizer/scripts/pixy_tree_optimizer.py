#!/usr/bin/env python3
"""
pixy_tree_optimizer.py - Main optimization orchestrator
VLM-guided hill climbing for PixyTree preset optimization
"""

import json
import time
import argparse
import os
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import Optional
import requests

from evaluate import evaluate_tree
from mutate import mutate_parameters, random_mutation, PARAM_BOUNDS
from render_config import get_render_config, generate_godot_config


@dataclass
class OptimizationConfig:
    tree_type: str = "oak"
    style: str = "low_poly"
    max_iterations: int = 50
    min_iterations: int = 5
    reference_dir: str = "./references"
    godot_url: str = "http://localhost:8765"
    early_stop_threshold: float = 8.0
    patience: int = 10
    exploration_rate: float = 0.2
    mutation_strength: float = 1.0
    output_dir: str = "./results"


@dataclass 
class OptimizationState:
    iteration: int = 0
    best_score: float = 0.0
    best_params: dict = field(default_factory=dict)
    no_improvement_count: int = 0
    history: list = field(default_factory=list)


# Baseline presets matching PixyTree's Rust TreePresetValues
BASELINE_PRESETS = {
    "oak": {
        "trunk_height": 6.0,
        "trunk_radius": 0.6,
        "trunk_taper": 0.3,
        "trunk_taper_curve": 0.3,
        "trunk_flare": 1.2,
        "trunk_randomness": 0.1,
        "radial_segments": 8,
        "height_segments": 6,
        "branch_start": 0.35,
        "branch_end": 0.85,
        "branch_density": 2.0,
        "branch_length": 0.65,
        "branch_angle": 55.0,
        "branch_radius_ratio": 0.35,
        "branch_taper": 0.7,
        "phyllotaxis_angle": 137.5,
        "branch_randomness": 0.2,
        "up_attraction": 0.15,
        "branch_recursion": 2,
        "sub_branch_count": 3,
        "sub_branch_scale": 0.6,
        "apical_dominance": 0.3,
        "gravity_strength": 0.3,
        "stiffness": 0.6,
        "crown_influence": 0.9,
        "crown_shape": 0,  # Spherical
        "leaf_style": 0, "foliage_placement": 1, "leaf_orientation": 0,
        "foliage_density": 4.0, "cluster_size": 5, "leaf_size": 0.35,
        "leaf_size_variation": 0.15, "foliage_radius_threshold": 0.2,
        "foliage_height_falloff": 0.25, "leaf_droop": 0.15, "leaf_rotation_variation": 0.6,
    },
    "pine": {
        "trunk_height": 8.0,
        "trunk_radius": 0.4,
        "trunk_taper": 0.15,
        "trunk_taper_curve": 0.1,
        "trunk_flare": 1.1,
        "trunk_randomness": 0.05,
        "radial_segments": 6,
        "height_segments": 8,
        "branch_start": 0.2,
        "branch_end": 0.95,
        "branch_density": 3.0,
        "branch_length": 0.5,
        "branch_angle": 75.0,
        "branch_radius_ratio": 0.25,
        "branch_taper": 0.6,
        "phyllotaxis_angle": 90.0,
        "branch_randomness": 0.1,
        "up_attraction": -0.2,
        "branch_recursion": 1,
        "sub_branch_count": 2,
        "sub_branch_scale": 0.5,
        "apical_dominance": 0.8,
        "gravity_strength": 0.4,
        "stiffness": 0.7,
        "crown_influence": 0.7,
        "crown_shape": 1,  # Conical
        "leaf_style": 4, "foliage_placement": 1, "leaf_orientation": 1,
        "foliage_density": 6.0, "cluster_size": 3, "leaf_size": 0.15,
        "leaf_size_variation": 0.1, "foliage_radius_threshold": 0.1,
        "foliage_height_falloff": 0.1, "leaf_droop": 0.3, "leaf_rotation_variation": 0.3,
    },
    "willow": {
        "trunk_height": 7.0,
        "trunk_radius": 0.7,
        "trunk_taper": 0.25,
        "trunk_taper_curve": 0.2,
        "trunk_flare": 1.3,
        "trunk_randomness": 0.15,
        "radial_segments": 8,
        "height_segments": 5,
        "branch_start": 0.4,
        "branch_end": 0.8,
        "branch_density": 2.5,
        "branch_length": 0.9,
        "branch_angle": 45.0,
        "branch_radius_ratio": 0.3,
        "branch_taper": 0.5,
        "phyllotaxis_angle": 137.5,
        "branch_randomness": 0.25,
        "up_attraction": -0.6,
        "branch_recursion": 3,
        "sub_branch_count": 4,
        "sub_branch_scale": 0.7,
        "apical_dominance": 0.2,
        "gravity_strength": 0.8,
        "stiffness": 0.2,
        "crown_influence": 0.6,
        "crown_shape": 7,  # Umbrella
        "leaf_style": 1, "foliage_placement": 0, "leaf_orientation": 2,
        "foliage_density": 5.0, "cluster_size": 2, "leaf_size": 0.2,
        "leaf_size_variation": 0.2, "foliage_radius_threshold": 0.15,
        "foliage_height_falloff": 0.4, "leaf_droop": 0.8, "leaf_rotation_variation": 0.5,
    },
    "birch": {
        "trunk_height": 7.0,
        "trunk_radius": 0.25,
        "trunk_taper": 0.2,
        "trunk_taper_curve": 0.15,
        "trunk_flare": 1.05,
        "trunk_randomness": 0.1,
        "radial_segments": 6,
        "height_segments": 8,
        "branch_start": 0.3,
        "branch_end": 0.9,
        "branch_density": 2.0,
        "branch_length": 0.5,
        "branch_angle": 50.0,
        "branch_radius_ratio": 0.2,
        "branch_taper": 0.65,
        "phyllotaxis_angle": 137.5,
        "branch_randomness": 0.2,
        "up_attraction": 0.3,
        "branch_recursion": 2,
        "sub_branch_count": 2,
        "sub_branch_scale": 0.5,
        "apical_dominance": 0.5,
        "gravity_strength": 0.2,
        "stiffness": 0.7,
        "crown_influence": 0.8,
        "crown_shape": 2,  # Hemispherical
        "leaf_style": 0, "foliage_placement": 0, "leaf_orientation": 0,
        "foliage_density": 3.5, "cluster_size": 4, "leaf_size": 0.25,
        "leaf_size_variation": 0.2, "foliage_radius_threshold": 0.15,
        "foliage_height_falloff": 0.3, "leaf_droop": 0.1, "leaf_rotation_variation": 0.7,
    },
    "dead": {
        "trunk_height": 5.0,
        "trunk_radius": 0.5,
        "trunk_taper": 0.35,
        "trunk_taper_curve": 0.4,
        "trunk_flare": 1.3,
        "trunk_randomness": 0.3,
        "radial_segments": 6,
        "height_segments": 4,
        "branch_start": 0.25,
        "branch_end": 0.75,
        "branch_density": 1.0,
        "branch_length": 0.4,
        "branch_angle": 65.0,
        "branch_radius_ratio": 0.4,
        "branch_taper": 0.8,
        "phyllotaxis_angle": 180.0,
        "branch_randomness": 0.4,
        "up_attraction": 0.0,
        "branch_recursion": 2,
        "sub_branch_count": 1,
        "sub_branch_scale": 0.4,
        "apical_dominance": 0.1,
        "gravity_strength": 0.5,
        "stiffness": 0.3,
        "crown_influence": 0.3,
        "crown_shape": 8,  # Irregular
        "break_chance": 0.3,
        "trunk_twist": 15.0,
        "branch_twist": 20.0,
        "leaf_style": 0, "foliage_placement": 0, "leaf_orientation": 0,
        "foliage_density": 0.5, "cluster_size": 1, "leaf_size": 0.1,
        "leaf_size_variation": 0.0, "foliage_radius_threshold": 1.0,
        "foliage_height_falloff": 0.0, "leaf_droop": 0.0, "leaf_rotation_variation": 0.0,
    },
}


STYLE_OVERRIDES = {
    "low_poly": {
        "radial_segments": 5,
        "height_segments": 4,
        "leaf_style": 2,           # ClusterSphere for rounded faceted clusters
        "foliage_placement": 2,    # TipClusters
        "leaf_size": 1.2,          # Large for chunky look (octahedrons ~0.48 units)
        "cluster_size": 8,         # Enough to merge into solid blobs
        "foliage_density": 3.5,
        "branch_recursion": 1,
        "sub_branch_count": 2,
    },
}


def load_baseline_preset(tree_type: str, style: str = "") -> dict:
    """Load existing PixyTree preset as starting point, with style overrides."""
    if tree_type in BASELINE_PRESETS:
        params = BASELINE_PRESETS[tree_type].copy()
    else:
        print(f"Unknown tree type '{tree_type}', using oak as baseline")
        params = BASELINE_PRESETS["oak"].copy()

    if style in STYLE_OVERRIDES:
        params.update(STYLE_OVERRIDES[style])

    return params


def get_reference_images(config: OptimizationConfig) -> list[str]:
    """Get paths to reference images for the style/type combo."""
    ref_dir = Path(config.reference_dir) / f"{config.style}_{config.tree_type}"
    
    if not ref_dir.exists():
        # Try alternative naming
        alt_dir = Path(config.reference_dir) / f"{config.tree_type}_{config.style}"
        if alt_dir.exists():
            ref_dir = alt_dir
        else:
            raise FileNotFoundError(
                f"Reference directory not found: {ref_dir}\n"
                f"Create it and add 2-3 reference images (ref_01.png, ref_02.png, etc.)\n"
                f"Or use any image filenames (.png, .jpg)"
            )
    
    images = []
    for ext in ["*.png", "*.jpg", "*.jpeg", "*.webp"]:
        images.extend([str(p) for p in ref_dir.glob(ext)])
    
    if not images:
        raise FileNotFoundError(f"No images found in {ref_dir}")
    
    return sorted(images)[:3]  # Max 3 reference images


def capture_screenshots_from_godot(config: OptimizationConfig) -> list[str]:
    """Request screenshot capture from Godot."""
    try:
        response = requests.post(
            f"{config.godot_url}/capture",
            timeout=30
        )
        if response.status_code != 200:
            raise RuntimeError(f"Capture failed: {response.text}")
        return response.json().get("paths", [])
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            f"Cannot connect to Godot at {config.godot_url}\n"
            "Start Godot with: godot --headless --script res://scripts/optimization_server.gd"
        )


def apply_params_to_godot(config: OptimizationConfig, params: dict):
    """Send parameters to Godot."""
    try:
        response = requests.post(
            f"{config.godot_url}/apply_params",
            json=params,
            timeout=10
        )
        if response.status_code != 200:
            print(f"Warning: apply_params returned {response.status_code}")
    except requests.exceptions.ConnectionError:
        raise RuntimeError(f"Cannot connect to Godot at {config.godot_url}")


def apply_render_config_to_godot(config: OptimizationConfig):
    """Send render configuration to Godot."""
    render_config = generate_godot_config(config.style)
    try:
        response = requests.post(
            f"{config.godot_url}/apply_render_config",
            json=render_config,
            timeout=10
        )
        if response.status_code != 200:
            print(f"Warning: render config not applied: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Warning: Could not apply render config")


def save_results(config: OptimizationConfig, state: OptimizationState):
    """Save optimization results to JSON."""
    Path(config.output_dir).mkdir(parents=True, exist_ok=True)
    
    output_path = Path(config.output_dir) / f"optimization_{config.tree_type}_{config.style}.json"
    
    results = {
        "config": {
            "tree_type": config.tree_type,
            "style": config.style,
            "max_iterations": config.max_iterations,
            "early_stop_threshold": config.early_stop_threshold,
        },
        "final_params": state.best_params,
        "best_score": state.best_score,
        "total_iterations": state.iteration,
        "history": state.history,
    }
    
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to: {output_path}")
    return output_path


def generate_rust_preset(params: dict, tree_type: str, style: str) -> str:
    """Generate Rust code for TreePresetValues struct."""
    func_name = f"{tree_type}_{style}".lower().replace("-", "_")
    
    rust_code = f'''    /// {tree_type.title()} tree optimized for {style.replace("_", " ").title()} style
    /// Auto-generated by VLM optimizer
    pub fn {func_name}() -> Self {{
        Self {{
'''
    
    # Sort params for consistent output
    for key in sorted(params.keys()):
        value = params[key]
        if isinstance(value, bool):
            rust_val = "true" if value else "false"
        elif isinstance(value, float):
            rust_val = f"{value:.4f}"
        elif isinstance(value, int):
            rust_val = str(value)
        else:
            continue
        rust_code += f"            {key}: {rust_val},\n"
    
    rust_code += '''            ..Default::default()
        }
    }
'''
    return rust_code


def run_optimization(config: OptimizationConfig) -> dict:
    """
    Main optimization loop.
    
    Returns: Final optimized parameters
    """
    state = OptimizationState()
    
    # Load reference images
    try:
        reference_images = get_reference_images(config)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return {}
    
    # Start from baseline preset
    current_params = load_baseline_preset(config.tree_type, config.style)
    state.best_params = current_params.copy()
    
    print(f"\n{'='*60}")
    print(f"PixyTree VLM Optimizer")
    print(f"{'='*60}")
    print(f"Tree type: {config.tree_type}")
    print(f"Target style: {config.style}")
    print(f"References: {reference_images}")
    print(f"Max iterations: {config.max_iterations}")
    print(f"Early stop threshold: {config.early_stop_threshold}")
    print(f"Patience: {config.patience}")
    print(f"{'='*60}\n")
    
    # Apply render configuration
    try:
        apply_render_config_to_godot(config)
    except Exception as e:
        print(f"Warning: Could not apply render config: {e}")
    
    while state.iteration < config.max_iterations:
        state.iteration += 1
        print(f"\n--- Iteration {state.iteration}/{config.max_iterations} ---")
        
        # Apply current parameters to Godot
        try:
            apply_params_to_godot(config, current_params)
        except RuntimeError as e:
            print(f"ERROR: {e}")
            break
        
        # Wait for Godot to regenerate tree
        time.sleep(0.5)
        
        # Capture screenshots
        try:
            generated_images = capture_screenshots_from_godot(config)
            print(f"Captured {len(generated_images)} screenshots")
        except RuntimeError as e:
            print(f"ERROR: {e}")
            break
        
        if not generated_images:
            print("No screenshots captured, using random mutation")
            current_params = random_mutation(current_params)
            continue
        
        # VLM evaluation
        print("Evaluating with VLM...")
        evaluation = evaluate_tree(
            generated_images=generated_images,
            reference_images=reference_images,
            style=config.style,
            tree_type=config.tree_type
        )
        
        # Skip failed VLM evaluations entirely
        if evaluation.get("vlm_failed", False):
            print("VLM unavailable, skipping iteration (keeping current params)")
            time.sleep(10)  # Back off before retrying
            continue

        score = evaluation.get("overall_score", 0)
        scores = evaluation.get("scores", {})
        issues = evaluation.get("issues", [])
        suggestions = evaluation.get("parameter_suggestions", {})

        print(f"Score: {score:.1f}/10")
        print(f"  Silhouette: {scores.get('silhouette', '?')}")
        print(f"  Branching:  {scores.get('branching', '?')}")
        print(f"  Trunk:      {scores.get('trunk', '?')}")
        print(f"  Foliage:    {scores.get('foliage', '?')}")
        print(f"  Style:      {scores.get('style_match', '?')}")

        if issues:
            print(f"Issues: {issues[:3]}")
        
        # Track history
        state.history.append({
            "iteration": state.iteration,
            "score": score,
            "scores": scores,
            "params": current_params.copy(),
            "issues": issues[:3],
            "suggestions": list(suggestions.keys())[:5],
        })
        
        # Check termination conditions
        if evaluation.get("matches_well", False):
            print(f"\n✅ VLM confirms tree matches reference well!")
            if state.iteration >= config.min_iterations:
                state.best_params = current_params.copy()
                state.best_score = score
                break
        
        # Update best
        if score > state.best_score:
            state.best_score = score
            state.best_params = current_params.copy()
            state.no_improvement_count = 0
            print(f"📈 New best score: {score:.1f}")
        else:
            state.no_improvement_count += 1
        
        # Early stopping on threshold
        if score >= config.early_stop_threshold and state.iteration >= config.min_iterations:
            print(f"\n✅ Reached target threshold ({config.early_stop_threshold})")
            break
        
        # Patience exhausted
        if state.no_improvement_count >= config.patience:
            print(f"\n⚠️ No improvement for {config.patience} iterations")
            break
        
        # Mutate parameters
        if suggestions:
            print(f"Adjusting: {list(suggestions.keys())[:5]}")
            current_params = mutate_parameters(
                current_params,
                suggestions,
                exploration_rate=config.exploration_rate,
                mutation_strength=config.mutation_strength
            )
        else:
            print("No suggestions, random exploration")
            current_params = random_mutation(current_params)
    
    # Save results
    print(f"\n{'='*60}")
    print(f"Optimization complete!")
    print(f"Best score: {state.best_score:.1f}/10")
    print(f"Total iterations: {state.iteration}")
    print(f"{'='*60}\n")
    
    save_results(config, state)
    
    # Generate Rust code
    rust_code = generate_rust_preset(state.best_params, config.tree_type, config.style)
    rust_path = Path(config.output_dir) / f"preset_{config.tree_type}_{config.style}.rs"
    with open(rust_path, "w") as f:
        f.write(rust_code)
    print(f"Rust preset saved to: {rust_path}")
    
    return state.best_params


def main():
    parser = argparse.ArgumentParser(
        description="PixyTree VLM Optimizer - Automated tree preset optimization"
    )
    parser.add_argument(
        "--tree-type", "-t",
        default="oak",
        help="Tree type to optimize (oak, pine, willow, birch, dead, etc.)"
    )
    parser.add_argument(
        "--style", "-s",
        default="low_poly",
        choices=["low_poly", "realistic", "cartoon", "pixel_art", "anime", "dead"],
        help="Target art style"
    )
    parser.add_argument(
        "--max-iter", "-i",
        type=int,
        default=50,
        help="Maximum iterations (default: 50)"
    )
    parser.add_argument(
        "--reference-dir", "-r",
        default="./references",
        help="Directory containing reference images"
    )
    parser.add_argument(
        "--godot-url", "-g",
        default="http://localhost:8765",
        help="Godot HTTP server URL"
    )
    parser.add_argument(
        "--threshold", "-T",
        type=float,
        default=8.0,
        help="Early stop score threshold (default: 8.0)"
    )
    parser.add_argument(
        "--patience", "-p",
        type=int,
        default=10,
        help="Stop after N iterations without improvement (default: 10)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="./results",
        help="Output directory for results"
    )
    
    args = parser.parse_args()
    
    # Validate OLLAMA_API_KEY
    if not os.environ.get("OLLAMA_API_KEY"):
        print("WARNING: OLLAMA_API_KEY not set. Get one at https://ollama.com/settings/keys")
    
    config = OptimizationConfig(
        tree_type=args.tree_type,
        style=args.style,
        max_iterations=args.max_iter,
        reference_dir=args.reference_dir,
        godot_url=args.godot_url,
        early_stop_threshold=args.threshold,
        patience=args.patience,
        output_dir=args.output_dir,
    )
    
    final_params = run_optimization(config)
    
    if final_params:
        print("\nFinal parameters:")
        print(json.dumps(final_params, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

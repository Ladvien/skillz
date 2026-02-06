#!/usr/bin/env python3
"""
mutate.py - Parameter mutation logic for PixyTree optimization
VLM-guided hill climbing with exploration
"""

import random
from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class ParameterBounds:
    min_val: Union[int, float]
    max_val: Union[int, float]
    step: float = 0.05  # Mutation step as fraction of range
    is_integer: bool = False
    

# Complete parameter bounds matching PixyTree's Rust structs
PARAM_BOUNDS = {
    # ========== TRUNK (11 params) ==========
    "trunk_height": ParameterBounds(1.0, 25.0, 0.1),
    "trunk_radius": ParameterBounds(0.1, 2.0, 0.05),
    "trunk_taper": ParameterBounds(0.0, 1.0, 0.05),
    "trunk_taper_curve": ParameterBounds(0.0, 1.0, 0.05),
    "trunk_flare": ParameterBounds(1.0, 2.0, 0.05),
    "trunk_randomness": ParameterBounds(0.0, 0.5, 0.02),
    "root_flare_count": ParameterBounds(0, 8, 1, is_integer=True),
    "root_flare_spread": ParameterBounds(0.0, 1.0, 0.05),
    "root_flare_height": ParameterBounds(0.0, 0.5, 0.02),
    "radial_segments": ParameterBounds(4, 16, 1, is_integer=True),
    "height_segments": ParameterBounds(2, 12, 1, is_integer=True),
    
    # ========== TRUNK TERMINATION (4 params) ==========
    # trunk_termination is enum: FlatCap=0, PointedTip=1, LeaderBranch=2
    "trunk_termination": ParameterBounds(0, 2, 1, is_integer=True),
    "leader_length": ParameterBounds(0.0, 0.5, 0.02),
    "leader_taper": ParameterBounds(0.0, 0.3, 0.02),
    # leader_has_branches is bool
    
    # ========== BRANCHES (19 params) ==========
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
    "branch_recursion": ParameterBounds(0, 4, 1, is_integer=True),
    "sub_branch_count": ParameterBounds(0, 5, 1, is_integer=True),
    "sub_branch_scale": ParameterBounds(0.3, 0.8, 0.05),
    "branch_length_variation": ParameterBounds(0.0, 0.5, 0.02),
    "sub_branch_position_bias": ParameterBounds(-0.5, 0.5, 0.02),
    "apical_dominance": ParameterBounds(0.0, 1.0, 0.05),
    "branch_flatness": ParameterBounds(0.0, 1.0, 0.05),
    "branch_angle_curve": ParameterBounds(-0.5, 0.5, 0.02),
    "crown_angle_variation": ParameterBounds(-0.5, 0.5, 0.02),
    
    # ========== TWIST & PHYSICS (6 params) ==========
    "trunk_twist": ParameterBounds(0.0, 45.0, 2.0),
    "branch_twist": ParameterBounds(0.0, 30.0, 2.0),
    "gravity_strength": ParameterBounds(0.0, 1.0, 0.05),
    "stiffness": ParameterBounds(0.0, 1.0, 0.05),
    "break_chance": ParameterBounds(0.0, 0.5, 0.02),
    
    # ========== SPLITTING (5 params) ==========
    # split_enabled is bool
    "split_probability": ParameterBounds(0.0, 1.0, 0.05),
    "split_angle": ParameterBounds(15.0, 60.0, 2.0),
    "split_position": ParameterBounds(0.3, 0.7, 0.02),
    "split_radius_threshold": ParameterBounds(0.03, 0.2, 0.01),
    
    # ========== CROWN (3 params) ==========
    # crown_shape is enum: Spherical=0, Conical=1, Hemispherical=2, Cylindrical=3,
    #   TaperedCylindrical=4, Flame=5, Spreading=6, Umbrella=7, Irregular=8
    "crown_shape": ParameterBounds(0, 8, 1, is_integer=True),
    "crown_influence": ParameterBounds(0.0, 1.0, 0.05),
    "crown_radius": ParameterBounds(0.5, 3.0, 0.1),

    # ========== FOLIAGE (11 params) ==========
    "leaf_style": ParameterBounds(0, 5, 1, is_integer=True),        # 0=CrossedPlanes 1=SingleQuad 2=ClusterSphere 3=StarBurst 4=NeedleCluster 5=Icosphere
    "foliage_placement": ParameterBounds(0, 2, 1, is_integer=True), # 0=TerminalBranches 1=AllBranches 2=TipClusters
    "leaf_orientation": ParameterBounds(0, 3, 1, is_integer=True),  # 0=RadialOutward 1=FollowBranch 2=RandomUpward 3=HorizontalSpread
    "foliage_density": ParameterBounds(0.5, 10.0, 0.1),
    "cluster_size": ParameterBounds(1, 12, 1, is_integer=True),
    "leaf_size": ParameterBounds(0.05, 2.0, 0.05),
    "leaf_size_variation": ParameterBounds(0.0, 0.5, 0.02),
    "foliage_radius_threshold": ParameterBounds(0.0, 1.0, 0.05),
    "foliage_height_falloff": ParameterBounds(0.0, 1.0, 0.05),
    "leaf_droop": ParameterBounds(0.0, 1.0, 0.05),
    "leaf_rotation_variation": ParameterBounds(0.0, 1.0, 0.05),

    # ========== FLOOR & COLLAR (4 params) ==========
    # floor_avoidance is bool
    "floor_level": ParameterBounds(-1.0, 1.0, 0.05),
    # branch_collar_enabled is bool
    "branch_collar_length": ParameterBounds(1.0, 2.0, 0.05),
    
    # ========== L-SYSTEM GROWTH (16 params) ==========
    "grow_threshold": ParameterBounds(0.1, 0.6, 0.02),
    "cut_threshold": ParameterBounds(0.05, 0.3, 0.02),
    "split_threshold": ParameterBounds(0.3, 1.0, 0.05),
    "flower_threshold": ParameterBounds(0.05, 0.3, 0.02),
    "lsystem_apical_dominance": ParameterBounds(0.2, 1.0, 0.05),
    "lateral_start": ParameterBounds(0.0, 0.5, 0.02),
    "lateral_end": ParameterBounds(0.5, 1.0, 0.02),
    "lateral_density": ParameterBounds(0.5, 4.0, 0.1),
    "lateral_activation": ParameterBounds(0.2, 0.6, 0.02),
    "lateral_angle": ParameterBounds(20.0, 80.0, 2.0),
    "iterations": ParameterBounds(3, 8, 1, is_integer=True),
    "lsystem_branch_length": ParameterBounds(0.2, 0.8, 0.02),
    "gravitropism": ParameterBounds(-0.3, 0.5, 0.02),
    "lsystem_randomness": ParameterBounds(0.0, 0.4, 0.02),
    "lsystem_gravity_strength": ParameterBounds(0.0, 0.5, 0.02),
    "lsystem_stiffness": ParameterBounds(0.2, 1.0, 0.05),
}


# Parameters grouped by visual impact for smarter mutation
HIGH_IMPACT_PARAMS = [
    "trunk_height", "trunk_radius", "trunk_taper",
    "branch_density", "branch_angle", "branch_length",
    "crown_influence", "crown_shape",
    "gravity_strength", "up_attraction",
    "branch_recursion", "sub_branch_count",
    "leaf_style", "foliage_placement", "leaf_size",
    "cluster_size", "foliage_density",
]

MEDIUM_IMPACT_PARAMS = [
    "branch_start", "branch_end",
    "phyllotaxis_angle", "apical_dominance",
    "trunk_flare", "branch_randomness",
    "sub_branch_scale", "stiffness",
    "foliage_radius_threshold", "foliage_height_falloff",
    "leaf_droop", "leaf_orientation",
]

LOW_IMPACT_PARAMS = [
    "trunk_randomness", "branch_twist", "trunk_twist",
    "root_flare_count", "radial_segments", "height_segments",
    "branch_collar_length", "leader_length",
    "leaf_size_variation", "leaf_rotation_variation",
]


# Parameters that are enums - raw numeric values mean "set to this"
ENUM_PARAMS = {
    "leaf_style", "foliage_placement", "leaf_orientation",
    "crown_shape", "trunk_termination", "preset",
}


def parse_suggestion(suggestion, param_name: str = "") -> tuple[str, float]:
    """
    Parse VLM suggestion into direction and magnitude.
    Returns: (direction, magnitude) where direction is "increase", "decrease", or "set"

    For enum parameters, raw numbers are always treated as "set to this value".
    For continuous parameters, raw numbers are treated as deltas.
    String prefixes like "set:", "+", "-" override defaults.
    """
    # Handle string suggestions with explicit prefixes
    if isinstance(suggestion, str):
        suggestion = suggestion.strip()

        # Explicit "set:N" format
        if suggestion.startswith("set:"):
            try:
                return ("set", float(suggestion[4:]))
            except ValueError:
                pass

        # Explicit delta format "+N" or "-N"
        if suggestion.startswith("+"):
            try:
                return ("increase", abs(float(suggestion)))
            except ValueError:
                pass
        if suggestion.startswith("-"):
            try:
                return ("decrease", abs(float(suggestion)))
            except ValueError:
                pass

        s = suggestion.lower()
        if "increase" in s or "more" in s or "higher" in s:
            words = s.split()
            for word in words:
                try:
                    mag = float(word.replace("%", "").replace("+", ""))
                    return ("increase", mag / 100 if mag > 1 else mag)
                except ValueError:
                    continue
            return ("increase", 1.0)

        elif "decrease" in s or "less" in s or "lower" in s or "reduce" in s:
            words = s.split()
            for word in words:
                try:
                    mag = float(word.replace("%", "").replace("-", ""))
                    return ("decrease", mag / 100 if mag > 1 else mag)
                except ValueError:
                    continue
            return ("decrease", 1.0)

        # Try to parse as a direct value
        try:
            val = float(suggestion)
            # For enums, always treat as "set"
            if param_name in ENUM_PARAMS:
                return ("set", val)
            # For continuous params, treat as delta
            if val > 0:
                return ("increase", abs(val))
            elif val < 0:
                return ("decrease", abs(val))
            return ("none", 0)
        except ValueError:
            pass

        return ("none", 0)

    # Handle numeric suggestions
    if isinstance(suggestion, (int, float)):
        # For enum parameters, raw numbers always mean "set to this value"
        if param_name in ENUM_PARAMS:
            return ("set", float(suggestion))

        # For continuous parameters, treat as delta
        if suggestion > 0:
            return ("increase", abs(suggestion))
        elif suggestion < 0:
            return ("decrease", abs(suggestion))
        else:
            return ("none", 0)

    return ("none", 0)


def mutate_single_param(
    param_name: str,
    current_value: Union[int, float],
    direction: str,
    magnitude: float,
    bounds: ParameterBounds
) -> Union[int, float]:
    """
    Apply a mutation to a single parameter.
    """
    param_range = bounds.max_val - bounds.min_val
    if bounds.is_integer:
        step_size = bounds.step * magnitude
    else:
        step_size = bounds.step * param_range * magnitude
    
    # Add some noise for exploration
    noise = random.gauss(0, step_size * 0.2)
    
    if direction == "increase":
        new_val = current_value + step_size + noise
    elif direction == "decrease":
        new_val = current_value - step_size + noise
    elif direction == "set":
        new_val = magnitude  # magnitude is the target value
    else:
        new_val = current_value
    
    # Clamp to bounds
    new_val = max(bounds.min_val, min(bounds.max_val, new_val))
    
    # Round integers
    if bounds.is_integer:
        new_val = int(round(new_val))
    
    return new_val


PARAM_ALIASES = {
    "foliage_cluster_size": "cluster_size",
    "foliage_leaf_size": "leaf_size",
    "foliage_style": "leaf_style",
    "leaf_geometry": "leaf_style",
    "leaf_placement": "foliage_placement",
}


# Style constraints: parameters that should NOT be mutated away from these values
# These are known-correct for the given art style
STYLE_CONSTRAINTS = {
    "low_poly": {
        "preset": 0,               # Custom - MUST be 0 or Godot preset overrides our params
        "leaf_style": 5,           # Icosphere - subdivided icosahedron for rounded low-poly blobs
        "foliage_placement": 2,    # TipClusters - rounded blobs at branch tips
        "radial_segments": 5,      # Low poly count
        "height_segments": 4,      # Low poly count
    },
    "realistic": {
        "leaf_style": 0,           # CrossedPlanes for realistic foliage
        "foliage_placement": 1,    # AllBranches for natural distribution
    },
    "cartoon": {
        "leaf_style": 2,           # ClusterSphere for bold shapes
        "foliage_placement": 2,    # TipClusters for exaggerated blobs
    },
    "pixel_art": {
        "leaf_style": 0,           # CrossedPlanes for blocky look
        "radial_segments": 4,      # Minimal segments
        "height_segments": 3,
    },
    "anime": {
        "leaf_style": 2,           # ClusterSphere for soft rounded shapes
        "foliage_placement": 2,    # TipClusters
    },
    "dead": {
        "foliage_density": 0.0,    # No foliage
    },
}


def mutate_parameters(
    current_params: dict,
    vlm_suggestions: dict,
    exploration_rate: float = 0.2,
    mutation_strength: float = 1.0,
    style: str = ""
) -> dict:
    """
    Apply VLM-suggested mutations with some random exploration.

    Args:
        current_params: Current parameter values
        vlm_suggestions: Dict of param_name -> suggestion from VLM
        exploration_rate: Probability of random mutation on unexplored params
        mutation_strength: Multiplier for mutation magnitude (0.5 = half step, 2.0 = double step)
        style: Target art style for constraint pinning

    Returns:
        New parameter dict with mutations applied
    """
    new_params = current_params.copy()
    mutated_params = set()
    constraints = STYLE_CONSTRAINTS.get(style, {})

    # Apply VLM suggestions
    for param_name, suggestion in vlm_suggestions.items():
        if param_name not in PARAM_BOUNDS:
            # Check explicit aliases first
            if param_name in PARAM_ALIASES:
                param_name = PARAM_ALIASES[param_name]
            else:
                # Fuzzy match fallback
                matching = [p for p in PARAM_BOUNDS if param_name.replace("_", "") in p.replace("_", "")]
                if matching:
                    param_name = matching[0]
                else:
                    continue

        # Skip constrained parameters unless VLM suggests the constrained value
        if param_name in constraints:
            direction, magnitude = parse_suggestion(suggestion, param_name)
            if direction == "set" and magnitude == constraints[param_name]:
                # VLM agrees with constraint, keep it
                new_params[param_name] = constraints[param_name]
            # Otherwise skip - don't mutate pinned params
            mutated_params.add(param_name)
            continue

        bounds = PARAM_BOUNDS[param_name]
        current_val = current_params.get(param_name)

        if current_val is None:
            # Initialize with midpoint
            current_val = (bounds.min_val + bounds.max_val) / 2

        direction, magnitude = parse_suggestion(suggestion, param_name)
        magnitude *= mutation_strength

        if direction != "none":
            new_params[param_name] = mutate_single_param(
                param_name, current_val, direction, magnitude, bounds
            )
            mutated_params.add(param_name)

    # Random exploration on high-impact params not touched by VLM
    if random.random() < exploration_rate:
        # Prefer high-impact params for exploration, exclude constrained
        candidates = [p for p in HIGH_IMPACT_PARAMS
                      if p not in mutated_params and p in PARAM_BOUNDS and p not in constraints]
        if not candidates:
            candidates = [p for p in PARAM_BOUNDS if p not in mutated_params and p not in constraints]

        if candidates:
            param = random.choice(candidates)
            bounds = PARAM_BOUNDS[param]
            current = current_params.get(param, (bounds.min_val + bounds.max_val) / 2)

            # Random direction
            direction = random.choice(["increase", "decrease"])
            magnitude = random.uniform(0.5, 1.5) * mutation_strength

            new_params[param] = mutate_single_param(
                param, current, direction, magnitude, bounds
            )

    # Enforce constraints as final step (safety net)
    for param_name, value in constraints.items():
        new_params[param_name] = value

    return new_params


def random_mutation(current_params: dict, num_mutations: int = 3, style: str = "") -> dict:
    """
    Apply random mutations to a few parameters.
    Used when VLM doesn't provide useful suggestions.
    """
    new_params = current_params.copy()
    constraints = STYLE_CONSTRAINTS.get(style, {})

    # Weight towards high-impact params, exclude constrained
    all_params = [p for p in HIGH_IMPACT_PARAMS * 3 + MEDIUM_IMPACT_PARAMS * 2 + LOW_IMPACT_PARAMS
                  if p not in constraints]
    params_to_mutate = random.sample(all_params, min(num_mutations, len(all_params)))

    for param in params_to_mutate:
        if param not in PARAM_BOUNDS:
            continue

        bounds = PARAM_BOUNDS[param]
        current = current_params.get(param, (bounds.min_val + bounds.max_val) / 2)

        direction = random.choice(["increase", "decrease"])
        magnitude = random.uniform(0.3, 1.2)

        new_params[param] = mutate_single_param(
            param, current, direction, magnitude, bounds
        )

    # Enforce constraints
    for param_name, value in constraints.items():
        new_params[param_name] = value

    return new_params


def get_param_info(param_name: str) -> Optional[dict]:
    """Get information about a parameter."""
    if param_name not in PARAM_BOUNDS:
        return None
    
    bounds = PARAM_BOUNDS[param_name]
    return {
        "name": param_name,
        "min": bounds.min_val,
        "max": bounds.max_val,
        "step": bounds.step,
        "is_integer": bounds.is_integer,
        "impact": (
            "high" if param_name in HIGH_IMPACT_PARAMS else
            "medium" if param_name in MEDIUM_IMPACT_PARAMS else
            "low"
        )
    }


def list_all_params() -> list[str]:
    """Get list of all tunable parameter names."""
    return sorted(PARAM_BOUNDS.keys())


if __name__ == "__main__":
    # Test mutation
    test_params = {
        "trunk_height": 6.0,
        "trunk_radius": 0.5,
        "branch_density": 2.0,
        "branch_angle": 45.0,
    }

    test_suggestions = {
        "trunk_height": "increase by 20%",
        "branch_density": -0.3,
        "branch_angle": "decrease",
    }

    new_params = mutate_parameters(test_params, test_suggestions)

    print("Original params:")
    for k, v in test_params.items():
        print(f"  {k}: {v}")

    print("\nSuggestions:")
    for k, v in test_suggestions.items():
        print(f"  {k}: {v}")

    print("\nMutated params:")
    for k, v in new_params.items():
        if k in test_params:
            delta = v - test_params[k]
            print(f"  {k}: {v:.3f} (delta: {delta:+.3f})")
        else:
            print(f"  {k}: {v:.3f} (new)")

    # Test integer parameter mutation (regression test for oscillation bug)
    print("\n--- Integer mutation tests ---")
    random.seed(42)  # Deterministic for testing
    int_tests = [
        ("leaf_style", 2, "increase", 1.0, 3),
        ("cluster_size", 5, "increase", 1.0, 6),
        ("branch_recursion", 1, "decrease", 1.0, 0),
        ("radial_segments", 8, "increase", 1.0, 9),
        ("crown_shape", 4, "decrease", 1.0, 3),
    ]
    all_passed = True
    for param, current, direction, magnitude, expected in int_tests:
        random.seed(42)
        bounds = PARAM_BOUNDS[param]
        result = mutate_single_param(param, current, direction, magnitude, bounds)
        status = "PASS" if result == expected else "FAIL"
        if result != expected:
            all_passed = False
        print(f"  {status}: {param}={current} {direction} -> {result} (expected {expected})")

    if all_passed:
        print("All integer mutation tests passed!")
    else:
        print("WARNING: Some integer mutation tests failed!")

    # Test enum "set" behavior (regression test for set-vs-delta bug)
    print("\n--- Enum set-vs-delta tests ---")
    enum_tests = [
        # (param_name, suggestion_value, expected_direction, expected_magnitude)
        ("leaf_style", 2, "set", 2.0),      # raw int for enum -> set
        ("leaf_style", "set:2", "set", 2.0), # explicit set prefix
        ("foliage_placement", 0, "set", 0.0),# raw 0 for enum -> set to 0
        ("crown_shape", 3, "set", 3.0),      # raw int for enum -> set
        ("trunk_height", 2.0, "increase", 2.0),  # raw float for non-enum -> delta
        ("trunk_height", -0.5, "decrease", 0.5),  # negative for non-enum -> decrease
        ("leaf_style", "increase", "increase", 1.0),  # explicit direction still works
    ]
    all_passed = True
    for param, suggestion, exp_dir, exp_mag in enum_tests:
        got_dir, got_mag = parse_suggestion(suggestion, param)
        ok = got_dir == exp_dir and abs(got_mag - exp_mag) < 0.01
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_passed = False
        print(f"  {status}: parse_suggestion({suggestion!r}, '{param}') -> ({got_dir}, {got_mag}) "
              f"(expected ({exp_dir}, {exp_mag}))")

    if all_passed:
        print("All enum set-vs-delta tests passed!")
    else:
        print("WARNING: Some enum tests failed!")

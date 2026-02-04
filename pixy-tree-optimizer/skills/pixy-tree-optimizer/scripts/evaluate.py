#!/usr/bin/env python3
"""
evaluate.py - VLM evaluation for PixyTree optimization
Uses Ollama Cloud qwen-3vl:235b
"""

import json
from typing import Optional
from ollama import chat


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
- sub_branch_count, branch_recursion, phyllotaxis_angle
- apical_dominance, branch_flatness, trunk_flare
- leaf_style (0=CrossedPlanes, 1=SingleQuad, 2=ClusterSphere, 3=StarBurst, 4=NeedleCluster)
- foliage_placement (0=TerminalBranches, 1=AllBranches, 2=TipClusters)
- foliage_density, cluster_size, leaf_size
- leaf_droop, foliage_radius_threshold, foliage_height_falloff

For enum parameters (leaf_style, foliage_placement, crown_shape, trunk_termination),
suggest the exact numeric value (e.g., 2) rather than "increase"/"decrease".

Focus on the most impactful 3-5 parameters to adjust.
"""


STYLE_HINTS = {
    "low_poly": """
LOW-POLY STYLE CHARACTERISTICS:
- Geometric, faceted appearance with visible polygon edges
- Flat or vertex-colored shading, minimal texture detail
- Clean silhouettes, simplified branching
- Foliage should be LARGE rounded geometric clusters (octahedrons/icospheres)
- Best achieved with leaf_style=2 (ClusterSphere) and foliage_placement=2 (TipClusters)
- Examples: Firewatch, Astroneer, Monument Valley trees
""",
    "realistic": """
REALISTIC STYLE CHARACTERISTICS:
- Natural, organic branching patterns
- Detailed bark texture impression
- Proper proportions matching real tree species
- Complex foliage distribution
- Examples: Witcher 3, Skyrim trees
""",
    "cartoon": """
CARTOON STYLE CHARACTERISTICS:
- Exaggerated proportions, bold shapes
- Simplified but expressive forms
- Could have stylized curves or bulbous shapes
- Vibrant, saturated colors
- Examples: Fortnite, Overwatch environment trees
""",
    "pixel_art": """
PIXEL ART 3D STYLE CHARACTERISTICS:
- Chunky, blocky appearance
- Sharp edges, low resolution look
- Limited color palette
- Retro PSX/N64 aesthetic
- Examples: Hyper Light Drifter style, Octopath Traveler
""",
    "anime": """
ANIME/GHIBLI STYLE CHARACTERISTICS:
- Soft, painterly appearance
- Organic flowing shapes
- Warm, harmonious color palettes
- Stylized but natural feeling
- Examples: Genshin Impact, Ni no Kuni trees
""",
    "dead": """
DEAD/HORROR STYLE CHARACTERISTICS:
- Twisted, gnarled forms
- Broken branches, no foliage
- Dark, desaturated colors
- Ominous, atmospheric feeling
- Examples: Bloodborne, Dark Souls dead trees
"""
}


def parse_vlm_response(content: str) -> dict:
    """Extract JSON from VLM response, handling markdown fences."""
    # Handle markdown code fences
    if '```json' in content:
        content = content.split('```json')[1].split('```')[0]
    elif '```' in content:
        parts = content.split('```')
        if len(parts) >= 2:
            content = parts[1]
    
    # Try to find JSON object
    content = content.strip()
    
    # Find first { and last }
    start = content.find('{')
    end = content.rfind('}')
    if start != -1 and end != -1:
        content = content[start:end+1]
    
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Failed to parse VLM response: {e}")
        print(f"Content was: {content[:500]}...")
        return {
            "scores": {
                "silhouette": 5, 
                "branching": 5, 
                "trunk": 5, 
                "foliage": 5, 
                "style_match": 5
            },
            "overall_score": 5,
            "matches_well": False,
            "issues": ["Failed to parse VLM response"],
            "parameter_suggestions": {}
        }


def evaluate_tree(
    generated_images: list[str],
    reference_images: list[str],
    style: str,
    tree_type: str,
    model: str = 'qwen3-vl:235b-cloud'
) -> dict:
    """
    Send images to VLM for comparison evaluation.
    
    Args:
        generated_images: Paths to screenshots of generated tree
        reference_images: Paths to reference images
        style: Target art style (low_poly, realistic, etc.)
        tree_type: Tree type (oak, pine, etc.)
        model: Ollama model to use
        
    Returns:
        Evaluation dict with scores, issues, and suggestions
    """
    # Build prompt with style hints
    prompt = COMPARISON_PROMPT.format(
        style=style.replace("_", " ").title(),
        tree_type=tree_type.title()
    )
    
    # Add style-specific hints
    if style in STYLE_HINTS:
        prompt = STYLE_HINTS[style] + "\n" + prompt
    
    # Add context about which images are which
    prompt += f"\n\nFirst {len(reference_images)} image(s) are REFERENCE."
    prompt += f"\nRemaining {len(generated_images)} image(s) are GENERATED (different angles)."
    
    # Combine all image paths
    all_images = reference_images + generated_images
    
    try:
        response = chat(
            model=model,
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': all_images
            }]
        )
        
        result = parse_vlm_response(response.message.content)
        
        # Validate and fix scores
        scores = result.get("scores", {})
        for key in ["silhouette", "branching", "trunk", "foliage", "style_match"]:
            if key not in scores:
                scores[key] = 5
            scores[key] = max(1, min(10, int(scores[key])))
        
        # Calculate overall if missing
        if "overall_score" not in result:
            result["overall_score"] = sum(scores.values()) / len(scores)
        
        # Determine matches_well
        overall = result.get("overall_score", 5)
        all_above_7 = all(s >= 7 for s in scores.values())
        result["matches_well"] = overall >= 8 and all_above_7
        
        return result
        
    except Exception as e:
        print(f"VLM evaluation failed: {e}")
        # Retry once after a delay
        import time
        time.sleep(5)
        try:
            response = chat(
                model=model,
                messages=[{
                    'role': 'user',
                    'content': prompt,
                    'images': all_images
                }]
            )
            result = parse_vlm_response(response.message.content)
            scores = result.get("scores", {})
            for key in ["silhouette", "branching", "trunk", "foliage", "style_match"]:
                if key not in scores:
                    scores[key] = 5
                scores[key] = max(1, min(10, int(scores[key])))
            if "overall_score" not in result:
                result["overall_score"] = sum(scores.values()) / len(scores)
            overall = result.get("overall_score", 5)
            all_above_7 = all(s >= 7 for s in scores.values())
            result["matches_well"] = overall >= 8 and all_above_7
            return result
        except Exception as e2:
            print(f"VLM retry also failed: {e2}")
            return {
                "scores": {
                    "silhouette": 0,
                    "branching": 0,
                    "trunk": 0,
                    "foliage": 0,
                    "style_match": 0
                },
                "overall_score": 0,
                "matches_well": False,
                "vlm_failed": True,
                "issues": [f"VLM call failed: {str(e2)}"],
                "parameter_suggestions": {}
            }


def describe_tree(image_path: str, model: str = 'qwen3-vl:235b-cloud') -> str:
    """
    Get a detailed description of a tree image.
    Useful for debugging or understanding what the VLM sees.
    """
    prompt = """Describe this 3D tree in detail:
    
1. Overall shape and silhouette
2. Trunk characteristics (height, thickness, taper, texture)
3. Branch structure (density, angles, distribution)
4. Foliage (if present) - density, shape, color
5. Art style impression (realistic, stylized, low-poly, etc.)
6. Any notable features or issues

Be specific and objective."""

    try:
        response = chat(
            model=model,
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [image_path]
            }]
        )
        return response.message.content
    except Exception as e:
        return f"Description failed: {e}"


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python evaluate.py <image_path> [--reference <ref_path>] [--style <style>]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    ref_path = None
    style = "low_poly"
    tree_type = "oak"
    
    # Parse args
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--reference" and i + 1 < len(args):
            ref_path = args[i + 1]
            i += 2
        elif args[i] == "--style" and i + 1 < len(args):
            style = args[i + 1]
            i += 2
        elif args[i] == "--tree-type" and i + 1 < len(args):
            tree_type = args[i + 1]
            i += 2
        else:
            i += 1
    
    if ref_path:
        result = evaluate_tree(
            generated_images=[image_path],
            reference_images=[ref_path],
            style=style,
            tree_type=tree_type
        )
        print(json.dumps(result, indent=2))
    else:
        description = describe_tree(image_path)
        print(description)

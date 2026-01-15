#!/usr/bin/env python3
"""
Visual Output Checker - Analyze images using Ollama Cloud's vision models.

Usage:
    python analyze_visual.py <image_path> [--type TYPE] [--model MODEL] [--reference REF_IMAGE]
    
Examples:
    python analyze_visual.py render.png --type terrain
    python analyze_visual.py chart.png --type chart
    python analyze_visual.py screenshot.png --type ui --reference mockup.png
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from ollama import chat
except ImportError:
    print("Error: ollama package not installed. Run: pip install ollama")
    sys.exit(1)

# Domain-specific analysis prompts
PROMPTS = {
    "terrain": """Analyze this 3D terrain render for quality issues. Return JSON only:
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
}""",

    "chart": """Analyze this chart/graph for accuracy and clarity. Return JSON only:
{
    "score": 1-10,
    "passes": true/false (true if score >= 7),
    "issues": [
        {"severity": "high|medium|low", "description": "specific issue"}
    ],
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
    "fixes": ["specific actionable fixes"],
    "code_suggestion": "one-line code change if applicable"
}""",

    "ui": """Analyze this UI screenshot for design quality. Return JSON only:
{
    "score": 1-10,
    "passes": true/false (true if score >= 7),
    "issues": [
        {"severity": "high|medium|low", "description": "specific issue"}
    ],
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
    "fixes": ["specific actionable fixes"],
    "code_suggestion": "CSS/HTML change if applicable"
}""",

    "general": """Analyze this image for visual quality issues. Return JSON only:
{
    "score": 1-10,
    "passes": true/false (true if score >= 7),
    "issues": [
        {"severity": "high|medium|low", "description": "specific issue"}
    ],
    "observations": ["key observations about the image"],
    "fixes": ["suggested improvements"],
    "code_suggestion": "code change if applicable"
}"""
}

COMPARISON_PROMPT = """Compare these two images. The first is the test image, the second is the reference/expected image.
Identify differences and whether the test matches the reference. Return JSON only:
{
    "score": 1-10,
    "passes": true/false (true if score >= 7),
    "matches_reference": true/false,
    "differences": [
        {"severity": "high|medium|low", "description": "specific difference"}
    ],
    "fixes": ["changes needed to match reference"]
}"""


def analyze_image(
    image_path: str,
    check_type: str = "general",
    model: str = "qwen3-vl:235b-cloud",
    reference_path: str = None
) -> dict:
    """
    Analyze an image using Ollama's vision model.
    
    Args:
        image_path: Path to the image to analyze
        check_type: Type of analysis (terrain, chart, ui, general)
        model: Ollama model to use
        reference_path: Optional reference image for comparison
    
    Returns:
        dict: Analysis results as JSON
    """
    path = Path(image_path)
    if not path.exists():
        return {"error": f"Image not found: {image_path}"}
    
    # Build the prompt
    if reference_path and Path(reference_path).exists():
        prompt = COMPARISON_PROMPT
        images = [str(path), reference_path]
    else:
        prompt = PROMPTS.get(check_type, PROMPTS["general"])
        images = [str(path)]
    
    try:
        response = chat(
            model=model,
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': images
            }]
        )
        
        content = response.message.content
        
        # Try to parse as JSON
        # Handle common issues: markdown code blocks, trailing text
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0]
        elif '```' in content:
            content = content.split('```')[1].split('```')[0]
        
        try:
            return json.loads(content.strip())
        except json.JSONDecodeError:
            # Return raw response if JSON parsing fails
            return {
                "score": 0,
                "passes": False,
                "raw_response": response.message.content,
                "parse_error": True
            }
            
    except Exception as e:
        return {
            "error": str(e),
            "score": 0,
            "passes": False
        }


def main():
    parser = argparse.ArgumentParser(
        description="Analyze visual outputs using Ollama Cloud vision models"
    )
    parser.add_argument("image", help="Path to image to analyze")
    parser.add_argument(
        "--type", "-t",
        choices=["terrain", "chart", "ui", "general"],
        default="general",
        help="Type of analysis to perform"
    )
    parser.add_argument(
        "--model", "-m",
        default="qwen3-vl:235b-cloud",
        help="Ollama model to use (default: qwen3-vl:235b-cloud)"
    )
    parser.add_argument(
        "--reference", "-r",
        help="Reference image for comparison (optional)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Output only JSON, no status messages"
    )
    
    args = parser.parse_args()
    
    if not args.quiet:
        print(f"Analyzing: {args.image}", file=sys.stderr)
        print(f"Type: {args.type}", file=sys.stderr)
        print(f"Model: {args.model}", file=sys.stderr)
        if args.reference:
            print(f"Reference: {args.reference}", file=sys.stderr)
        print("---", file=sys.stderr)
    
    result = analyze_image(
        image_path=args.image,
        check_type=args.type,
        model=args.model,
        reference_path=args.reference
    )
    
    print(json.dumps(result, indent=2))
    
    # Exit with error code if analysis failed or score is low
    if result.get("error") or result.get("parse_error"):
        sys.exit(2)
    elif not result.get("passes", True):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

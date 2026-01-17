#!/usr/bin/env python3
"""
Visual Output Checker - Analyze images using Ollama's vision models.

Usage:
    python analyze_visual.py <image_path> [--reference REF] [--prompt PROMPT] [--model MODEL]

Examples:
    python analyze_visual.py render.png                              # Debug mode
    python analyze_visual.py test.png --reference expected.png       # Comparison
    python analyze_visual.py chart.png --prompt "Check axis labels"  # Custom
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from ollama import chat
except ImportError:
    print("Error: ollama package not installed. Run: pip install ollama", file=sys.stderr)
    sys.exit(1)


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


def parse_json_response(content: str) -> dict:
    """Extract JSON from VLM response, handling markdown fences."""
    if '```json' in content:
        content = content.split('```json')[1].split('```')[0]
    elif '```' in content:
        content = content.split('```')[1].split('```')[0]
    
    try:
        return json.loads(content.strip())
    except json.JSONDecodeError:
        return {
            "raw_response": content,
            "parse_error": True
        }


def analyze_image(
    image_path: str,
    model: str = "qwen3-vl:235b-cloud",
    reference_path: str = None,
    custom_prompt: str = None
) -> dict:
    """
    Analyze an image using Ollama's vision model.
    
    Args:
        image_path: Path to the image to analyze
        model: Ollama model to use
        reference_path: Optional reference image for comparison
        custom_prompt: Optional custom prompt (overrides default)
    
    Returns:
        dict: Analysis results
    """
    path = Path(image_path)
    if not path.exists():
        return {"error": f"Image not found: {image_path}"}
    
    # Determine prompt and images
    if custom_prompt:
        prompt = custom_prompt
        images = [str(path)]
        if reference_path and Path(reference_path).exists():
            images.append(reference_path)
    elif reference_path and Path(reference_path).exists():
        prompt = COMPARISON_PROMPT
        images = [str(path), reference_path]
    else:
        prompt = DEBUG_PROMPT
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
        return parse_json_response(response.message.content)
        
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="Analyze images using Ollama vision models"
    )
    parser.add_argument("image", help="Path to image to analyze")
    parser.add_argument(
        "--reference", "-r",
        help="Reference image for comparison"
    )
    parser.add_argument(
        "--prompt", "-p",
        help="Custom prompt (overrides default debug/comparison)"
    )
    parser.add_argument(
        "--model", "-m",
        default="qwen3-vl:235b-cloud",
        help="Ollama model (default: qwen3-vl:235b-cloud)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Output only JSON"
    )
    
    args = parser.parse_args()
    
    if not args.quiet:
        mode = "custom" if args.prompt else ("comparison" if args.reference else "debug")
        print(f"Image: {args.image}", file=sys.stderr)
        print(f"Mode: {mode}", file=sys.stderr)
        print(f"Model: {args.model}", file=sys.stderr)
        if args.reference:
            print(f"Reference: {args.reference}", file=sys.stderr)
        print("---", file=sys.stderr)
    
    result = analyze_image(
        image_path=args.image,
        model=args.model,
        reference_path=args.reference,
        custom_prompt=args.prompt
    )
    
    print(json.dumps(result, indent=2))
    
    # Exit codes: 0=success, 1=analysis issue, 2=error
    if result.get("error"):
        sys.exit(2)
    elif result.get("parse_error"):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

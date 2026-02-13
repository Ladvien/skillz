#!/usr/bin/env python3
"""
Meshy.ai Full Pipeline: Image → 3D → Remesh (Quad/Adaptive) → Texture → Animate

Usage:
    export MESHY_API_KEY="your_key"
    python meshy_pipeline.py \
        --image reference.png \
        --prompt "a low poly medieval shield" \
        --animations "idle,walk,run,attack" \
        --target-polycount 3000
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

BASE_URL = "https://api.meshy.ai"
POLL_INTERVAL = 10  # seconds


# =============================================================================
# .env file loading
# =============================================================================
def load_env_file(env_path: str | Path | None = None) -> dict:
    """
    Load key=value pairs from a .env file. Checks in order:
      1. Explicit path passed via --env-file
      2. .env in the current working directory
      3. .env in the script's own directory (~/skillz/meshy-pipeline/.env)
      4. ~/.env (home directory)

    Returns dict of loaded vars. Also injects them into os.environ.
    """
    candidates = []
    if env_path:
        candidates.append(Path(env_path))
    candidates.extend([
        Path.cwd() / ".env",
        Path(__file__).resolve().parent.parent / ".env",  # skillz/meshy-pipeline/.env
        Path.home() / ".env",
    ])

    loaded = {}
    for candidate in candidates:
        if candidate.is_file():
            print(f"  Loading .env from: {candidate}")
            with open(candidate) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    # Strip optional 'export ' prefix
                    if line.startswith("export "):
                        line = line[7:]
                    if "=" not in line:
                        continue
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip()
                    # Strip surrounding quotes
                    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
                        value = value[1:-1]
                    loaded[key] = value
                    os.environ.setdefault(key, value)
            return loaded  # Use first .env found

    return loaded


def resolve_api_key(args) -> str:
    """
    Resolve API key from (in priority order):
      1. --api-key CLI argument
      2. MESHY_API_KEY environment variable (may have been set by .env)
      3. Fail with clear error
    """
    # Load .env first so it populates os.environ
    load_env_file(getattr(args, "env_file", None))

    key = args.api_key or os.environ.get("MESHY_API_KEY")
    if not key:
        print("ERROR: No API key found. Provide it via one of:")
        print("  1. --api-key YOUR_KEY")
        print("  2. MESHY_API_KEY in environment")
        print("  3. MESHY_API_KEY=your_key in a .env file")
        print("     (.env checked in: cwd, skill dir, home dir)")
        sys.exit(1)
    return key


# =============================================================================
# Helpers
# =============================================================================
def get_headers(api_key: str) -> dict:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def is_url(s: str) -> bool:
    try:
        result = urlparse(s)
        return result.scheme in ("http", "https")
    except Exception:
        return False


def image_to_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_mime_type(path: str) -> str:
    ext = Path(path).suffix.lower()
    return {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(ext, "image/png")


def poll_task(api_key: str, endpoint: str, task_id: str, timeout: int, step_name: str) -> dict:
    """Poll a Meshy task until completion or timeout."""
    url = f"{BASE_URL}{endpoint}/{task_id}"
    headers = get_headers(api_key)
    start = time.time()
    retries = 0
    max_retries = 3

    print(f"  [{step_name}] Polling task {task_id}...")

    while True:
        elapsed = time.time() - start
        if elapsed > timeout:
            raise TimeoutError(f"[{step_name}] Task {task_id} timed out after {timeout}s")

        try:
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            retries += 1
            if retries > max_retries:
                raise RuntimeError(f"[{step_name}] Failed to poll after {max_retries} retries: {e}")
            print(f"  [{step_name}] Poll error (retry {retries}/{max_retries}): {e}")
            time.sleep(POLL_INTERVAL)
            continue

        status = data.get("status", "UNKNOWN")
        progress = data.get("progress", 0)
        print(f"  [{step_name}] Status: {status} | Progress: {progress}% | Elapsed: {int(elapsed)}s")

        if status == "SUCCEEDED":
            return data
        elif status in ("FAILED", "EXPIRED"):
            error_msg = data.get("task_error", {}).get("message", "Unknown error")
            raise RuntimeError(f"[{step_name}] Task failed: {error_msg}")

        time.sleep(POLL_INTERVAL)


def download_file(url: str, dest: Path):
    """Download a file from URL to local path."""
    print(f"  Downloading {url} → {dest}")
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)


def save_task_info(data: dict, dest: Path):
    """Save task response JSON."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "w") as f:
        json.dump(data, f, indent=2)


# =============================================================================
# Step 1: Image to 3D
# =============================================================================
def step_image_to_3d(
    api_key: str,
    image: str,
    target_polycount: int,
    output_dir: Path,
    timeout: int,
    output_format: str = "glb",
) -> dict:
    """Generate 3D mesh from reference image."""
    print("\n" + "=" * 60)
    print("STEP 1: Image to 3D")
    print("=" * 60)

    endpoint = "/openapi/v2/image-to-3d"
    headers = get_headers(api_key)

    body = {
        "enable_pbr": True,
        "should_remesh": False,  # We'll remesh ourselves in step 2
        "topology": "triangle",  # Start with triangles, remesh to quads later
        "target_polycount": target_polycount * 2,  # Give remesher room to work
    }

    if is_url(image):
        body["image_url"] = image
    else:
        mime = get_mime_type(image)
        b64 = image_to_base64(image)
        body["image_url"] = f"data:{mime};base64,{b64}"

    print(f"  Submitting image-to-3d task (target ~{body['target_polycount']} polys)...")
    resp = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=body)
    resp.raise_for_status()
    result = resp.json()
    task_id = result.get("result", result.get("id", ""))

    if not task_id:
        raise RuntimeError(f"No task ID returned: {result}")

    print(f"  Task ID: {task_id}")

    # Poll until done
    data = poll_task(api_key, endpoint, task_id, timeout, "Image-to-3D")

    # Save results
    step_dir = output_dir / "01_image_to_3d"
    save_task_info(data, step_dir / "task_info.json")

    # Download model
    model_urls = data.get("model_urls", {})
    model_url = model_urls.get(output_format) or model_urls.get("glb") or model_urls.get("obj")

    if model_url:
        download_file(model_url, step_dir / f"model.{output_format}")

    print(f"  ✓ Image-to-3D complete. Model saved to {step_dir}")
    return data


# =============================================================================
# Step 2: Remesh
# =============================================================================
def step_remesh(
    api_key: str,
    model_url: str,
    target_polycount: int,
    topology: str,
    output_dir: Path,
    timeout: int,
    output_format: str = "glb",
) -> dict:
    """Remesh to quad topology with adaptive low-poly target."""
    print("\n" + "=" * 60)
    print("STEP 2: Remesh (Quad / Adaptive / Low-Poly)")
    print("=" * 60)

    endpoint = "/openapi/v1/remesh"
    headers = get_headers(api_key)

    body = {
        "input_model_url": model_url,
        "topology": topology,
        "target_polycount": target_polycount,
        "target_formats": [output_format],
    }

    print(f"  Submitting remesh task (topology={topology}, target={target_polycount} polys)...")
    resp = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=body)
    resp.raise_for_status()
    result = resp.json()
    task_id = result.get("result", result.get("id", ""))

    if not task_id:
        raise RuntimeError(f"No task ID returned: {result}")

    print(f"  Task ID: {task_id}")

    data = poll_task(api_key, endpoint, task_id, timeout, "Remesh")

    step_dir = output_dir / "02_remesh"
    save_task_info(data, step_dir / "task_info.json")

    model_urls = data.get("model_urls", {})
    model_url_out = model_urls.get(output_format) or model_urls.get("glb")

    if model_url_out:
        download_file(model_url_out, step_dir / f"model.{output_format}")

    print(f"  ✓ Remesh complete. {topology} mesh at ~{target_polycount} polys.")
    return data


# =============================================================================
# Step 3: Texture
# =============================================================================
def step_texture(
    api_key: str,
    model_url: str,
    object_prompt: str,
    style_prompt: str,
    art_style: str,
    enable_pbr: bool,
    resolution: str,
    output_dir: Path,
    timeout: int,
    output_format: str = "glb",
) -> dict:
    """Apply AI-generated textures to the model."""
    print("\n" + "=" * 60)
    print("STEP 3: Texture")
    print("=" * 60)

    endpoint = "/openapi/v2/text-to-texture"
    headers = get_headers(api_key)

    body = {
        "model_url": model_url,
        "object_prompt": object_prompt,
        "style_prompt": style_prompt,
        "art_style": art_style,
        "enable_pbr": enable_pbr,
        "resolution": resolution,
    }

    print(f"  Submitting texture task (style={art_style}, resolution={resolution})...")
    resp = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=body)
    resp.raise_for_status()
    result = resp.json()
    task_id = result.get("result", result.get("id", ""))

    if not task_id:
        raise RuntimeError(f"No task ID returned: {result}")

    print(f"  Task ID: {task_id}")

    data = poll_task(api_key, endpoint, task_id, timeout, "Texture")

    step_dir = output_dir / "03_texture"
    save_task_info(data, step_dir / "task_info.json")

    model_urls = data.get("model_urls", {})
    model_url_out = model_urls.get(output_format) or model_urls.get("glb")

    if model_url_out:
        download_file(model_url_out, step_dir / f"model.{output_format}")

    # Download texture maps if PBR
    texture_urls = data.get("texture_urls", [])
    if texture_urls and isinstance(texture_urls, list):
        for tex in texture_urls:
            if isinstance(tex, dict):
                for map_name, map_url in tex.items():
                    if map_url and isinstance(map_url, str) and map_url.startswith("http"):
                        ext = Path(urlparse(map_url).path).suffix or ".png"
                        download_file(map_url, step_dir / f"{map_name}{ext}")

    print(f"  ✓ Texture complete.")
    return data


# =============================================================================
# Step 4: Animate
# =============================================================================
def step_animate(
    api_key: str,
    model_url: str,
    animation_prompts: list[str],
    output_dir: Path,
    timeout: int,
    output_format: str = "glb",
) -> list[dict]:
    """Add animations to the model. One task per animation prompt."""
    print("\n" + "=" * 60)
    print("STEP 4: Animate")
    print("=" * 60)

    if not animation_prompts:
        print("  No animations requested. Skipping.")
        return []

    endpoint = "/openapi/v1/animate"
    headers = get_headers(api_key)
    results = []

    for i, anim_prompt in enumerate(animation_prompts):
        anim_name = anim_prompt.strip().replace(" ", "_").lower()
        print(f"\n  --- Animation {i + 1}/{len(animation_prompts)}: '{anim_prompt}' ---")

        body = {
            "input_model_url": model_url,
            "animation_prompt": anim_prompt.strip(),
        }

        try:
            resp = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=body)
            resp.raise_for_status()
            result = resp.json()
            task_id = result.get("result", result.get("id", ""))

            if not task_id:
                print(f"  ✗ No task ID for '{anim_prompt}': {result}")
                results.append({"prompt": anim_prompt, "status": "FAILED", "error": "No task ID"})
                continue

            print(f"  Task ID: {task_id}")
            data = poll_task(api_key, endpoint, task_id, timeout, f"Animate:{anim_name}")

            anim_dir = output_dir / "04_animate" / anim_name
            save_task_info(data, anim_dir / "task_info.json")

            # Download animated model
            model_urls = data.get("model_urls", {})
            anim_url = model_urls.get(output_format) or model_urls.get("glb")
            if anim_url:
                download_file(anim_url, anim_dir / f"model.{output_format}")

            # Also check for video preview
            video_url = data.get("video_url")
            if video_url:
                download_file(video_url, anim_dir / "preview.mp4")

            results.append({"prompt": anim_prompt, "status": "SUCCEEDED", "data": data})
            print(f"  ✓ Animation '{anim_prompt}' complete.")

        except Exception as e:
            print(f"  ✗ Animation '{anim_prompt}' failed: {e}")
            results.append({"prompt": anim_prompt, "status": "FAILED", "error": str(e)})

        # Small delay between animation submissions to avoid rate limits
        if i < len(animation_prompts) - 1:
            time.sleep(2)

    return results


# =============================================================================
# Helpers to extract model URLs from task results
# =============================================================================
def get_model_url(task_data: dict, preferred_format: str = "glb") -> str | None:
    """Extract best model URL from a completed task."""
    model_urls = task_data.get("model_urls", {})
    return (
        model_urls.get(preferred_format)
        or model_urls.get("glb")
        or model_urls.get("fbx")
        or model_urls.get("obj")
        or model_urls.get("usdz")
    )


# =============================================================================
# Main Pipeline
# =============================================================================
def run_pipeline(args):
    api_key = resolve_api_key(args)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pipeline_result = {
        "config": {k: v for k, v in vars(args).items() if k != "api_key"},
        "steps": {},
        "status": "RUNNING",
    }

    current_model_url = None

    # ── Step 1: Image to 3D ──
    try:
        img3d_data = step_image_to_3d(
            api_key=api_key,
            image=args.image,
            target_polycount=args.target_polycount,
            output_dir=output_dir,
            timeout=args.timeout,
            output_format=args.output_format,
        )
        current_model_url = get_model_url(img3d_data, args.output_format)
        pipeline_result["steps"]["image_to_3d"] = {
            "status": "SUCCEEDED",
            "model_url": current_model_url,
        }
    except Exception as e:
        print(f"\n✗ FATAL: Image-to-3D failed: {e}")
        pipeline_result["steps"]["image_to_3d"] = {"status": "FAILED", "error": str(e)}
        pipeline_result["status"] = "FAILED"
        save_task_info(pipeline_result, output_dir / "pipeline_summary.json")
        sys.exit(1)

    # ── Step 2: Remesh ──
    if not args.skip_remesh:
        try:
            remesh_data = step_remesh(
                api_key=api_key,
                model_url=current_model_url,
                target_polycount=args.target_polycount,
                topology=args.topology,
                output_dir=output_dir,
                timeout=args.timeout,
                output_format=args.output_format,
            )
            remeshed_url = get_model_url(remesh_data, args.output_format)
            if remeshed_url:
                current_model_url = remeshed_url
            pipeline_result["steps"]["remesh"] = {
                "status": "SUCCEEDED",
                "model_url": current_model_url,
            }
        except Exception as e:
            print(f"\n⚠ Remesh failed: {e}. Continuing with original mesh.")
            pipeline_result["steps"]["remesh"] = {"status": "FAILED", "error": str(e)}
    else:
        print("\n  Skipping remesh (--skip-remesh)")
        pipeline_result["steps"]["remesh"] = {"status": "SKIPPED"}

    # ── Step 3: Texture ──
    if not args.skip_texture:
        try:
            texture_data = step_texture(
                api_key=api_key,
                model_url=current_model_url,
                object_prompt=args.prompt,
                style_prompt=args.style,
                art_style=args.art_style,
                enable_pbr=args.enable_pbr,
                resolution=args.resolution,
                output_dir=output_dir,
                timeout=args.timeout,
                output_format=args.output_format,
            )
            textured_url = get_model_url(texture_data, args.output_format)
            if textured_url:
                current_model_url = textured_url
            pipeline_result["steps"]["texture"] = {
                "status": "SUCCEEDED",
                "model_url": current_model_url,
            }
        except Exception as e:
            print(f"\n⚠ Texture failed: {e}. Continuing with untextured mesh.")
            pipeline_result["steps"]["texture"] = {"status": "FAILED", "error": str(e)}
    else:
        print("\n  Skipping texture (--skip-texture)")
        pipeline_result["steps"]["texture"] = {"status": "SKIPPED"}

    # ── Step 4: Animate ──
    if not args.skip_animate and args.animations:
        anim_prompts = [a.strip() for a in args.animations.split(",") if a.strip()]
        anim_results = step_animate(
            api_key=api_key,
            model_url=current_model_url,
            animation_prompts=anim_prompts,
            output_dir=output_dir,
            timeout=args.timeout,
            output_format=args.output_format,
        )
        succeeded = sum(1 for r in anim_results if r["status"] == "SUCCEEDED")
        pipeline_result["steps"]["animate"] = {
            "status": "SUCCEEDED" if succeeded > 0 else "FAILED",
            "total": len(anim_prompts),
            "succeeded": succeeded,
            "failed": len(anim_prompts) - succeeded,
            "results": [
                {"prompt": r["prompt"], "status": r["status"]}
                for r in anim_results
            ],
        }
    elif args.skip_animate:
        print("\n  Skipping animation (--skip-animate)")
        pipeline_result["steps"]["animate"] = {"status": "SKIPPED"}
    else:
        print("\n  No animations specified.")
        pipeline_result["steps"]["animate"] = {"status": "SKIPPED", "reason": "no prompts"}

    # ── Summary ──
    pipeline_result["status"] = "COMPLETED"
    pipeline_result["final_model_url"] = current_model_url
    save_task_info(pipeline_result, output_dir / "pipeline_summary.json")

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)
    print(f"  Output directory: {output_dir}")
    print(f"  Final model URL:  {current_model_url}")
    for step_name, step_info in pipeline_result["steps"].items():
        status = step_info.get("status", "UNKNOWN")
        icon = "✓" if status == "SUCCEEDED" else "⚠" if status == "SKIPPED" else "✗"
        print(f"  {icon} {step_name}: {status}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Meshy.ai Full Pipeline: Image → 3D → Remesh → Texture → Animate"
    )
    parser.add_argument("--image", required=True, help="Reference image path or URL")
    parser.add_argument("--prompt", required=True, help="Object description for texturing")
    parser.add_argument("--style", default="", help="Style prompt for texturing")
    parser.add_argument(
        "--art-style",
        default="low-poly",
        choices=["realistic", "cartoon", "low-poly", "sculpture", "pbr"],
        help="Art style for texturing (default: low-poly)",
    )
    parser.add_argument(
        "--animations",
        default="",
        help="Comma-separated animation prompts (e.g., 'idle,walk,run,attack')",
    )
    parser.add_argument(
        "--target-polycount", type=int, default=3000, help="Target polygon count (default: 3000)"
    )
    parser.add_argument(
        "--topology",
        default="quad",
        choices=["quad", "triangle"],
        help="Remesh topology (default: quad)",
    )
    parser.add_argument("--enable-pbr", action="store_true", help="Enable PBR texture maps")
    parser.add_argument(
        "--resolution",
        default="2048",
        choices=["1024", "2048", "4096"],
        help="Texture resolution (default: 2048)",
    )
    parser.add_argument("--output-dir", default="./output", help="Output directory")
    parser.add_argument(
        "--output-format",
        default="glb",
        choices=["glb", "fbx", "obj", "usdz"],
        help="Preferred output format (default: glb)",
    )
    parser.add_argument(
        "--timeout", type=int, default=600, help="Timeout per step in seconds (default: 600)"
    )
    parser.add_argument("--api-key", default=None, help="Meshy API key (or set MESHY_API_KEY)")
    parser.add_argument(
        "--env-file", default=None, help="Path to .env file (default: auto-detect)"
    )
    parser.add_argument("--skip-remesh", action="store_true", help="Skip remesh step")
    parser.add_argument("--skip-texture", action="store_true", help="Skip texture step")
    parser.add_argument("--skip-animate", action="store_true", help="Skip animate step")

    args = parser.parse_args()
    run_pipeline(args)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Meshy.ai Rig & Batch Animate — Upload a local FBX, rig it, then generate
38 animations from the Meshy animation library using action_ids.

Usage:
    python3 meshy_rig_animate.py \
        --model ~/Downloads/succubus/Meshy_AI_Character_output.fbx \
        --texture ~/Downloads/succubus/Meshy_AI_texture_0.png \
        --output-dir ~/pixy/pixy_game/godot/assets/models/succubus \
        --fps 60

Resume after interruption (skips completed animations automatically):
    python3 meshy_rig_animate.py \
        --model ~/Downloads/succubus/Meshy_AI_Character_output.fbx \
        --texture ~/Downloads/succubus/Meshy_AI_texture_0.png \
        --output-dir ~/pixy/pixy_game/godot/assets/models/succubus \
        --fps 60

Retry only failed animations:
    python3 meshy_rig_animate.py \
        --output-dir ~/pixy/pixy_game/godot/assets/models/succubus \
        --retry-failed
"""

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import requests

BASE_URL = "https://api.meshy.ai"
POLL_INTERVAL = 10  # seconds
SUBMIT_DELAY = 3    # seconds between animation submissions

# ─── Animation catalog: name → action_id ──────────────────────────────────────
ANIMATION_CATALOG = {
    # Locomotion (10)
    "idle":             0,
    "combat_idle":      11,
    "casual_walk":      30,
    "flirty_strut":     108,
    "confident_walk":   106,
    "run":              14,
    "sprint":           16,
    "injured_walk":     111,
    "walk_backward":    544,
    "step_back":        543,
    # Combat melee (8)
    "attack":               4,
    "flying_fist_kick":     94,
    "simple_kick":          103,
    "roundhouse_kick":      207,
    "leg_sweep":            213,
    "lunge_spin_kick":      216,
    "double_blade_spin":    91,
    "triple_combo_attack":  105,
    # Magic (6)
    "charged_spell_cast":   125,
    "charged_spell_cast_1": 126,
    "charged_ground_slam":  127,
    "mage_spell_cast":      129,
    "mage_spell_cast_1":    130,
    "mage_spell_cast_2":    131,
    # Defense (4)
    "dodge_and_counter":        93,
    "stand_dodge":              156,
    "roll_dodge":               158,
    "quick_step_spin_dodge":    384,
    # Hit reactions (3)
    "face_punch_reaction":  174,
    "hit_reaction":         178,
    "hit_reaction_waist":   171,
    # Death (3)
    "dead":             8,
    "knock_down":       187,
    "dying_backwards":  189,
    # Taunts (4)
    "chest_pound_taunt":    88,
    "neck_slash_gesture":   411,
    "hand_on_hip":          315,
    "scream":               386,
    # Acrobatics (2)
    "backflip":             452,
    "sprint_roll_flip":     401,
}


# ─── .env + auth (same pattern as meshy_pipeline.py) ──────────────────────────
def load_env_file(env_path=None):
    candidates = []
    if env_path:
        candidates.append(Path(env_path))
    candidates.extend([
        Path.cwd() / ".env",
        Path(__file__).resolve().parent.parent / ".env",
        Path.home() / "pixy" / "pixy_game" / ".env",
        Path.home() / ".env",
    ])
    for candidate in candidates:
        if candidate.is_file():
            with open(candidate) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith("export "):
                        line = line[7:]
                    if "=" not in line:
                        continue
                    key, _, value = line.partition("=")
                    key, value = key.strip(), value.strip()
                    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
                        value = value[1:-1]
                    os.environ.setdefault(key, value)
            return


def get_api_key(args):
    load_env_file(getattr(args, "env_file", None))
    key = getattr(args, "api_key", None) or os.environ.get("MESHY_API_KEY")
    if not key:
        print("ERROR: No API key. Set MESHY_API_KEY via .env, env var, or --api-key.")
        sys.exit(1)
    return key


def get_headers(api_key):
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


# ─── Helpers ──────────────────────────────────────────────────────────────────
def convert_fbx_to_glb(fbx_path: Path) -> Path:
    """Convert FBX to GLB using assimp CLI. Returns path to temp GLB file."""
    glb_path = Path(tempfile.mkdtemp()) / (fbx_path.stem + ".glb")
    print(f"  Converting {fbx_path.name} to GLB...")
    result = subprocess.run(
        ["assimp", "export", str(fbx_path), str(glb_path)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"FBX-to-GLB conversion failed: {result.stderr}")
    print(f"  Converted to {glb_path} ({glb_path.stat().st_size / 1024 / 1024:.1f} MB)")
    return glb_path


def file_to_data_uri(path: Path) -> str:
    """Convert a local file to a base64 data URI."""
    ext = path.suffix.lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".glb": "model/gltf-binary",
        ".fbx": "application/octet-stream",
    }
    mime = mime_map.get(ext, "application/octet-stream")
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode("utf-8")
    print(f"  Encoded {path.name} ({len(data)/1024/1024:.1f} MB) as data URI")
    return f"data:{mime};base64,{b64}"


def poll_task(api_key: str, endpoint: str, task_id: str, timeout: int, step_name: str) -> dict:
    """Poll a Meshy task until completion or timeout."""
    url = f"{BASE_URL}{endpoint}/{task_id}"
    hdrs = get_headers(api_key)
    start = time.time()
    retries = 0
    max_retries = 3

    print(f"  [{step_name}] Polling task {task_id}...")

    while True:
        elapsed = time.time() - start
        if elapsed > timeout:
            raise TimeoutError(f"[{step_name}] Task {task_id} timed out after {timeout}s")

        try:
            resp = requests.get(url, headers=hdrs)
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
    print(f"  Downloading -> {dest}")
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)


def load_progress(output_dir: Path) -> dict:
    """Load progress.json from output dir."""
    path = output_dir / "progress.json"
    if path.is_file():
        with open(path) as f:
            return json.load(f)
    return {"rig_task_id": None, "animations": {}}


def save_progress(output_dir: Path, progress: dict):
    """Save progress.json to output dir."""
    path = output_dir / "progress.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(progress, f, indent=2)


def save_task_info(data: dict, dest: Path):
    """Save task response JSON."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "w") as f:
        json.dump(data, f, indent=2)


# ─── Step 1: Rig ─────────────────────────────────────────────────────────────
def step_rig(
    api_key: str,
    model_path: Path,
    texture_path: Path | None,
    output_dir: Path,
    timeout: int,
) -> str:
    """Upload model, rig it, download rigged FBX. Returns rig_task_id."""
    print("\n" + "=" * 60)
    print("STEP 1: Rig Character")
    print("=" * 60)

    endpoint = "/openapi/v1/rigging"

    # Meshy rigging API requires GLB — convert FBX if needed
    upload_path = model_path
    if model_path.suffix.lower() == ".fbx":
        upload_path = convert_fbx_to_glb(model_path)

    body = {
        "model_url": file_to_data_uri(upload_path),
        "height_meters": 1.7,
    }

    if texture_path and texture_path.is_file():
        body["texture_image_url"] = file_to_data_uri(texture_path)

    print(f"  Submitting rigging task...")
    resp = requests.post(f"{BASE_URL}{endpoint}", headers=get_headers(api_key), json=body)
    if not resp.ok:
        print(f"  ERROR {resp.status_code}: {resp.text[:500]}")
    resp.raise_for_status()
    result = resp.json()
    task_id = result.get("result", result.get("id", ""))

    if not task_id:
        raise RuntimeError(f"No task ID returned: {result}")

    print(f"  Task ID: {task_id}")

    data = poll_task(api_key, endpoint, task_id, timeout, "Rig")

    # Save task info
    char_dir = output_dir / "character"
    save_task_info(data, char_dir / "rig_task_info.json")

    # Download rigged model (FBX)
    rig_result = data.get("result", {})
    fbx_url = rig_result.get("rigged_character_fbx_url")
    if fbx_url:
        download_file(fbx_url, char_dir / "succubus_rigged.fbx")
    else:
        glb_url = rig_result.get("rigged_character_glb_url")
        if glb_url:
            download_file(glb_url, char_dir / "succubus_rigged.glb")

    print(f"  Rig complete. Task ID: {task_id}")
    return task_id


# ─── Step 2: Batch animate ───────────────────────────────────────────────────
def step_animate_one(
    api_key: str,
    rig_task_id: str,
    anim_name: str,
    action_id: int,
    fps: int,
    output_dir: Path,
    timeout: int,
) -> dict:
    """Submit one animation task, poll, download FBX. Returns status dict."""
    endpoint = "/openapi/v1/animations"

    body = {
        "rig_task_id": rig_task_id,
        "action_id": action_id,
    }

    if fps and fps != 30:
        body["post_process"] = {
            "operation_type": "change_fps",
            "fps": fps,
        }

    print(f"  Submitting animation '{anim_name}' (action_id={action_id})...")
    resp = requests.post(f"{BASE_URL}{endpoint}", headers=get_headers(api_key), json=body)
    resp.raise_for_status()
    result = resp.json()
    task_id = result.get("result", result.get("id", ""))

    if not task_id:
        raise RuntimeError(f"No task ID returned for '{anim_name}': {result}")

    print(f"  Task ID: {task_id}")

    data = poll_task(api_key, endpoint, task_id, timeout, f"Animate:{anim_name}")

    # Save task info
    anim_dir = output_dir / "animations"
    save_task_info(data, anim_dir / f"{anim_name}_task_info.json")

    # Download FBX — prefer fps-adjusted version when post_process was used
    anim_result = data.get("result", {})
    fbx_url = None
    if fps and fps != 30:
        fbx_url = anim_result.get("processed_animation_fps_fbx_url")
    if not fbx_url:
        fbx_url = anim_result.get("animation_fbx_url")
    if not fbx_url:
        fbx_url = anim_result.get("animation_glb_url")

    if fbx_url:
        ext = "fbx" if "fbx" in fbx_url else "glb"
        download_file(fbx_url, anim_dir / f"{anim_name}.{ext}")

    return {
        "status": "SUCCEEDED",
        "task_id": task_id,
        "action_id": action_id,
    }


def step_animate_batch(
    api_key: str,
    rig_task_id: str,
    fps: int,
    output_dir: Path,
    timeout: int,
    progress: dict,
    retry_failed: bool = False,
) -> dict:
    """Iterate animation catalog, submit each, save progress after each."""
    print("\n" + "=" * 60)
    print("STEP 2: Batch Animate (38 animations)")
    print("=" * 60)

    animations = progress.get("animations", {})
    total = len(ANIMATION_CATALOG)
    succeeded = sum(1 for v in animations.values() if v.get("status") == "SUCCEEDED")
    failed = sum(1 for v in animations.values() if v.get("status") == "FAILED")

    if succeeded > 0:
        print(f"  Resuming: {succeeded} already completed, {failed} failed, {total - succeeded - failed} remaining")

    for i, (anim_name, action_id) in enumerate(ANIMATION_CATALOG.items()):
        existing = animations.get(anim_name, {})
        existing_status = existing.get("status")

        # Skip completed
        if existing_status == "SUCCEEDED":
            continue

        # Skip non-failed unless retrying
        if existing_status == "FAILED" and not retry_failed:
            print(f"\n  [{i+1}/{total}] Skipping failed '{anim_name}' (use --retry-failed)")
            continue

        print(f"\n  --- [{i+1}/{total}] {anim_name} (action_id={action_id}) ---")

        try:
            result = step_animate_one(
                api_key=api_key,
                rig_task_id=rig_task_id,
                anim_name=anim_name,
                action_id=action_id,
                fps=fps,
                output_dir=output_dir,
                timeout=timeout,
            )
            animations[anim_name] = result
            print(f"  Animation '{anim_name}' complete.")
        except Exception as e:
            print(f"  Animation '{anim_name}' FAILED: {e}")
            animations[anim_name] = {
                "status": "FAILED",
                "action_id": action_id,
                "error": str(e),
            }

        # Save progress after each animation
        progress["animations"] = animations
        save_progress(output_dir, progress)

        # Rate limit delay (skip after last)
        remaining = [
            name for name in list(ANIMATION_CATALOG.keys())[i+1:]
            if animations.get(name, {}).get("status") != "SUCCEEDED"
        ]
        if remaining:
            time.sleep(SUBMIT_DELAY)

    return progress


# ─── Copy textures ────────────────────────────────────────────────────────────
def copy_textures(source_dir: Path, output_dir: Path):
    """Copy texture files from source (Downloads) to output character/textures/."""
    tex_dir = output_dir / "character" / "textures"
    tex_dir.mkdir(parents=True, exist_ok=True)

    texture_map = {
        "Meshy_AI_texture_0.png": "albedo.png",
        "Meshy_AI_texture_0_normal.png": "normal.png",
        "Meshy_AI_texture_0_metallic.png": "metallic.png",
        "Meshy_AI_texture_0_roughness.png": "roughness.png",
    }

    for src_name, dst_name in texture_map.items():
        src = source_dir / src_name
        if src.is_file():
            dst = tex_dir / dst_name
            shutil.copy2(src, dst)
            print(f"  Copied {src_name} -> {dst}")
        else:
            print(f"  Skipped {src_name} (not found)")


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Meshy.ai Rig & Batch Animate — rig a local model then generate 38 animations"
    )
    parser.add_argument("--model", type=str, help="Path to local FBX/GLB model file")
    parser.add_argument("--texture", type=str, help="Path to albedo texture (PNG)")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument("--fps", type=int, default=60, help="Animation FPS (default: 60)")
    parser.add_argument("--timeout", type=int, default=600, help="Timeout per task in seconds (default: 600)")
    parser.add_argument("--api-key", default=None, help="Meshy API key (or set MESHY_API_KEY)")
    parser.add_argument("--env-file", default=None, help="Path to .env file")
    parser.add_argument("--retry-failed", action="store_true", help="Re-attempt only failed animations")
    parser.add_argument("--skip-rig", action="store_true", help="Skip rigging (use existing rig_task_id from progress.json)")
    parser.add_argument("--skip-textures", action="store_true", help="Skip copying texture files")

    args = parser.parse_args()
    api_key = get_api_key(args)
    output_dir = Path(args.output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    progress = load_progress(output_dir)

    # ── Step 1: Rig ──
    rig_task_id = progress.get("rig_task_id")

    if args.skip_rig and rig_task_id:
        print(f"\n  Skipping rig (using existing rig_task_id: {rig_task_id})")
    elif args.retry_failed and rig_task_id:
        print(f"\n  Rig already completed (rig_task_id: {rig_task_id})")
    else:
        if not args.model:
            print("ERROR: --model is required for rigging step.")
            sys.exit(1)

        model_path = Path(args.model).expanduser()
        if not model_path.is_file():
            print(f"ERROR: Model file not found: {model_path}")
            sys.exit(1)

        texture_path = Path(args.texture).expanduser() if args.texture else None

        rig_task_id = step_rig(
            api_key=api_key,
            model_path=model_path,
            texture_path=texture_path,
            output_dir=output_dir,
            timeout=args.timeout,
        )

        progress["rig_task_id"] = rig_task_id
        save_progress(output_dir, progress)

    # ── Copy textures ──
    if not args.skip_textures and args.model:
        model_path = Path(args.model).expanduser()
        print("\n  Copying textures...")
        copy_textures(model_path.parent, output_dir)

    # ── Step 2: Batch animate ──
    progress = step_animate_batch(
        api_key=api_key,
        rig_task_id=rig_task_id,
        fps=args.fps,
        output_dir=output_dir,
        timeout=args.timeout,
        progress=progress,
        retry_failed=args.retry_failed,
    )

    # ── Summary ──
    animations = progress.get("animations", {})
    succeeded = sum(1 for v in animations.values() if v.get("status") == "SUCCEEDED")
    failed = sum(1 for v in animations.values() if v.get("status") == "FAILED")
    total = len(ANIMATION_CATALOG)

    print("\n" + "=" * 60)
    print("COMPLETE")
    print("=" * 60)
    print(f"  Rig task ID:  {rig_task_id}")
    print(f"  Animations:   {succeeded}/{total} succeeded, {failed} failed")
    print(f"  Output:       {output_dir}")

    if failed > 0:
        print(f"\n  Failed animations:")
        for name, info in animations.items():
            if info.get("status") == "FAILED":
                print(f"    - {name}: {info.get('error', 'unknown')}")
        print(f"\n  Re-run with --retry-failed to retry these.")

    print()


if __name__ == "__main__":
    main()

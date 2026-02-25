#!/usr/bin/env python3
"""
Meshy.ai API helper — list, status, download, retry operations.

Used by meshy-pipeline commands. Handles .env loading, auth, and pagination.

Usage:
    python meshy_api.py list-meshes [--status STATUS] [--page N] [--page-size N]
    python meshy_api.py list-animations [--status STATUS] [--page N]
    python meshy_api.py list-textures [--status STATUS] [--page N]
    python meshy_api.py list-remeshes [--status STATUS] [--page N]
    python meshy_api.py status --task-id ID --type TYPE
    python meshy_api.py status --latest
    python meshy_api.py download --task-id ID [--format FORMAT] [--output-dir DIR]
    python meshy_api.py download --latest --type TYPE [--output-dir DIR]
    python meshy_api.py retry --task-id ID --type TYPE
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests

BASE_URL = "https://api.meshy.ai"

ENDPOINTS = {
    "image-to-3d": "/openapi/v1/image-to-3d",
    "multi-image-to-3d": "/openapi/v1/multi-image-to-3d",
    "text-to-3d": "/openapi/v2/text-to-3d",
    "remesh": "/openapi/v1/remesh",
    "retexture": "/openapi/v1/retexture",
    "animations": "/openapi/v1/animations",
    "rigging": "/openapi/v1/rigging",
    "text-to-image": "/openapi/v1/text-to-image",
    "image-to-image": "/openapi/v1/image-to-image",
}

# Endpoints that support the list (GET without :id) operation
LISTABLE_ENDPOINTS = {
    "image-to-3d", "multi-image-to-3d", "text-to-3d", "remesh",
    "retexture", "text-to-image", "image-to-image",
    # "animations" has NO list endpoint per Meshy docs
}

TYPE_ALIASES = {
    "mesh": "image-to-3d",
    "meshes": "image-to-3d",
    "3d": "image-to-3d",
    "multi": "multi-image-to-3d",
    "text3d": "text-to-3d",
    "remeshes": "remesh",
    "texture": "retexture",
    "textures": "retexture",
    "animate": "animations",
    "anim": "animations",
    "animation": "animations",
    "rig": "rigging",
    "img": "text-to-image",
    "img2img": "image-to-image",
}


# =============================================================================
# .env + auth (shared with meshy_pipeline.py)
# =============================================================================
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
    return


def get_api_key(args):
    load_env_file(getattr(args, "env_file", None))
    key = getattr(args, "api_key", None) or os.environ.get("MESHY_API_KEY")
    if not key:
        print("ERROR: No API key. Set MESHY_API_KEY via .env, env var, or --api-key.")
        sys.exit(1)
    return key


def headers(api_key):
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def resolve_type(t):
    t = t.lower().strip()
    return TYPE_ALIASES.get(t, t)


def fmt_time(ts):
    if not ts:
        return "—"
    try:
        if isinstance(ts, (int, float)):
            return datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M")
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return str(ts)[:16]


# =============================================================================
# List commands
# =============================================================================
def list_tasks(api_key, task_type, status_filter=None, page=1, page_size=20):
    endpoint = ENDPOINTS.get(task_type)
    if not endpoint:
        print(f"Unknown type: {task_type}. Options: {', '.join(ENDPOINTS.keys())}")
        sys.exit(1)

    if task_type not in LISTABLE_ENDPOINTS:
        print(f"WARNING: '{task_type}' does not have a list endpoint in the Meshy API.")
        return [], 0

    params = {"page_num": page, "page_size": min(page_size, 50), "sort_by": "-created_at"}
    if status_filter:
        params["status"] = status_filter.upper()

    resp = requests.get(f"{BASE_URL}{endpoint}", headers=headers(api_key), params=params)
    resp.raise_for_status()
    data = resp.json()

    # Meshy returns either a list directly or { "data": [...], "total": N }
    if isinstance(data, list):
        tasks = data
        total = len(tasks)
    elif isinstance(data, dict):
        tasks = data.get("data", data.get("results", []))
        total = data.get("total_count", data.get("total", len(tasks)))
    else:
        tasks = []
        total = 0

    return tasks, total


def cmd_list_meshes(args):
    api_key = get_api_key(args)
    tasks, total = list_tasks(api_key, "image-to-3d", args.status, args.page, args.page_size)

    print(f"\n{'='*80}")
    print(f"  Image-to-3D Meshes (page {args.page}, {len(tasks)} of {total} total)")
    print(f"{'='*80}")
    print(f"  {'#':<4} {'ID':<28} {'Status':<12} {'Created':<18} {'Polys':<8}")
    print(f"  {'—'*4} {'—'*28} {'—'*12} {'—'*18} {'—'*8}")

    for i, t in enumerate(tasks, 1):
        tid = t.get("id", "?")[:26]
        status = t.get("status", "?")
        created = fmt_time(t.get("created_at"))
        polys = t.get("target_polycount", "—")
        print(f"  {i:<4} {tid:<28} {status:<12} {created:<18} {polys:<8}")

    print()
    print(json.dumps(tasks, indent=2))


def cmd_list_animations(args):
    api_key = get_api_key(args)
    tasks, total = list_tasks(api_key, "animations", args.status, args.page, args.page_size)

    print(f"\n{'='*80}")
    print(f"  Animations (page {args.page}, {len(tasks)} of {total} total)")
    print(f"{'='*80}")
    print(f"  {'#':<4} {'ID':<28} {'Status':<12} {'Prompt':<30} {'Created':<18}")
    print(f"  {'—'*4} {'—'*28} {'—'*12} {'—'*30} {'—'*18}")

    for i, t in enumerate(tasks, 1):
        tid = t.get("id", "?")[:26]
        status = t.get("status", "?")
        prompt = (t.get("animation_prompt", "") or "—")[:28]
        created = fmt_time(t.get("created_at"))
        print(f"  {i:<4} {tid:<28} {status:<12} {prompt:<30} {created:<18}")

    print()
    print(json.dumps(tasks, indent=2))


def cmd_list_textures(args):
    api_key = get_api_key(args)
    tasks, total = list_tasks(api_key, "retexture", args.status, args.page, args.page_size)

    print(f"\n{'='*80}")
    print(f"  Textures (page {args.page}, {len(tasks)} of {total} total)")
    print(f"{'='*80}")
    print(f"  {'#':<4} {'ID':<28} {'Status':<12} {'Object':<24} {'Style':<14} {'Created':<18}")
    print(f"  {'—'*4} {'—'*28} {'—'*12} {'—'*24} {'—'*14} {'—'*18}")

    for i, t in enumerate(tasks, 1):
        tid = t.get("id", "?")[:26]
        status = t.get("status", "?")
        obj = (t.get("object_prompt", "") or "—")[:22]
        style = (t.get("art_style", "") or "—")[:12]
        created = fmt_time(t.get("created_at"))
        print(f"  {i:<4} {tid:<28} {status:<12} {obj:<24} {style:<14} {created:<18}")

    print()
    print(json.dumps(tasks, indent=2))


def cmd_list_remeshes(args):
    api_key = get_api_key(args)
    tasks, total = list_tasks(api_key, "remesh", args.status, args.page, args.page_size)

    print(f"\n{'='*80}")
    print(f"  Remeshes (page {args.page}, {len(tasks)} of {total} total)")
    print(f"{'='*80}")
    print(f"  {'#':<4} {'ID':<28} {'Status':<12} {'Topology':<10} {'Polys':<8} {'Created':<18}")
    print(f"  {'—'*4} {'—'*28} {'—'*12} {'—'*10} {'—'*8} {'—'*18}")

    for i, t in enumerate(tasks, 1):
        tid = t.get("id", "?")[:26]
        status = t.get("status", "?")
        topo = t.get("topology", "—")
        polys = t.get("target_polycount", "—")
        created = fmt_time(t.get("created_at"))
        print(f"  {i:<4} {tid:<28} {status:<12} {topo:<10} {polys:<8} {created:<18}")

    print()
    print(json.dumps(tasks, indent=2))


# =============================================================================
# Status
# =============================================================================
def get_task_status(api_key, task_id, task_type):
    endpoint = ENDPOINTS.get(task_type)
    if not endpoint:
        return None
    resp = requests.get(f"{BASE_URL}{endpoint}/{task_id}", headers=headers(api_key))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def cmd_status(args):
    api_key = get_api_key(args)

    if args.latest:
        print("\nFetching latest task from each category...\n")
        for ttype in ENDPOINTS:
            tasks, _ = list_tasks(api_key, ttype, page=1, page_size=1)
            if tasks:
                t = tasks[0]
                status = t.get("status", "?")
                icon = "✓" if status == "SUCCEEDED" else "⏳" if status in ("PENDING", "IN_PROGRESS") else "✗"
                print(f"  {icon} {ttype:<14} {t.get('id', '?')[:26]:<28} {status:<12} {fmt_time(t.get('created_at'))}")
            else:
                print(f"  — {ttype:<14} (none)")
        print()
        return

    if not args.task_id:
        print("ERROR: Provide --task-id or use --latest")
        sys.exit(1)

    # If type specified, check just that endpoint
    if args.type:
        ttype = resolve_type(args.type)
        data = get_task_status(api_key, args.task_id, ttype)
        if data:
            print(json.dumps(data, indent=2))
            return
        print(f"Task {args.task_id} not found as {ttype}")
        sys.exit(1)

    # Otherwise try all endpoints
    for ttype in ENDPOINTS:
        data = get_task_status(api_key, args.task_id, ttype)
        if data:
            print(f"  Type: {ttype}")
            print(json.dumps(data, indent=2))
            return

    print(f"Task {args.task_id} not found in any endpoint.")
    sys.exit(1)


# =============================================================================
# Download
# =============================================================================
def download_file(url, dest):
    print(f"  Downloading → {dest}")
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)


def cmd_download(args):
    api_key = get_api_key(args)
    output_dir = Path(args.output_dir)
    fmt = args.format

    task_ids = []

    if args.latest:
        ttype = resolve_type(args.type or "image-to-3d")
        tasks, _ = list_tasks(api_key, ttype, status_filter="SUCCEEDED", page=1, page_size=1)
        if not tasks:
            print(f"No completed {ttype} tasks found.")
            sys.exit(1)
        task_ids = [tasks[0]["id"]]
        task_type_hint = ttype
    elif args.task_ids:
        task_ids = [t.strip() for t in args.task_ids.split(",") if t.strip()]
        task_type_hint = resolve_type(args.type) if args.type else None
    elif args.task_id:
        task_ids = [args.task_id]
        task_type_hint = resolve_type(args.type) if args.type else None
    else:
        print("ERROR: Provide --task-id, --task-ids, or --latest")
        sys.exit(1)

    for tid in task_ids:
        print(f"\n  Fetching task {tid}...")
        data = None

        if task_type_hint:
            data = get_task_status(api_key, tid, task_type_hint)
        else:
            for ttype in ENDPOINTS:
                data = get_task_status(api_key, tid, ttype)
                if data:
                    break

        if not data:
            print(f"  ✗ Task {tid} not found.")
            continue

        status = data.get("status", "UNKNOWN")
        if status != "SUCCEEDED":
            print(f"  ⚠ Task {tid} status is {status}, cannot download.")
            continue

        model_urls = data.get("model_urls", {})
        url = model_urls.get(fmt) or model_urls.get("glb") or model_urls.get("fbx") or model_urls.get("obj")

        if not url:
            print(f"  ⚠ No downloadable model URL for {tid}.")
            continue

        ext = fmt if fmt in model_urls else "glb"
        dest = output_dir / f"{tid}.{ext}"
        download_file(url, dest)
        print(f"  ✓ Downloaded {tid} → {dest}")

    print()


# =============================================================================
# Retry
# =============================================================================
def cmd_retry(args):
    api_key = get_api_key(args)

    if not args.task_id or not args.type:
        print("ERROR: --task-id and --type are required for retry.")
        sys.exit(1)

    ttype = resolve_type(args.type)
    endpoint = ENDPOINTS.get(ttype)
    if not endpoint:
        print(f"Unknown type: {ttype}")
        sys.exit(1)

    # Fetch original task to get its params
    data = get_task_status(api_key, args.task_id, ttype)
    if not data:
        print(f"Task {args.task_id} not found as {ttype}.")
        sys.exit(1)

    # Build new request body from original params (varies by type)
    body = {}
    if ttype == "image-to-3d":
        for key in ("image_url", "enable_pbr", "topology", "target_polycount", "should_remesh"):
            if key in data:
                body[key] = data[key]
    elif ttype == "remesh":
        for key in ("input_model_url", "topology", "target_polycount", "target_formats"):
            if key in data:
                body[key] = data[key]
    elif ttype == "retexture":
        for key in ("model_url", "object_prompt", "style_prompt", "art_style", "enable_pbr", "resolution"):
            if key in data:
                body[key] = data[key]
    elif ttype == "animations":
        for key in ("input_model_url", "animation_prompt"):
            if key in data:
                body[key] = data[key]

    if not body:
        print(f"Could not extract parameters from task {args.task_id}. Original data:")
        print(json.dumps(data, indent=2))
        sys.exit(1)

    print(f"  Retrying {ttype} with params:")
    print(json.dumps(body, indent=2))

    resp = requests.post(f"{BASE_URL}{endpoint}", headers=headers(api_key), json=body)
    resp.raise_for_status()
    result = resp.json()
    new_id = result.get("result", result.get("id", "?"))
    print(f"\n  ✓ New task submitted: {new_id}")
    print(f"  Check status with: python meshy_api.py status --task-id {new_id} --type {ttype}")


# =============================================================================
# CLI
# =============================================================================
def main():
    parser = argparse.ArgumentParser(description="Meshy.ai API helper")
    parser.add_argument("--api-key", default=None, help="API key (or set MESHY_API_KEY)")
    parser.add_argument("--env-file", default=None, help="Path to .env file")

    sub = parser.add_subparsers(dest="command")

    # List commands
    for cmd_name in ("list-meshes", "list-animations", "list-textures", "list-remeshes"):
        p = sub.add_parser(cmd_name)
        p.add_argument("--status", default=None, help="Filter by status (SUCCEEDED, FAILED, etc.)")
        p.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
        p.add_argument("--page-size", type=int, default=20, help="Results per page (default: 20)")

    # Status
    p = sub.add_parser("status")
    p.add_argument("--task-id", default=None, help="Task ID to check")
    p.add_argument("--type", default=None, help="Task type (image-to-3d, remesh, texture, animate)")
    p.add_argument("--latest", action="store_true", help="Show latest task from each type")

    # Download
    p = sub.add_parser("download")
    p.add_argument("--task-id", default=None, help="Task ID to download")
    p.add_argument("--task-ids", default=None, help="Comma-separated task IDs")
    p.add_argument("--type", default=None, help="Task type hint")
    p.add_argument("--format", default="glb", help="Preferred format (glb, fbx, obj, usdz)")
    p.add_argument("--output-dir", default="./meshy-output", help="Output directory")
    p.add_argument("--latest", action="store_true", help="Download latest completed task")

    # Retry
    p = sub.add_parser("retry")
    p.add_argument("--task-id", required=True, help="Task ID to retry")
    p.add_argument("--type", required=True, help="Task type (image-to-3d, remesh, texture, animate)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    dispatch = {
        "list-meshes": cmd_list_meshes,
        "list-animations": cmd_list_animations,
        "list-textures": cmd_list_textures,
        "list-remeshes": cmd_list_remeshes,
        "status": cmd_status,
        "download": cmd_download,
        "retry": cmd_retry,
    }

    fn = dispatch.get(args.command)
    if fn:
        fn(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

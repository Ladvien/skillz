#!/usr/bin/env python3
"""
render_config.py - Style-based rendering configuration
Auto-tunes Godot rendering settings based on target art style
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class RenderConfig:
    """Rendering configuration for a specific art style."""
    resolution: tuple[int, int]
    antialiasing: str  # none, fxaa, msaa_2x, msaa_4x, msaa_8x
    shadows: str  # none, hard, soft
    ambient_occlusion: bool
    post_process: list[str]
    background: str  # solid_color, gradient, hdri
    background_color: tuple[int, int, int]  # RGB
    camera_fov: float
    camera_distance: float
    lighting_preset: str


RENDER_CONFIGS = {
    "low_poly": RenderConfig(
        resolution=(640, 480),
        antialiasing="none",
        shadows="hard",
        ambient_occlusion=False,
        post_process=["outline"],
        background="solid_color",
        background_color=(220, 220, 225),  # Light neutral gray
        camera_fov=45.0,
        camera_distance=10.0,
        lighting_preset="three_point",
    ),
    
    "pixel_art": RenderConfig(
        resolution=(320, 180),
        antialiasing="none",
        shadows="none",
        ambient_occlusion=False,
        post_process=["pixelate", "dither", "color_quantize"],
        background="solid_color",
        background_color=(100, 120, 140),  # Darker blue-gray
        camera_fov=35.0,
        camera_distance=12.0,
        lighting_preset="flat",
    ),
    
    "realistic": RenderConfig(
        resolution=(1920, 1080),
        antialiasing="msaa_4x",
        shadows="soft",
        ambient_occlusion=True,
        post_process=["bloom", "tonemap", "vignette"],
        background="hdri",
        background_color=(135, 206, 235),  # Sky blue (fallback)
        camera_fov=50.0,
        camera_distance=8.0,
        lighting_preset="natural",
    ),
    
    "cartoon": RenderConfig(
        resolution=(1280, 720),
        antialiasing="fxaa",
        shadows="hard",
        ambient_occlusion=False,
        post_process=["outline", "cel_shade"],
        background="gradient",
        background_color=(180, 220, 255),  # Bright sky blue
        camera_fov=45.0,
        camera_distance=9.0,
        lighting_preset="stylized",
    ),
    
    "anime": RenderConfig(
        resolution=(1280, 720),
        antialiasing="fxaa",
        shadows="soft",
        ambient_occlusion=False,
        post_process=["bloom_soft", "vignette", "color_grade_warm"],
        background="gradient",
        background_color=(255, 230, 210),  # Warm peach
        camera_fov=42.0,
        camera_distance=9.0,
        lighting_preset="ghibli",
    ),
    
    "dead": RenderConfig(
        resolution=(1280, 720),
        antialiasing="msaa_2x",
        shadows="hard",
        ambient_occlusion=True,
        post_process=["desaturate", "vignette_dark", "fog"],
        background="solid_color",
        background_color=(40, 45, 50),  # Dark gray
        camera_fov=55.0,
        camera_distance=10.0,
        lighting_preset="dramatic",
    ),
}


LIGHTING_PRESETS = {
    "three_point": {
        "key_light": {
            "type": "directional",
            "direction": (-0.5, -0.7, -0.5),
            "energy": 1.0,
            "color": (255, 255, 245),
        },
        "fill_light": {
            "type": "directional", 
            "direction": (0.5, -0.3, 0.5),
            "energy": 0.4,
            "color": (200, 210, 255),
        },
        "rim_light": {
            "type": "directional",
            "direction": (0.0, -0.5, 0.8),
            "energy": 0.3,
            "color": (255, 245, 230),
        },
        "ambient": {
            "energy": 0.3,
            "color": (180, 200, 220),
        },
    },
    
    "flat": {
        "key_light": {
            "type": "directional",
            "direction": (0.0, -1.0, -0.2),
            "energy": 0.8,
            "color": (255, 255, 255),
        },
        "ambient": {
            "energy": 0.6,
            "color": (200, 200, 200),
        },
    },
    
    "natural": {
        "key_light": {
            "type": "directional",
            "direction": (-0.4, -0.8, -0.4),
            "energy": 1.2,
            "color": (255, 250, 230),  # Warm sunlight
        },
        "fill_light": {
            "type": "directional",
            "direction": (0.3, -0.2, 0.6),
            "energy": 0.3,
            "color": (180, 200, 255),  # Sky blue fill
        },
        "ambient": {
            "energy": 0.2,
            "color": (150, 180, 210),
        },
    },
    
    "stylized": {
        "key_light": {
            "type": "directional",
            "direction": (-0.5, -0.6, -0.5),
            "energy": 1.0,
            "color": (255, 255, 255),
        },
        "fill_light": {
            "type": "directional",
            "direction": (0.6, -0.4, 0.4),
            "energy": 0.5,
            "color": (180, 200, 255),
        },
        "ambient": {
            "energy": 0.4,
            "color": (200, 210, 230),
        },
    },
    
    "ghibli": {
        "key_light": {
            "type": "directional",
            "direction": (-0.3, -0.7, -0.4),
            "energy": 0.9,
            "color": (255, 250, 235),  # Warm
        },
        "fill_light": {
            "type": "directional",
            "direction": (0.5, -0.3, 0.5),
            "energy": 0.5,
            "color": (220, 230, 255),  # Cool
        },
        "rim_light": {
            "type": "directional",
            "direction": (0.0, -0.3, 0.9),
            "energy": 0.4,
            "color": (255, 240, 220),
        },
        "ambient": {
            "energy": 0.35,
            "color": (200, 210, 200),
        },
    },
    
    "dramatic": {
        "key_light": {
            "type": "directional",
            "direction": (-0.6, -0.5, -0.6),
            "energy": 1.3,
            "color": (220, 200, 180),  # Desaturated warm
        },
        "ambient": {
            "energy": 0.1,
            "color": (80, 90, 100),  # Very dark
        },
    },
}


CAMERA_ANGLES = {
    "three_quarter_front": {
        "position": (5, 3, 5),
        "look_at": (0, 2, 0),
        "description": "3/4 view from front-right, eye level with crown",
    },
    "side": {
        "position": (7, 2, 0),
        "look_at": (0, 2.5, 0),
        "description": "Pure side view, slightly above base",
    },
    "top_angled": {
        "position": (0, 8, 4),
        "look_at": (0, 2, 0),
        "description": "Top-down angled view showing crown structure",
    },
    "low_angle": {
        "position": (4, 0.5, 4),
        "look_at": (0, 3, 0),
        "description": "Low angle looking up at tree",
    },
    "back": {
        "position": (-5, 3, -5),
        "look_at": (0, 2, 0),
        "description": "View from behind",
    },
}


def get_render_config(style: str) -> RenderConfig:
    """Get rendering configuration for a target style."""
    return RENDER_CONFIGS.get(style, RENDER_CONFIGS["low_poly"])


def get_lighting_preset(preset_name: str) -> dict:
    """Get lighting configuration for a preset."""
    return LIGHTING_PRESETS.get(preset_name, LIGHTING_PRESETS["three_point"])


def get_camera_angles(style: str, num_angles: int = 3) -> list[dict]:
    """
    Get appropriate camera angles for a style.
    Returns list of camera configurations.
    """
    # Default angles for most styles
    default_angles = ["three_quarter_front", "side", "top_angled"]
    
    # Style-specific adjustments
    if style == "dead":
        # More dramatic angles for horror trees
        default_angles = ["low_angle", "three_quarter_front", "side"]
    elif style == "pixel_art":
        # More orthographic-feeling angles
        default_angles = ["side", "three_quarter_front", "back"]
    
    return [CAMERA_ANGLES[name] for name in default_angles[:num_angles]]


def generate_godot_config(style: str) -> dict:
    """
    Generate complete Godot configuration dictionary.
    Can be sent to Godot for applying render settings.
    """
    config = get_render_config(style)
    lighting = get_lighting_preset(config.lighting_preset)
    cameras = get_camera_angles(style)
    
    return {
        "viewport": {
            "width": config.resolution[0],
            "height": config.resolution[1],
        },
        "rendering": {
            "antialiasing": config.antialiasing,
            "shadows": config.shadows,
            "ambient_occlusion": config.ambient_occlusion,
        },
        "post_process": config.post_process,
        "background": {
            "type": config.background,
            "color": config.background_color,
        },
        "camera": {
            "fov": config.camera_fov,
            "distance": config.camera_distance,
            "angles": cameras,
        },
        "lighting": lighting,
    }


def list_styles() -> list[str]:
    """Get list of available styles."""
    return list(RENDER_CONFIGS.keys())


def list_lighting_presets() -> list[str]:
    """Get list of available lighting presets."""
    return list(LIGHTING_PRESETS.keys())


if __name__ == "__main__":
    import json
    
    print("Available styles:")
    for style in list_styles():
        config = get_render_config(style)
        print(f"  {style}: {config.resolution[0]}x{config.resolution[1]}, {config.antialiasing}")
    
    print("\nExample config for 'anime' style:")
    config = generate_godot_config("anime")
    print(json.dumps(config, indent=2))

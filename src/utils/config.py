"""Configuration module for Snake game.

All global constants and default configuration are defined here.
Hot-reload is supported via reload_config() for development.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# ─── Window & Display ─────────────────────────────────────────────
WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 600

# ─── Board (Game Area) ────────────────────────────────────────────
GRID_SIZE: int = 30          # Each cell in pixels (originally 20, adjusted to 30 for 20x20 grid = 600px)
BOARD_ROWS: int = 20         # Number of grid rows
BOARD_COLS: int = 20         # Number of grid columns
BOARD_OFFSET_X: int = 0      # X offset from window left (game area starts at 0)
BOARD_OFFSET_Y: int = 0      # Y offset from window top

# The sidebar width: WINDOW_WIDTH - BOARD_COLS * GRID_SIZE
SIDEBAR_WIDTH: int = WINDOW_WIDTH - BOARD_COLS * GRID_SIZE  # 200px

# ─── FPS / Speed ──────────────────────────────────────────────────
INITIAL_FPS: int = 8              # Starting ticks per second
SPEED_INCREMENT: float = 1.10     # Multiplier every speed_up_interval steps
MAX_SPEED_RATIO: float = 1.50     # Cap: max speed ratio over initial
SPEED_UP_INTERVAL: int = 5        # Grow by this many cells between speed-ups

# ─── Colors ───────────────────────────────────────────────────────
COLOR_BG: tuple = (0x1A, 0x1A, 0x2E)       # Deep space blue  #1a1a2e
COLOR_GRID: tuple = (0x25, 0x25, 0x45)      # Subtle grid lines
COLOR_SNAKE_BODY: tuple = (0x4C, 0xAF, 0x50) # Green  #4CAF50
COLOR_SNAKE_HEAD: tuple = (0x66, 0xFF, 0x66) # Brighter green
COLOR_FOOD: tuple = (0xF4, 0x43, 0x36)       # Red    #F44336
COLOR_TEXT: tuple = (0xFF, 0xFF, 0xFF)       # White
COLOR_TEXT_DIM: tuple = (0xAA, 0xAA, 0xAA)   # Gray
COLOR_OVERLAY: tuple = (0, 0, 0, 128)        # Semi-transparent black (RGBA)
COLOR_HIGHLIGHT: tuple = (0xFF, 0xD7, 0x00)  # Gold highlight
COLOR_BORDER: tuple = (0x60, 0x60, 0x80)     # Border color
COLOR_PROGRESS_BAR: tuple = (0x4C, 0xAF, 0x50)
COLOR_PROGRESS_BG: tuple = (0x25, 0x25, 0x45)

# ─── Fonts ────────────────────────────────────────────────────────
FONT_PX_SMALL: int = 8
FONT_PX_MEDIUM: int = 12
FONT_PX_LARGE: int = 16
FONT_PX_TITLE: int = 24

# ─── Paths ────────────────────────────────────────────────────────
ASSET_DIR: str = "src/ui/assets"
STORAGE_PATH: str = "data/highscore.json"


def _default_config() -> Dict[str, Any]:
    """Return the embedded default configuration dictionary."""
    return {
        "window_width": WINDOW_WIDTH,
        "window_height": WINDOW_HEIGHT,
        "grid_size": GRID_SIZE,
        "board_rows": BOARD_ROWS,
        "board_cols": BOARD_COLS,
        "initial_fps": INITIAL_FPS,
        "speed_increment": SPEED_INCREMENT,
        "max_speed_ratio": MAX_SPEED_RATIO,
        "speed_up_interval": SPEED_UP_INTERVAL,
    }


def load_config(config_path: str = "") -> dict:
    """Load configuration from a JSON file, falling back to defaults.

    Args:
        config_path: Path to a custom config JSON file. Empty string means use built-in defaults.

    Returns:
        Merged configuration dictionary. Built-in defaults are overridden by any keys found
        in the JSON file that pass validation.

    Raises:
        OSError when the file exists but cannot be read (logged, not propagated).
    """
    cfg = dict(_default_config())

    if not config_path:
        return cfg

    path = Path(config_path)
    if not path.is_file():
        logger.warning("Config file not found (%s), using defaults.", config_path)
        return cfg

    try:
        with open(path, "r", encoding="utf-8") as fh:
            user_cfg: dict = json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        logger.error("Failed to parse config file %s: %s — using defaults.", path, exc)
        return cfg

    # ── Validation gate ──────────────────────────────────────────
    validated: Dict[str, Any] = {}
    bounds = {
        "window_width":    (200, 1920),
        "window_height":   (200, 1080),
        "grid_size":       (10, 60),
        "board_rows":      (10, 50),
        "board_cols":      (10, 50),
        "initial_fps":     (2, 30),
        "speed_increment": (1.01, 2.0),
        "max_speed_ratio": (1.1, 5.0),
        "speed_up_interval": (1, 30),
    }

    for key, value in user_cfg.items():
        if key not in bounds:
            logger.warning("Unknown config key '%s' — ignored.", key)
            continue

        lo, hi = bounds[key]
        if isinstance(lo, int):
            cast_val = int(value)
        else:
            cast_val = float(value)

        if not (lo <= cast_val <= hi):
            logger.warning(
                "Config key '%s' value %s out of range [%d, %d] — clamped.",
                key, cast_val, lo, hi,
            )
            cast_val = max(lo, min(cast_val, hi))

        validated[key] = cast_val

    cfg.update(validated)
    return cfg


def reload_config() -> dict:
    """Convenience wrapper that calls load_config("") to re-compute built-in defaults.

    Useful during development when inspecting whether parameter changes affect behavior.
    """
    return _default_config()
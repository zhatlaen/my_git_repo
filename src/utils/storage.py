"""Local data persistence for Snake game.

Handles high-score read/write via a simple JSON file in the data/ directory.
All functions accept an explicit ``storage_path`` parameter so that callers
(and tests) can route I/O to arbitrary locations without side effects.
"""

import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

DEFAULT_STORAGE_PATH: str = "data/highscore.json"


def load_highscore(storage_path: str = DEFAULT_STORAGE_PATH) -> int:
    """Read the historical highest score from *storage_path*.

    Returns 0 when the file does not exist or contains invalid data.

    Args:
        storage_path: Path to the JSON file containing {\"high_score\": <int>}.

    Returns:
        Non-negative integer score, or 0 on any failure mode.
    """
    path = Path(storage_path)
    if not path.is_file():
        return 0

    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to read high-score file %s: %s", storage_path, exc)
        return 0

    score = _validate_score(data.get("high_score"))
    return score if score is not None else 0


def save_highscore(score: int, storage_path: str = DEFAULT_STORAGE_PATH) -> bool:
    """Atomically persist *score* as the new high score.

    Uses a write-temp-then-rename strategy to avoid partial writes.
    The parent directory is auto-created if missing.

    Args:
        score: Non-negative integer to record.
        storage_path: Target JSON file path.

    Returns:
        True on success, False on any error (error is also logged).
    """
    if score < 0:
        logger.error("Cannot save negative score (%d).", score)
        return False

    path = Path(storage_path)

    # Ensure parent directory exists
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        logger.error("Cannot create directory %s: %s", path.parent, exc)
        return False

    payload = {"high_score": int(score)}

    try:
        # Write to a temporary file alongside the target, then rename atomically
        fd, tmp_path_str = tempfile.mkstemp(
            prefix=".highscore_", suffix=".tmp", dir=str(path.parent)
        )
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False)

        os.replace(tmp_path_str, str(path))
        logger.info("High score saved: %d → %s", score, path)
        return True

    except OSError as exc:
        logger.error("Failed to save high score %d to %s: %s", score, path, exc)
        # Best-effort cleanup of dangling temp file
        try:
            os.unlink(tmp_path_str)
        except OSError:
            pass
        return False


# ── Helpers ────────────────────────────────────────────────────────

def _validate_score(value: object) -> Optional[int]:
    """Return *value* cast to non-negative int, or None if invalid."""
    try:
        s = int(value)
        return s if s >= 0 else None
    except (TypeError, ValueError):
        return None
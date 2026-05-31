"""Main entry point for the Snake game.

Initializes Pygame, loads configuration and persistent data, assembles all
game objects, and runs the main loop.
"""

from __future__ import annotations

import os
import sys
import pygame

# Ensure the project root is on sys.path so relative imports work
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from src.utils.config import load_config, STORAGE_PATH, WINDOW_WIDTH, WINDOW_HEIGHT
from src.utils.storage import load_highscore, save_highscore
from src.game.controller import GameController, GameState


def main() -> None:
    """Entry point: initialize + main loop + cleanup."""
    # --- Pygame initialization ---
    pygame.init()

    try:
        display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake - Pixel Edition")
    except pygame.error as exc:
        print(f"Failed to create display window: {exc}")
        pygame.quit()
        return

    # --- Configuration & persistent data ---
    cfg = load_config()
    try:
        high_score = load_highscore(STORAGE_PATH)
    except Exception as exc:
        print(f"Warning: could not load high score ({exc}), starting at 0.")
        high_score = 0

    # --- Assemble core objects ---
    controller = GameController(cfg, high_score)

    # --- Data directory creation ---
    storage_dir = os.path.dirname(STORAGE_PATH)
    if storage_dir:
        os.makedirs(storage_dir, exist_ok=True)

    # --- Main loop ---
    running = True
    while running and controller.running:
        # Event handling
        events = pygame.event.get()
        controller.handle_input(events)
        running = controller.running

        # Game logic update (only PLAYING state)
        if controller.state == GameState.PLAYING:
            controller.update()

        # Rendering
        controller.render(display)
        pygame.display.flip()

        # Frame pacing
        controller.get_delta_time()

    # --- Cleanup ---
    # Save final high score
    if controller.score > controller.current_high_score:
        try:
            save_highscore(controller.current_high_score, STORAGE_PATH)
        except Exception as exc:
            print(f"Warning: failed to save high score ({exc})")

    pygame.quit()
    print(f"\nGame ended. Final score: {controller.score} | Best: {controller.current_high_score}")


if __name__ == "__main__":
    main()

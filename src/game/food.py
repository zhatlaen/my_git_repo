"""Food module -- manages food spawning, position tracking, and rendering."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, List, Tuple

import pygame

from src.utils import config

if TYPE_CHECKING:
    from src.game.board import Board
    from src.ui.assets import AssetManager


class Food:
    """Food generation, position management, and rendering."""

    def __init__(self, board: "Board", assets: "AssetManager") -> None:
        """Initialize the food manager.

        Args:
            board: Game board for coordinate conversion and bounds.
            assets: Asset manager for loading food sprites.
        """
        self._board = board
        self._assets = assets
        self._grid_pos: Tuple[int, int] = (0, 0)
        self._pixel_pos: Tuple[int, int] = (0, 0)
        self._anim_frame: int = 0
        self._anim_timer: int = 0

    def respawn(self, snake_segments: List[Tuple[int, int]]) -> None:
        """Respawn food at a random empty grid cell.

        Args:
            snake_segments: Current snake body pixel positions (used for avoidance).
        """
        cell = config.GRID_SIZE
        rows = config.BOARD_ROWS
        cols = config.BOARD_COLS

        snake_grid = set()
        for px, py in snake_segments:
            snake_grid.add((py // cell, px // cell))

        empty: List[Tuple[int, int]] = []
        for r in range(rows):
            for c in range(cols):
                if (r, c) not in snake_grid:
                    empty.append((r, c))

        if not empty:
            return

        self._grid_pos = random.choice(empty)
        row, col = self._grid_pos
        self._pixel_pos = (col * cell, row * cell)

    def get_position(self) -> Tuple[int, int]:
        """Return the food's current pixel coordinate (x, y)."""
        return self._pixel_pos

    def get_grid_pos(self) -> Tuple[int, int]:
        """Return the food's current grid coordinate (row, col)."""
        return self._grid_pos

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the food sprite to the given surface.

        Falls back to a solid color rectangle if the sprite is unavailable.

        Args:
            surface: The pygame Surface to render onto.
        """
        x, y = self._pixel_pos
        cell = config.GRID_SIZE

        try:
            frames = self._assets.get_animation("food_pulse")
            if frames:
                self._anim_timer += 1
                if self._anim_timer >= 8:
                    self._anim_timer = 0
                    self._anim_frame = (self._anim_frame + 1) % len(frames)
                surface.blit(frames[self._anim_frame], (x, y))
                return

            sprite = self._assets.load_sprite("food")
            surface.blit(sprite, (x, y))
        except (KeyError, Exception):
            pad = max(1, cell // 10)
            radius = cell // 2 - pad
            center_x = x + cell // 2
            center_y = y + cell // 2
            pygame.draw.circle(surface, config.COLOR_FOOD, (center_x, center_y), radius)

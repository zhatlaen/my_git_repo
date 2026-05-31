"""Asset manager - programmatic pixel sprite generation and caching.

Generates all game sprites (snake segments, food, decorations) at startup
using pure pygame drawing primitives. No external PNG files are required.
"""

import math
from typing import Dict, List, Optional

import pygame

from src.utils import config


class AssetManager:
    """Generates and caches pixel-art sprites for the game.

    All sprites are created programmatically at the configured `GRID_SIZE`
    and stored in an internal dictionary keyed by name.
    """

    def __init__(self, cell_size: int | None = None) -> None:
        """Initialize the asset manager.

        Args:
            cell_size: Pixel size of one grid cell. Falls back to
                       `config.GRID_SIZE` when *None*.
        """
        self.cell: int = cell_size if cell_size is not None else config.GRID_SIZE
        self._sprites: Dict[str, pygame.Surface] = {}
        self._animations: Dict[str, List[pygame.Surface]] = {}
        self._generate_all()

    # ── Public API ───────────────────────────────────────────────────

    def load_sprite(self, name: str) -> pygame.Surface:
        """Return the cached sprite for *name*.

        Args:
            name: Sprite key such as `'snake_head'` or `'food'`.

        Returns:
            The corresponding `pygame.Surface`.

        Raises:
            KeyError: If the sprite name is unknown.
        """
        return self._sprites[name]

    def get_animation(self, name: str) -> List[pygame.Surface]:
        """Return the animation frame list for *name*."""
        return self._animations.get(name, [])

    # ── Sprite generation ────────────────────────────────────────────

    def _make_surface(self) -> pygame.Surface:
        """Create a transparent surface of one cell size."""
        return pygame.Surface((self.cell, self.cell), pygame.SRCALPHA)

    def _generate_all(self) -> None:
        """Generate every sprite used by the game."""
        c = self.cell
        pad = max(1, c // 10)

        # ── Snake head ──────────────────────────────────────────────
        head = self._make_surface()
        body_color = config.COLOR_SNAKE_HEAD
        pygame.draw.rect(head, body_color, (pad, pad, c - 2 * pad, c - 2 * pad))
        eye_sz = max(2, c // 6)
        pygame.draw.rect(head, (255, 255, 255), (c // 4, c // 4, eye_sz, eye_sz))
        pygame.draw.rect(head, (255, 255, 255), (c - c // 4 - eye_sz, c // 4, eye_sz, eye_sz))
        pygame.draw.rect(head, (0, 0, 0), (c // 4 + 1, c // 4 + 1, eye_sz - 1, eye_sz - 1))
        pygame.draw.rect(head, (0, 0, 0), (c - c // 4 - eye_sz + 1, c // 4 + 1, eye_sz - 1, eye_sz - 1))
        self._sprites["snake_head"] = head

        # ── Snake body segment ──────────────────────────────────────
        seg = self._make_surface()
        seg_color = config.COLOR_SNAKE_BODY
        pygame.draw.rect(seg, seg_color, (pad, pad, c - 2 * pad, c - 2 * pad))
        inner_pad = pad + max(1, c // 10)
        pygame.draw.rect(seg, (0x3C, 0x9F, 0x44),
                         (inner_pad, inner_pad, c - 2 * inner_pad, c - 2 * inner_pad))
        self._sprites["snake_body"] = seg

        # ── Snake tail ──────────────────────────────────────────────
        tail = self._make_surface()
        tail_color = (0x3C, 0x8F, 0x40)
        pygame.draw.rect(tail, tail_color, (pad + 2, pad + 2, c - 2 * pad - 4, c - 2 * pad - 4))
        self._sprites["snake_tail"] = tail

        # ── Food (apple) ────────────────────────────────────────────
        food = self._make_surface()
        food_color = config.COLOR_FOOD
        center = c // 2
        radius = c // 2 - pad
        pygame.draw.circle(food, food_color, (center, center), radius)
        highlight_r = max(1, radius // 3)
        pygame.draw.circle(food, (0xFF, 0x80, 0x80),
                           (center - radius // 3, center - radius // 3), highlight_r)
        stem_w = max(1, c // 12)
        pygame.draw.rect(food, (0x8B, 0x45, 0x13),
                         (center - stem_w // 2, pad - 1, stem_w, c // 5))
        self._sprites["food"] = food

        # ── Particle (for eat animation) ─────────────────────────────
        particle = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.rect(particle, (255, 255, 100), (0, 0, 4, 4))
        self._sprites["particle"] = particle

        # ── Food animation frames (gentle pulse) ─────────────────────
        frames: List[pygame.Surface] = []
        for i in range(4):
            frame = self._make_surface()
            pulse = 1.0 + 0.08 * math.sin(i * math.pi / 2)
            r = int(radius * pulse)
            pygame.draw.circle(frame, food_color, (center, center), r)
            pygame.draw.circle(frame, (0xFF, 0x80, 0x80),
                               (center - r // 3, center - r // 3), highlight_r)
            frames.append(frame)
        self._animations["food_pulse"] = frames

        # ── UI decorations ──────────────────────────────────────────
        border = self._make_surface()
        pygame.draw.rect(border, config.COLOR_BORDER, (0, 0, c, c), 1)
        self._sprites["border_cell"] = border

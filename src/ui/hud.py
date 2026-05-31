"""HUD module -- real-time score, high score and speed progress bar display.

The HUD is rendered in the right sidebar (200px wide by default).
All text uses the PixelFont wrapper; no blurry elements are drawn.
"""

from __future__ import annotations

from typing import Optional

import pygame

from src.utils import config


class HUD:
    """In-game heads-up display for score, best score and speed progress."""

    def __init__(self, pixel_font=None) -> None:
        """Create the HUD renderer.

        Args:
            pixel_font: A ``PixelFont`` instance for rendering text.
                        If *None* a built-in monospace font will be used.
        """
        self._font = pixel_font
        self._score: int = 0
        self._high_score: int = 0
        self._snake_length: int = 3
        self._speed_ratio: float = 1.0
        self._is_new_record: bool = False
        self._record_blink_timer: int = 0

    # -- Data updates -------------------------------------------------------

    def update(
        self,
        score: int,
        high_score: int,
        snake_length: int,
        speed_ratio: float | None = None,
    ) -> None:
        """Update internal state from game data.

        Args:
            score: Current player score.
            high_score: Historical best score.
            snake_length: Current body segment count.
            speed_ratio: Current speed multiplier (defaults to 1.0).
        """
        prev_high = self._high_score
        self._score = score
        self._high_score = high_score
        self._snake_length = snake_length
        if speed_ratio is not None:
            self._speed_ratio = speed_ratio
        self._is_new_record = (score > prev_high and score > 0)

    # -- Rendering ------------------------------------------------------------

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the complete HUD onto the given surface.

        The HUD occupies the rightmost sidebar region of the window.

        Args:
            surface: Main rendering surface.
        """
        sidebar_w = config.SIDEBAR_WIDTH
        win_h = config.WINDOW_HEIGHT

        # Background panel
        panel_rect = pygame.Rect(config.BOARD_COLS * config.GRID_SIZE, 0,
                                 sidebar_w, win_h)
        pygame.draw.rect(surface, (0x14, 0x14, 0x2A), panel_rect)
        pygame.draw.rect(surface, config.COLOR_BORDER, panel_rect, 2)

        ox, oy = panel_rect.left + 12, 20

        self._draw_section_label(surface, "SCORE", ox, oy, color=config.COLOR_TEXT_DIM)
        score_color = config.COLOR_HIGHLIGHT if self._is_new_record else config.COLOR_TEXT
        if self._is_new_record:
            self._record_blink_timer += 1
            if (self._record_blink_timer // 6) % 2 == 0:
                score_color = config.COLOR_FOOD
        self._draw_value(surface, str(self._score), ox, oy + 28, size=config.FONT_PX_LARGE,
                         color=score_color)

        self._draw_section_label(surface, "BEST", ox, oy + 80, color=config.COLOR_TEXT_DIM)
        self._draw_value(surface, str(self._high_score), ox, oy + 108,
                         size=config.FONT_PX_MEDIUM, color=config.COLOR_TEXT)

        self._draw_section_label(surface, "LENGTH", ox, oy + 155, color=config.COLOR_TEXT_DIM)
        max_len_for_bar = 20
        len_pct = min(self._snake_length / max_len_for_bar, 1.0)
        self._draw_value(surface, str(self._snake_length), ox, oy + 183,
                         size=config.FONT_PX_MEDIUM, color=config.COLOR_TEXT)

        self._draw_progress_bar(surface, ox, oy + 205, len_pct,
                                label="SPEED", pct=self._speed_ratio)

        # Controls hint at bottom
        hint_y = win_h - 60
        hints = ["↑↓←→ Move", "P Pause"]
        line_surf = self._font.render(hints[0], size=config.FONT_PX_SMALL,
                                      color=config.COLOR_TEXT_DIM)
        surf2 = self._font.render(hints[1], size=config.FONT_PX_SMALL,
                                   color=config.COLOR_TEXT_DIM)
        w = max(line_surf.get_width(), surf2.get_width())
        surface.blit(line_surf, (ox + (sidebar_w - 24 - w) // 2, hint_y))
        surface.blit(surf2, (ox + (sidebar_w - 24 - w) // 2, hint_y + 16))

    # -- Helpers ------------------------------------------------------------------

    def _draw_section_label(self, surface: pygame.Surface, label: str,
                            x: int, y: int, color: tuple = config.COLOR_TEXT_DIM) -> None:
        """Draw an uppercase section header."""
        surf = self._font.render(label, size=config.FONT_PX_MEDIUM, color=color)
        surface.blit(surf, (x, y))

    def _draw_value(self, surface: pygame.Surface, value: str, x: int, y: int,
                    size: int = 12, color: tuple = config.COLOR_TEXT) -> None:
        surf = self._font.render(value, size=size, color=color)
        surface.blit(surf, (x, y))

    def _draw_progress_bar(self, surface: pygame.Surface, x: int, y: int,
                           pct: float, label: str = "",
                           pct_val: float = 1.0) -> None:
        """Draw a horizontal progress bar with optional labels."""
        bar_w = config.SIDEBAR_WIDTH - 48
        bar_h = 12

        if label:
            lbl = self._font.render(f"{label}: {pct_val:.0%}", size=config.FONT_PX_SMALL,
                                     color=config.COLOR_TEXT_DIM)
            surface.blit(lbl, (x, y))
            y += 18

        rect = pygame.Rect(x, y, bar_w, bar_h)
        pygame.draw.rect(surface, config.COLOR_PROGRESS_BG, rect)

        fill_w = max(0, int(bar_w * min(pct, 1.0)))
        if fill_w > 0:
            fill_rect = pygame.Rect(x, y, fill_w, bar_h)
            pygame.draw.rect(surface, config.COLOR_PROGRESS_BAR, fill_rect)

        pygame.draw.rect(surface, config.COLOR_BORDER, rect, 1)

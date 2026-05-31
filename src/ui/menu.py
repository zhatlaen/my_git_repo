"""Menu module -- start / pause / game-over screen rendering and interaction."""

from __future__ import annotations

from enum import Enum
from typing import List, Optional, Tuple

import pygame

from src.utils import config
from src.utils.pixel_font import PixelFont


class MenuType(Enum):
    """Types of menu screens."""
    START = "start"
    PAUSE = "pause"
    GAME_OVER = "game_over"


class MenuAction(Enum):
    """Actions that can be triggered by menu selection."""
    START_GAME = "start"
    RESUME = "resume"
    RESTART = "restart"
    QUIT = "quit"
    RETURN_TO_MENU = "return_to_menu"
    NONE = "none"


# Option definitions per menu type: (label, action)
_MENU_OPTIONS = {
    MenuType.START: [
        ("Start Game", MenuAction.START_GAME),
        ("Quit", MenuAction.QUIT),
    ],
    MenuType.PAUSE: [
        ("Resume", MenuAction.RESUME),
        ("Restart", MenuAction.RESTART),
        ("Return to Menu", MenuAction.RETURN_TO_MENU),
        ("Quit", MenuAction.QUIT),
    ],
    MenuType.GAME_OVER: [
        ("Play Again", MenuAction.RESTART),
        ("Return to Menu", MenuAction.RETURN_TO_MENU),
        ("Quit", MenuAction.QUIT),
    ],
}


class Menu:
    """Renders and handles input for start/pause/game-over menu screens."""

    def __init__(self, pixel_font: PixelFont) -> None:
        """Initialize the menu renderer.

        Args:
            pixel_font: PixelFont instance for text rendering.
        """
        self._font = pixel_font
        self._selected_index: int = 0
        self._menu_type: MenuType = MenuType.START
        self._score: int = 0
        self._high_score: int = 0
        self._is_new_record: bool = False

    def set_menu_type(self, menu_type: MenuType) -> None:
        """Switch to a different menu type and reset selection."""
        self._menu_type = menu_type
        self._selected_index = 0

    def set_score_data(self, score: int, high_score: int, is_new_record: bool) -> None:
        """Provide score data for the game-over screen.

        Args:
            score: Final score of the current game.
            high_score: Historical high score.
            is_new_record: Whether the current score broke the record.
        """
        self._score = score
        self._high_score = high_score
        self._is_new_record = is_new_record

    def handle_input(self, events: List[pygame.event.Event]) -> MenuAction:
        """Process input events for the current menu.

        Args:
            events: List of pygame events.

        Returns:
            The triggered MenuAction, or MenuAction.NONE if nothing happened.
        """
        options = _MENU_OPTIONS[self._menu_type]
        num_options = len(options)

        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_UP:
                self._selected_index = (self._selected_index - 1) % num_options
            elif event.key == pygame.K_DOWN:
                self._selected_index = (self._selected_index + 1) % num_options
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                _, action = options[self._selected_index]
                return action

        return MenuAction.NONE

    def draw(self, surface: pygame.Surface, background: Optional[pygame.Surface] = None) -> None:
        """Draw the menu overlay onto the given surface.

        Args:
            surface: Main rendering surface.
            background: Optional background snapshot for pause overlay.
        """
        win_w = config.WINDOW_WIDTH
        win_h = config.WINDOW_HEIGHT

        overlay = pygame.Surface((win_w, win_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        if self._menu_type == MenuType.START:
            self._draw_start_menu(surface)
        elif self._menu_type == MenuType.PAUSE:
            self._draw_pause_menu(surface)
        elif self._menu_type == MenuType.GAME_OVER:
            self._draw_game_over_menu(surface)

    def _draw_start_menu(self, surface: pygame.Surface) -> None:
        """Draw the start menu screen."""
        win_w = config.WINDOW_WIDTH
        center_x = win_w // 2

        title_surf = self._font.render("SNAKE", size=config.FONT_PX_TITLE * 2,
                                        color=(0x4C, 0xAF, 0x50))
        title_rect = title_surf.get_rect(center=(center_x, 180))
        surface.blit(title_surf, title_rect)

        subtitle = self._font.render("Pixel Edition", size=config.FONT_PX_LARGE,
                                      color=config.COLOR_TEXT_DIM)
        sub_rect = subtitle.get_rect(center=(center_x, 230))
        surface.blit(subtitle, sub_rect)

        decor_line = pygame.Surface((200, 2), pygame.SRCALPHA)
        pygame.draw.rect(decor_line, config.COLOR_SNAKE_BODY, (0, 0, 200, 2))
        surface.blit(decor_line, (center_x - 100, 255))

        self._draw_options(surface, center_x, 320)

        hint = self._font.render("Press ENTER to start", size=config.FONT_PX_MEDIUM,
                                  color=config.COLOR_TEXT_DIM)
        hint_rect = hint.get_rect(center=(center_x, 520))
        surface.blit(hint, hint_rect)

    def _draw_pause_menu(self, surface: pygame.Surface) -> None:
        """Draw the pause menu overlay."""
        win_w = config.WINDOW_WIDTH
        center_x = win_w // 2

        title = self._font.render("PAUSED", size=config.FONT_PX_TITLE,
                                   color=config.COLOR_HIGHLIGHT)
        title_rect = title.get_rect(center=(center_x, 180))
        surface.blit(title, title_rect)

        self._draw_options(surface, center_x, 260)

    def _draw_game_over_menu(self, surface: pygame.Surface) -> None:
        """Draw the game-over screen with score data."""
        win_w = config.WINDOW_WIDTH
        center_x = win_w // 2

        title = self._font.render("GAME OVER", size=config.FONT_PX_TITLE,
                                   color=config.COLOR_FOOD)
        title_rect = title.get_rect(center=(center_x, 150))
        surface.blit(title, title_rect)

        score_color = config.COLOR_HIGHLIGHT if self._is_new_record else config.COLOR_TEXT
        score_text = self._font.render(f"Score: {self._score}",
                                        size=config.FONT_PX_LARGE, color=score_color)
        score_rect = score_text.get_rect(center=(center_x, 210))
        surface.blit(score_text, score_rect)

        high_text = self._font.render(f"Best: {self._high_score}",
                                       size=config.FONT_PX_MEDIUM, color=config.COLOR_TEXT_DIM)
        high_rect = high_text.get_rect(center=(center_x, 245))
        surface.blit(high_text, high_rect)

        if self._is_new_record:
            record_surf = self._font.render("NEW RECORD!", size=config.FONT_PX_LARGE,
                                             color=config.COLOR_HIGHLIGHT)
            record_rect = record_surf.get_rect(center=(center_x, 280))
            surface.blit(record_surf, record_rect)

        option_y = 340 if self._is_new_record else 310
        self._draw_options(surface, center_x, option_y)

    def _draw_options(self, surface: pygame.Surface, center_x: int, start_y: int) -> None:
        """Draw menu options with highlight on the selected item."""
        options = _MENU_OPTIONS[self._menu_type]
        option_spacing = 50

        for i, (label, _) in enumerate(options):
            y = start_y + i * option_spacing
            is_selected = (i == self._selected_index)

            color = config.COLOR_HIGHLIGHT if is_selected else config.COLOR_TEXT
            text_surf = self._font.render(label, size=config.FONT_PX_LARGE, color=color)
            text_rect = text_surf.get_rect(center=(center_x, y))
            surface.blit(text_surf, text_rect)

            if is_selected:
                pad_x = 16
                pad_y = 6
                border_rect = pygame.Rect(
                    text_rect.left - pad_x,
                    text_rect.top - pad_y,
                    text_rect.width + 2 * pad_x,
                    text_rect.height + 2 * pad_y,
                )
                pygame.draw.rect(surface, config.COLOR_HIGHLIGHT, border_rect, 2)

                arrow = self._font.render(">", size=config.FONT_PX_LARGE,
                                           color=config.COLOR_HIGHLIGHT)
                arrow_rect = arrow.get_rect(midright=(text_rect.left - pad_x - 4, y))
                surface.blit(arrow, arrow_rect)

"""Controller module -- game state machine, input dispatch, update/render scheduling.

Manages the four game states (START / PLAYING / PAUSED / GAME_OVER) and wires
together Snake, Food, Board, HUD, Menu, and AssetManager.
"""

from __future__ import annotations

from enum import Enum
from typing import List, Optional

import pygame

from src.game.board import Board
from src.game.food import Food
from src.game.snake import Snake
from src.ui.assets import AssetManager
from src.ui.hud import HUD
from src.ui.menu import Menu, MenuType, MenuAction
from src.utils import config


class GameState(Enum):
    """Possible game states."""
    START = "start"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class GameController:
    """Central game controller: state machine + input dispatch + loop scheduling."""

    def __init__(self, cfg: dict | None = None, high_score: int = 0) -> None:
        """Initialize the game controller.

        Args:
            cfg: Configuration dictionary. If *None*, defaults from ``src.utils.config`` are used.
            high_score: Historical best score loaded from storage.
        """
        self._cfg = cfg if cfg is not None else {}

        # Initialize PyGame fonts before creating components that need them
        try:
            pygame.font.init()
        except pygame.error:
            pass

        # Create core objects
        self._board = Board(self._cfg)
        self._assets = AssetManager(self._cfg.get("grid_size"))
        self._pixel_font = self._create_pixel_font()

        cell_size = self._board.cell
        start_grid = (self._board.rows // 2, self._board.cols // 4)
        self._snake = Snake(start_grid, cell_size, initial_length=3)
        self._food = Food(self._board, self._assets)
        self._hud = HUD(self._pixel_font)
        self._menu = Menu(self._pixel_font)

        self._high_score: int = high_score
        self._current_high_score: int = high_score
        self._score: int = 0
        self._fps: float = float(self._cfg.get("initial_fps", config.INITIAL_FPS))
        self._speed_increment: float = self._cfg.get("speed_increment", config.SPEED_INCREMENT)
        self._max_speed_ratio: float = self._cfg.get("max_speed_ratio", config.MAX_SPEED_RATIO)
        self._speed_up_interval: int = self._cfg.get("speed_up_interval", config.SPEED_UP_INTERVAL)
        self._total_growth: int = 0

        self._state: GameState = GameState.START
        self._clock: pygame.time.Clock = pygame.time.Clock()
        self._move_timer: int = 0
        self._move_interval: int = max(1, int(60 / self._fps))
        self._shake_timer: int = 0
        self._shake_intensity: int = 0
        self._particles: list = []
        self._eating_anim: int = 0

        self._running: bool = True

    def _create_pixel_font(self):
        """Create a PixelFont instance for menu/HUD rendering."""
        from src.utils.pixel_font import PixelFont
        return PixelFont(default_size=config.FONT_PX_MEDIUM)

    # -- State management -----------------------------------------------------

    @property
    def state(self) -> GameState:
        return self._state

    @property
    def running(self) -> bool:
        return self._running

    @property
    def score(self) -> int:
        return self._score

    @property
    def current_high_score(self) -> int:
        return self._current_high_score

    @property
    def snake(self) -> Snake:
        return self._snake

    @property
    def food(self) -> Food:
        return self._food

    @property
    def board(self) -> Board:
        return self._board

    def set_state(self, new_state: GameState) -> None:
        """Transition to a new game state."""
        prev_state = self._state
        self._state = new_state

        if new_state == GameState.START:
            self._menu.set_menu_type(MenuType.START)
        elif new_state == GameState.PAUSED:
            self._menu.set_menu_type(MenuType.PAUSE)
        elif new_state == GameState.GAME_OVER:
            self._is_new_record = self._score > self._current_high_score
            if self._is_new_record:
                self._current_high_score = self._score
            self._menu.set_menu_type(MenuType.GAME_OVER)
            self._menu.set_score_data(self._score, self._current_high_score, self._is_new_record)
            self._shake_timer = 30
            self._shake_intensity = 5

        if new_state == GameState.PLAYING:
            self._move_timer = 0
            self._move_interval = max(1, int(60 / self._fps))

    def _reset_game(self) -> None:
        """Reset all game objects to initial state."""
        cell_size = self._board.cell
        start_grid = (self._board.rows // 2, self._board.cols // 4)
        self._snake.reset(start_grid, initial_length=3)
        self._score = 0
        self._fps = float(self._cfg.get("initial_fps", config.INITIAL_FPS))
        self._total_growth = 0
        self._particles = []
        self._eating_anim = 0
        self._food.respawn(self._snake.get_segments())
        self._hud.update(0, self._current_high_score, 3, speed_ratio=1.0)

    # -- Input handling -------------------------------------------------------

    def handle_input(self, events: List[pygame.event.Event]) -> None:
        """Process input events according to the current game state.

        Args:
            events: List of pygame events from pygame.event.get().
        """
        for event in events:
            if event.type == pygame.QUIT:
                self._running = False
                return

            if self._state == GameState.START:
                self._handle_start_input(event)
            elif self._state == GameState.PLAYING:
                self._handle_playing_input(event)
            elif self._state == GameState.PAUSED:
                self._handle_paused_input(event)
            elif self._state == GameState.GAME_OVER:
                self._handle_gameover_input(event)

    def _handle_start_input(self, event: pygame.event.Event) -> None:
        action = self._menu.handle_input([event])
        if action == MenuAction.START_GAME:
            self._reset_game()
            self.set_state(GameState.PLAYING)
        elif action == MenuAction.QUIT:
            self._running = False

    def _handle_playing_input(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        key_map = {
            pygame.K_UP: Snake.DIR_UP,
            pygame.K_DOWN: Snake.DIR_DOWN,
            pygame.K_LEFT: Snake.DIR_LEFT,
            pygame.K_RIGHT: Snake.DIR_RIGHT,
            pygame.K_w: Snake.DIR_UP,
            pygame.K_s: Snake.DIR_DOWN,
            pygame.K_a: Snake.DIR_LEFT,
            pygame.K_d: Snake.DIR_RIGHT,
        }

        if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
            self.set_state(GameState.PAUSED)
            return

        new_dir = key_map.get(event.key)
        if new_dir:
            self._snake.set_direction(new_dir)

    def _handle_paused_input(self, event: pygame.event.Event) -> None:
        action = self._menu.handle_input([event])
        if action == MenuAction.RESUME:
            self.set_state(GameState.PLAYING)
        elif action == MenuAction.RESTART:
            self._reset_game()
            self.set_state(GameState.PLAYING)
        elif action == MenuAction.RETURN_TO_MENU:
            self.set_state(GameState.START)
        elif action == MenuAction.QUIT:
            self._running = False

    def _handle_gameover_input(self, event: pygame.event.Event) -> None:
        action = self._menu.handle_input([event])
        if action == MenuAction.RESTART:
            self._reset_game()
            self.set_state(GameState.PLAYING)
        elif action == MenuAction.RETURN_TO_MENU:
            self.set_state(GameState.START)
        elif action == MenuAction.QUIT:
            self._running = False

    # -- Game logic update ---------------------------------------------------

    def update(self) -> None:
        """Execute one frame of game logic (only valid in PLAYING state)."""
        if self._state != GameState.PLAYING:
            return

        # Move timer (fixed-timestep snake movement)
        self._move_timer += 1
        if self._move_timer < self._move_interval:
            return
        self._move_timer = 0

        # Move snake
        success = self._snake.move()
        if not success:
            self.set_state(GameState.GAME_OVER)
            return

        # Collision detection
        bounds = self._board.get_bounds_rect()
        collision = self._snake.check_collision(bounds)
        if collision != "none":
            self.set_state(GameState.GAME_OVER)
            return

        # Food collision
        head_px = self._snake.get_head_pos()
        food_px = self._food.get_position()
        if head_px == food_px:
            self._snake.grow()
            self._score += 10
            self._total_growth += 1

            # Speed increase every SPEED_UP_INTERVAL growth
            if self._total_growth % self._speed_up_interval == 0:
                ratio = self._fps / max(config.INITIAL_FPS, 1)
                if ratio < self._max_speed_ratio:
                    self._fps = min(self._fps * self._speed_increment,
                                    config.INITIAL_FPS * self._max_speed_ratio)
                    self._move_interval = max(1, int(60 / self._fps))

            # Respawn food
            self._food.respawn(self._snake.get_segments())

            # Update HUD
            speed_pct = self._fps / max(config.INITIAL_FPS, 1)
            self._hud.update(self._score, self._current_high_score,
                            self._snake.length, speed_ratio=speed_pct)

    # -- Rendering ------------------------------------------------------------

    def render(self, surface: pygame.Surface) -> None:
        """Draw the complete game scene onto the given surface.

        Render order: background -> snake -> food -> HUD -> menu overlay.

        Args:
            surface: Main display surface.
        """
        # Screen shake effect
        shake_x, shake_y = 0, 0
        if self._shake_timer > 0:
            self._shake_timer -= 1
            intensity = self._shake_intensity * (self._shake_timer / 30)
            import random
            shake_x = random.randint(-intensity, intensity)
            shake_y = random.randint(-intensity, intensity)
            surface.fill(config.COLOR_BG)
            surface.blit(surface, (shake_x, shake_y),
                        pygame.Rect(0, 0, surface.get_width(), surface.get_height()))
        else:
            surface.fill(config.COLOR_BG)

        # Draw board background with grid
        self._board.draw_background(surface)

        # Draw snake body segments
        segs = self._snake.get_segments()
        for i, seg_px in enumerate(reversed(segs)):
            x, y = seg_px
            if i == 0:
                try:
                    sprite = self._assets.load_sprite("snake_head")
                    surface.blit(sprite, (x, y))
                except KeyError:
                    pad = max(1, config.GRID_SIZE // 10)
                    pygame.draw.rect(surface, config.COLOR_SNAKE_HEAD,
                                   (x + pad, y + pad, config.GRID_SIZE - 2*pad, config.GRID_SIZE - 2*pad))
            elif i == len(segs) - 1:
                try:
                    sprite = self._assets.load_sprite("snake_tail")
                    surface.blit(sprite, (x, y))
                except KeyError:
                    pygame.draw.rect(surface, config.COLOR_SNAKE_BODY,
                                   (x+1, y+1, config.GRID_SIZE-2, config.GRID_SIZE-2))
            else:
                try:
                    sprite = self._assets.load_sprite("snake_body")
                    surface.blit(sprite, (x, y))
                except KeyError:
                    pygame.draw.rect(surface, config.COLOR_SNAKE_BODY,
                                   (x+1, y+1, config.GRID_SIZE-2, config.GRID_SIZE-2))

        # Draw food
        self._food.draw(surface)

        # Draw HUD (sidebar)
        self._hud.draw(surface)

        # Draw menu overlay if not playing
        if self._state != GameState.PLAYING:
            self._menu.draw(surface)

    # -- Game loop control ----------------------------------------------------

    def get_delta_time(self) -> float:
        """Return the time since last frame in seconds."""
        return self._clock.tick(self._fps) / 1000.0

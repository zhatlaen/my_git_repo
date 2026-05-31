"""Board module - game area management and coordinate conversion.

Handles grid-to-pixel and pixel-to-grid transformations, boundary checking,
and background rendering for the Snake game play area.
"""

import pygame

from src.utils import config


class Board:
    """Manages the game area grid and coordinate conversions.

    The board occupies a fixed rectangular region of the screen. All game
    logic operates on grid coordinates; rendering converts to pixel space.
    """

    def __init__(self, cfg: dict | None = None) -> None:
        """Initialize the board from a configuration dictionary.

        Args:
            cfg: Config dict with keys `grid_size`, `board_rows`,
                 `board_cols`. Falls back to module-level constants when *None*.
        """
        self.cell: int = (cfg or {}).get("grid_size", config.GRID_SIZE)
        self.rows: int = (cfg or {}).get("board_rows", config.BOARD_ROWS)
        self.cols: int = (cfg or {}).get("board_cols", config.BOARD_COLS)
        self.offset_x: int = (cfg or {}).get("board_offset_x", config.BOARD_OFFSET_X)
        self.offset_y: int = (cfg or {}).get("board_offset_y", config.BOARD_OFFSET_Y)
        self.width_px: int = self.cols * self.cell
        self.height_px: int = self.rows * self.cell

    # ── Coordinate conversion ───────────────────────────────────────

    def to_pixel(self, grid_pos: tuple[int, int]) -> tuple[int, int]:
        """Convert grid `(row, col)` to top-left pixel `(x, y)`."""
        row, col = grid_pos
        return (self.offset_x + col * self.cell,
                self.offset_y + row * self.cell)

    def to_grid(self, pixel_pos: tuple[int, int]) -> tuple[int, int]:
        """Convert pixel `(x, y)` to grid `(row, col)` (floor division)."""
        px, py = pixel_pos
        col = (px - self.offset_x) // self.cell
        row = (py - self.offset_y) // self.cell
        return (row, col)

    def is_out_of_bounds(self, pixel_pos: tuple[int, int]) -> bool:
        """Return *True* when *pixel_pos* lies outside the playable area."""
        px, py = pixel_pos
        left, top, right, bottom = self.get_bounds_rect()
        return px < left or px >= right or py < top or py >= bottom

    def get_bounds_rect(self) -> tuple[int, int, int, int]:
        """Return `(left, top, right, bottom)` pixel bounds of the board."""
        return (self.offset_x,
                self.offset_y,
                self.offset_x + self.width_px,
                self.offset_y + self.height_px)

    # ── Rendering helpers ───────────────────────────────────────────

    def draw_background(self, surface: pygame.Surface) -> None:
        """Draw the board background with subtle grid lines.

        Args:
            surface: The target surface to draw onto.
        """
        bg_rect = pygame.Rect(self.offset_x, self.offset_y,
                              self.width_px, self.height_px)
        pygame.draw.rect(surface, config.COLOR_BG, bg_rect)

        for row in range(self.rows + 1):
            y = self.offset_y + row * self.cell
            pygame.draw.line(surface, config.COLOR_GRID,
                             (self.offset_x, y),
                             (self.offset_x + self.width_px, y))

        for col in range(self.cols + 1):
            x = self.offset_x + col * self.cell
            pygame.draw.line(surface, config.COLOR_GRID,
                             (x, self.offset_y),
                             (x, self.offset_y + self.height_px))

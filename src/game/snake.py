"""Snake entity module -- manages movement, growth, and collision detection.

The snake stores its body as a list of **grid** positions (row, col).
Pixel coordinates are derived on demand via *cell_size*.

Coordinate convention:
  - row  -> y axis (vertical)
  - col  -> x axis (horizontal)
  - pixel pos = (col * cell_size, row * cell_size)
"""

from __future__ import annotations

from typing import List, Tuple


class Snake:
    """Snake entity that manages movement, growth, and collision detection."""

    DIR_UP: Tuple[int, int] = (-1, 0)
    DIR_DOWN: Tuple[int, int] = (1, 0)
    DIR_LEFT: Tuple[int, int] = (0, -1)
    DIR_RIGHT: Tuple[int, int] = (0, 1)

    def __init__(
        self,
        start_pos: Tuple[int, int],
        cell_size: int,
        initial_length: int = 3,
    ) -> None:
        """Initialize the snake.

        Args:
            start_pos: Starting grid coordinate (row, col) for the head.
            cell_size: Pixel size of each grid cell.
            initial_length: Number of body segments at spawn (including head).
        """
        self.cell_size: int = cell_size
        self._direction: Tuple[int, int] = self.DIR_RIGHT
        self._pending_direction: Tuple[int, int] = self.DIR_RIGHT
        self._grow_pending: int = 0

        head_row, head_col = start_pos
        self._body: List[Tuple[int, int]] = []
        for i in range(initial_length):
            self._body.append((head_row, head_col - i))

    def set_direction(self, new_dir: Tuple[int, int]) -> bool:
        """Set movement direction. 180-degree reversals are rejected.

        Args:
            new_dir: Direction vector, e.g. (0, 1) for right.

        Returns:
            True if accepted, False if rejected.
        """
        dr, dc = new_dir
        cur_r, cur_c = self._direction
        if dr + cur_r == 0 and dc + cur_c == 0 and (dr != 0 or dc != 0):
            return False
        self._pending_direction = new_dir
        return True

    @property
    def direction(self) -> Tuple[int, int]:
        """Return the current movement direction vector."""
        return self._direction

    def move(self) -> bool:
        """Move one grid step in the current direction.

        Returns:
            True if the move was executed.
        """
        self._direction = self._pending_direction
        head_row, head_col = self._body[0]
        dr, dc = self._direction
        new_head = (head_row + dr, head_col + dc)

        self._body.insert(0, new_head)

        if self._grow_pending > 0:
            self._grow_pending -= 1
        else:
            self._body.pop()

        return True

    def grow(self) -> None:
        """Schedule growth: tail will not be removed on the next move."""
        self._grow_pending += 1

    def check_collision(self, bounds: Tuple[int, int, int, int]) -> str:
        """Check for wall or self collision.

        Args:
            bounds: Game area boundary (left, top, right, bottom) in pixel coords.

        Returns:
            'wall' if head is out of bounds,
            'self' if head overlaps a body segment,
            'none' if no collision.
        """
        left, top, right, bottom = bounds
        head_px, head_py = self.get_head_pos()
        cell = self.cell_size

        if head_px < left or head_py < top:
            return "wall"
        if head_px + cell > right or head_py + cell > bottom:
            return "wall"

        head_grid = self._body[0]
        for segment in self._body[1:]:
            if segment == head_grid:
                return "self"

        return "none"

    def get_segments(self) -> List[Tuple[int, int]]:
        """Return all body segment pixel coordinates (x, y) from head to tail."""
        c = self.cell_size
        return [(col * c, row * c) for row, col in self._body]

    def get_head_pos(self) -> Tuple[int, int]:
        """Return the snake head pixel coordinate (x, y)."""
        row, col = self._body[0]
        c = self.cell_size
        return (col * c, row * c)

    def get_grid_positions(self) -> List[Tuple[int, int]]:
        """Return all body grid positions as (row, col) tuples."""
        return list(self._body)

    @property
    def length(self) -> int:
        """Current number of body segments."""
        return len(self._body)

    def reset(self, start_pos: Tuple[int, int], initial_length: int = 3) -> None:
        """Reset the snake to its initial state.

        Args:
            start_pos: New starting grid coordinate for the head.
            initial_length: Number of body segments.
        """
        head_row, head_col = start_pos
        self._body = []
        for i in range(initial_length):
            self._body.append((head_row, head_col - i))
        self._direction = self.DIR_RIGHT
        self._pending_direction = self.DIR_RIGHT
        self._grow_pending = 0

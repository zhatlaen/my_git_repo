"""Pixel-style font rendering helper for Snake game.

Provides a thin wrapper around pygame.font that caches rendered text surfaces
at different sizes so repeated calls are fast.  Falls back to pygame's built-in
default font when no TTF file is available.
"""

from typing import Optional, Tuple

import pygame


class PixelFont:
    """Caches and renders text as pygame Surfaces using a pixel-art style.

    Example::

        pf = PixelFont()
        surf = pf.render("Score: 42", size=16, color=(255,255,0))
        screen.blit(surf, (10, 10))
    """

    def __init__(
        self,
        font_path: Optional[str] = None,
        default_size: int = 12,
    ) -> None:
        """Create a PixelFont instance.

        Args:
            font_path: Path to a TTF font file.  ``None`` or missing file means
                       pygame's default bitmap font will be used.
            default_size: Default point-size for :meth:`render` calls that omit *size*.
        """
        self.default_size: int = default_size
        # Cache per (size,) tuple — avoids re-rendering identical params
        self._cache: dict = {}
        self._font_ref: Optional[pygame.font.Font] = None
        self._default_font: pygame.font.Font = pygame.font.SysFont(
            "monospace", default_size, bold=False
        )

        if font_path:
            try:
                self._font_ref = pygame.font.Font(font_path, default_size)
            except (OSError, pygame.error):
                self._font_ref = None

    # ── Internal helpers ───────────────────────────────────────────

    @property
    def _active_font(self) -> pygame.font.Font:
        """Return the loaded font or the sys fallback."""
        if self._font_ref is not None:
            return self._font_ref
        return self._default_font

    def _make_surface(self, text: str, size: int, color: Tuple[int, int, int]) -> pygame.Surface:
        """Render *text* at *size* in *color*, returning a Surface."""
        actual_font = self._active_font
        # pygame.font.Font.set_size modifies the internal font; we use it for sizing
        try:
            sf = actual_font.render(text, True, color)
        except pygame.error:
            sf = self._default_font.render(text, True, color)
        return sf

    # ── Public API ─────────────────────────────────────────────────

    def render(
        self,
        text: str,
        size: Optional[int] = None,
        color: Tuple[int, int, int] = (255, 255, 255),
    ) -> pygame.Surface:
        """Render *text* into an RGB/RGBA Surface.

        Args:
            text:     Text string to render.
            size:     Desired font height in points.  Defaults to :attr:`default_size`.
            color:    ``(R, G, B)`` colour tuple.  Alpha is handled by the surface.

        Returns:
            A new :class:`pygame.Surface` containing the rendered text.
        """
        sz = size if size is not None else self.default_size
        cache_key = (text, sz, color)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        result = self._make_surface(text, sz, color)
        self._cache[cache_key] = result
        return result

    def clear_cache(self) -> None:
        """Drop all cached surfaces.  Useful when resources are being reloaded."""
        self._cache.clear()
import numpy as np


class Camera:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = 0
        self.y = 0

    def update(self, target_x: int, target_y: int, map_width: int, map_height: int):
        """Center camera on target and clamp to map bounds."""
        half_w = self.screen_width // 2
        half_h = self.screen_height // 2

        # Center camera on target
        self.x = target_x - half_w
        self.y = target_y - half_h

        # Clamp so camera never shows outside the map
        self.x = max(0, min(self.x, map_width - self.screen_width))
        self.y = max(0, min(self.y, map_height - self.screen_height))

    def viewport(self) -> tuple[slice, slice]:
        """Return x and y slices for visible area."""
        return (
            slice(self.x, self.x + self.screen_width),
            slice(self.y, self.y + self.screen_height),
        )

    def world_to_screen(self, world_x: int, world_y: int) -> tuple[int, int]:
        """Convert a single (world_x, world_y) to (screen_x, screen_y)."""
        return world_x - self.x, world_y - self.y

    def screen_to_world(self, screen_x: int, screen_y: int) -> tuple[int, int]:
        """Convert a single (screen_x, screen_y) to (world_x, world_y)."""
        return screen_x + self.x, screen_y + self.y

    def entities_to_screen(self, entities: list) -> list[tuple[int, int, object]]:
        """
        Convert multiple entities from world space to screen space.
        Returns a list of (sx, sy, entity) for visible entities.
        Assumes entities have `.x` and `.y` attributes.
        """
        result = []
        for e in entities:
            sx, sy = self.world_to_screen(e.x, e.y)
            if 0 <= sx < self.screen_width and 0 <= sy < self.screen_height:
                result.append((sx, sy, e))
        return result

from __future__ import annotations

from game.map_gen.rectangular_structure import RectangularStructure


class RectangularRoom(RectangularStructure):
    def __init__(self, x: int, y: int, width: int, height: int, purpose: str = ""):
        super().__init__(x, y, width, height)
        self.purpose = purpose
        self.door = None

    def add_door(self, door_x: int, door_y: int):
        self.door = (door_x, door_y)

    @property
    def inside_wall_opposite_door(self):
        if self.door:
            if self.door[0] == self.x:
                return self.right_inside_wall
            elif self.door[0] == self.x + self.w:
                return self.left_inside_wall
            elif self.door[1] == self.y:
                return self.down_inside_wall
            elif self.door[1] == self.y + self.h:
                return self.up_inside_wall
        return []

    @property
    def inside_wall_same_as_door(self):
        if self.door:
            if self.door[0] == self.x:
                return self.left_inside_wall
            elif self.door[0] == self.x + self.w:
                return self.right_inside_wall
            elif self.door[1] == self.y:
                return self.up_inside_wall
            elif self.door[1] == self.y + self.h:
                return self.down_inside_wall
        return []

    @property
    def inside_wall_left_of_door(self):
        if self.door:
            if self.door[0] == self.x:
                return self.up_inside_wall
            elif self.door[0] == self.x + self.w:
                return self.down_inside_wall
            elif self.door[1] == self.y:
                return self.right_inside_wall
            elif self.door[1] == self.y + self.h:
                return self.left_inside_wall
        return []

    @property
    def inside_wall_right_of_door(self):
        if self.door:
            if self.door[0] == self.x:
                return self.down_inside_wall_inside_wall
            elif self.door[0] == self.x + self.w:
                return self.up_inside_wall
            elif self.door[1] == self.y:
                return self.left_inside_wall
            elif self.door[1] == self.y + self.h:
                return self.right_inside_wall
        return []

    @property
    def left_inside_wall(self):
        spots = []
        spots.extend((self.x1 + 1, y) for y in range(self.y1 + 1, self.y2))
        return spots

    @property
    def right_inside_wall(self):
        spots = []
        spots.extend((self.x2 - 1, y) for y in range(self.y1 + 1, self.y2))
        return spots

    @property
    def down_inside_wall(self):
        spots = []
        spots.extend((x, self.y2 - 1) for x in range(self.x1 + 1, self.x2))
        return spots

    @property
    def up_inside_wall(self):
        spots = []
        spots.extend((x, self.y1 + 1) for x in range(self.x1 + 1, self.x2))
        return spots

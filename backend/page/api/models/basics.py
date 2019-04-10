from __future__ import annotations


class Vec2D:
    """
    A vector/point in a 2D space
    """
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    """
    Adds the two vectors
    """
    def add(self, other: Vec2D) -> Vec2D:
        return self.add_x_y(other.x, other.y)

    """
    Adds x and y to the vector
    """
    def add_x_y(self, x: float, y: float = 0):
        return Vec2D(self.x + x, self.y + y)


class Box:
    """
    A box has a position and a width and height
    """
    def __init__(self, pos: Vec2D, size: Vec2D) -> None:
        self.position = pos
        self.size = size

    @property
    def top_left(self):
        return self.position

    @property
    def top_right(self):
        return self.position.add_x_y(self.size.x)

    @property
    def bottom_right(self):
        return self.position.add(self.size)

    @property
    def bottom_left(self):
        return self.position.add_x_y(0, self.size.y)

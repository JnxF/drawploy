import abc
from typing import List
from backend.page.api.models.basics import Vec2D, Box


class Shape:
    """
    A shape is a generic figure. It can be, for example, an square containing
    a text in the center, a circle, an invisible square, etc.
    """
    @abc.abstractmethod
    def bounding_box(self) -> Box:
        """
        Implement this method to return the bounding box of the shape
        """
        pass


class Text(Shape, Box):
    """
    A text positioned somewhere floating in the diagram
    """
    def __init__(self, text: str, position: Vec2D, size: Vec2D) -> None:
        super().__init__(position, size)
        self.text = text

    def bounding_box(self) -> Box:
        return self


class Square(Shape, Box):
    """
    A square is defined by 4 points in space, or a top-left corner,
    a width and a height
    """
    def __init__(self, pos: Vec2D, size: Vec2D) -> None:
        super().__init__(pos, size)

    def bounding_box(self) -> Box:
        return self


class SquareWithCenteredText(Square):
    """
    A square with a centered text
    """
    def __init__(self, pos: Vec2D, size: Vec2D, text: str) -> None:
        super().__init__(pos, size)
        self.text = text


class Link:
    """
    A link is the bond between two shapes, it can be directed or not
    """
    def __init__(self, origin: Shape, target: Shape, is_directed: bool) -> None:
        super().__init__()
        self.origin = origin
        self.target = target
        self.is_directed = is_directed


class Diagram:
    """
    The diagram consists of a bunch of shapes linked by different links.
    It is possible also to have floating texts.
    """
    def __init__(self, shapes: List[Shape], links: List[Shape]) -> None:
        super().__init__()
        self.shapes = shapes
        self.links = links


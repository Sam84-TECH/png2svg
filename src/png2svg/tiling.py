"""Tilings: how a canvas is split into polygonal cells (object-oriented)."""

from abc import ABC, abstractmethod

from png2svg.geometry import Point, hexagon_centers, hexagon_points, triangle_cells


class Tiling(ABC):
    """A strategy that covers a width x height area with polygonal cells."""

    @abstractmethod
    def cells(self, width: float, height: float) -> list[list[Point]]:
        """Return the list of cells, each a list of vertices."""

    @property
    @abstractmethod
    def sample_radius(self) -> float:
        """Radius used to sample a cell's color around its centroid."""


class HexagonTiling(Tiling):
    """Hexagonal tiling, flat-top or pointy-top."""

    def __init__(self, radius: float = 13.0, orientation: str = "flat") -> None:
        if orientation not in ("pointy", "flat"):
            raise ValueError(f"Unknown orientation: {orientation}")
        self.radius = radius
        self.orientation = orientation

    def cells(self, width: float, height: float) -> list[list[Point]]:
        return [
            hexagon_points(cx, cy, self.radius, self.orientation)
            for cx, cy in hexagon_centers(width, height, self.radius, self.orientation)
        ]

    @property
    def sample_radius(self) -> float:
        return self.radius


class TriangleTiling(Tiling):
    """Triangular tiling of equilateral triangles."""

    def __init__(self, side: float = 13.0) -> None:
        self.side = side

    def cells(self, width: float, height: float) -> list[list[Point]]:
        return triangle_cells(width, height, self.side)

    @property
    def sample_radius(self) -> float:
        return self.side / 2


def make_tiling(shape: str, radius: float, orientation: str = "flat") -> Tiling:
    """Build the tiling matching a shape name."""
    if shape == "hexagon":
        return HexagonTiling(radius, orientation)
    if shape == "triangle":
        return TriangleTiling(radius)
    raise ValueError(f"Unknown shape: {shape}")

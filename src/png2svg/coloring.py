"""Colorizers: how each cell gets its color (object-oriented)."""

import math
from abc import ABC, abstractmethod
from collections.abc import Callable

from PIL import Image

from png2svg.geometry import Point, centroid
from png2svg.imaging import Color, average_color

# A distribution maps a normalized position (u, v) in [0, 1]x[0, 1] to a
# weight in [0, 1], used to pick a color from a palette.
Distribution = Callable[[float, float], float]


class Colorizer(ABC):
    """A strategy that assigns a color to a cell."""

    @abstractmethod
    def color(self, cell: list[Point]) -> Color:
        """Return the color of a cell given its vertices."""


class ImageColorizer(Colorizer):
    """Pick each cell's color by averaging the source image under it."""

    def __init__(self, image: Image.Image, sample_radius: float) -> None:
        self.image = image.convert("RGB")
        self.sample_radius = sample_radius

    def color(self, cell: list[Point]) -> Color:
        cx, cy = centroid(cell)
        return average_color(self.image, cx, cy, self.sample_radius)


class PaletteColorizer(Colorizer):
    """Pick each cell's color from a palette using a distribution function."""

    def __init__(
        self,
        palette: list[Color],
        distribution: Distribution,
        width: float,
        height: float,
    ) -> None:
        if not palette:
            raise ValueError("palette must not be empty")
        self.palette = palette
        self.distribution = distribution
        self.width = width
        self.height = height

    def color(self, cell: list[Point]) -> Color:
        cx, cy = centroid(cell)
        u = min(max(cx / self.width, 0.0), 1.0) if self.width else 0.0
        v = min(max(cy / self.height, 0.0), 1.0) if self.height else 0.0
        weight = min(max(self.distribution(u, v), 0.0), 1.0 - 1e-9)
        return self.palette[int(weight * len(self.palette))]


def horizontal(u: float, v: float) -> float:
    """Left-to-right gradient."""
    return u


def vertical(u: float, v: float) -> float:
    """Top-to-bottom gradient."""
    return v


def diagonal(u: float, v: float) -> float:
    """Top-left to bottom-right gradient."""
    return (u + v) / 2


def radial(u: float, v: float) -> float:
    """Distance from the center, 0 at the center, 1 at the corners."""
    return math.hypot(u - 0.5, v - 0.5) / math.hypot(0.5, 0.5)


DISTRIBUTIONS: dict[str, Distribution] = {
    "horizontal": horizontal,
    "vertical": vertical,
    "diagonal": diagonal,
    "radial": radial,
}


def parse_color(text: str) -> Color:
    """Parse a hex color like '#1ac7ea' or '1ac7ea' into an (r, g, b) tuple."""
    value = text.strip().lstrip("#")
    if len(value) != 6:
        raise ValueError(f"Invalid hex color: {text!r}")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


def parse_palette(text: str) -> list[Color]:
    """Parse a comma-separated list of hex colors into a palette."""
    return [parse_color(part) for part in text.split(",") if part.strip()]

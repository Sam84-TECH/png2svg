"""High-level PNG to SVG conversion (object-oriented core + functional facade)."""

from pathlib import Path

from PIL import Image

from png2svg.coloring import Colorizer, Distribution, ImageColorizer, PaletteColorizer
from png2svg.imaging import Color, load_image
from png2svg.svg import build_svg
from png2svg.tiling import Tiling, make_tiling


class Converter:
    """Turn a canvas into an SVG by combining a tiling and a colorizer."""

    def __init__(self, tiling: Tiling, colorizer: Colorizer) -> None:
        self.tiling = tiling
        self.colorizer = colorizer

    def render(self, width: int, height: int) -> str:
        """Return the SVG string for a width x height canvas."""
        polygons = [(cell, self.colorizer.color(cell)) for cell in self.tiling.cells(width, height)]
        return build_svg(width, height, polygons)


def image_to_svg(
    image: Image.Image,
    radius: float = 10.0,
    orientation: str = "pointy",
    shape: str = "hexagon",
) -> str:
    """Convert a PIL image into an SVG made of hexagons or triangles."""
    tiling = make_tiling(shape, radius, orientation)
    rgb = image.convert("RGB")
    colorizer = ImageColorizer(rgb, tiling.sample_radius)
    return Converter(tiling, colorizer).render(*rgb.size)


def convert_file(
    source: str | Path,
    target: str | Path,
    radius: float = 10.0,
    orientation: str = "pointy",
    shape: str = "hexagon",
) -> None:
    """Read an image file and write its hexagonal or triangular SVG version."""
    svg = image_to_svg(load_image(source), radius, orientation, shape)
    Path(target).write_text(svg, encoding="utf-8")


def generate_wallpaper(
    width: int,
    height: int,
    palette: list[Color],
    distribution: Distribution,
    radius: float = 13.0,
    orientation: str = "flat",
    shape: str = "hexagon",
) -> str:
    """Generate an SVG wallpaper from a palette and a distribution function."""
    tiling = make_tiling(shape, radius, orientation)
    colorizer = PaletteColorizer(palette, distribution, width, height)
    return Converter(tiling, colorizer).render(width, height)

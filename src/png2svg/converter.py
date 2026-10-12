"""High-level PNG to hexagonal SVG conversion."""

from pathlib import Path

from PIL import Image

from png2svg.geometry import hexagon_centers, hexagon_points
from png2svg.imaging import average_color, load_image
from png2svg.svg import build_svg


def image_to_svg(image: Image.Image, radius: float = 10.0, orientation: str = "pointy") -> str:
    """Convert a PIL image into an SVG string made of hexagons."""
    rgb = image.convert("RGB")
    width, height = rgb.size
    hexagons = [
        (
            hexagon_points(cx, cy, radius, orientation),
            average_color(rgb, cx, cy, radius),
        )
        for cx, cy in hexagon_centers(width, height, radius, orientation)
    ]
    return build_svg(width, height, hexagons)


def convert_file(
    source: str | Path,
    target: str | Path,
    radius: float = 10.0,
    orientation: str = "pointy",
) -> None:
    """Read an image file and write the hexagonal SVG version."""
    svg = image_to_svg(load_image(source), radius, orientation)
    Path(target).write_text(svg, encoding="utf-8")

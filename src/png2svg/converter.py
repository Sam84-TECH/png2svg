"""High-level image to SVG conversion."""

import math
from pathlib import Path

from PIL import Image

from png2svg.geometry import Point, hexagon_centers, hexagon_points, triangle_grid
from png2svg.imaging import Color, average_color, load_image
from png2svg.svg import build_svg


def image_to_svg(
    image: Image.Image,
    radius: float = 10.0,
    orientation: str = "pointy",
    shape: str = "hexagon",
) -> str:
    """Convert a PIL image into an SVG string made of hexagons or triangles."""
    rgb = image.convert("RGB")
    width, height = rgb.size
    cells: list[tuple[list[Point], Color]] = []
    if shape == "hexagon":
        for cx, cy in hexagon_centers(width, height, radius, orientation):
            cells.append(
                (hexagon_points(cx, cy, radius, orientation), average_color(rgb, cx, cy, radius))
            )
    elif shape == "triangle":
        sample_radius = radius * math.sqrt(3) / 6
        for points in triangle_grid(width, height, radius):
            cx = sum(p[0] for p in points) / 3
            cy = sum(p[1] for p in points) / 3
            cells.append((points, average_color(rgb, cx, cy, sample_radius)))
    else:
        raise ValueError(f"Unknown shape: {shape}")
    return build_svg(width, height, cells)


def convert_file(
    source: str | Path,
    target: str | Path,
    radius: float = 10.0,
    orientation: str = "pointy",
    shape: str = "hexagon",
) -> None:
    """Read an image file and write the SVG version."""
    svg = image_to_svg(load_image(source), radius, orientation, shape)
    Path(target).write_text(svg, encoding="utf-8")

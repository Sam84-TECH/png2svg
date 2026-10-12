"""SVG generation."""

from png2svg.geometry import Point
from png2svg.imaging import Color


def build_svg(width: int, height: int, hexagons: list[tuple[list[Point], Color]]) -> str:
    """Build an SVG document from a list of (vertices, color) hexagons."""
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}">'
    ]
    for points, (r, g, b) in hexagons:
        coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        fill = f"rgb({r},{g},{b})"
        lines.append(
            f'  <polygon points="{coords}" fill="{fill}" stroke="{fill}" stroke-width="1"/>'
        )
    lines.append("</svg>")
    return "\n".join(lines)

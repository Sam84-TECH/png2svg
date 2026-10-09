"""Hexagon geometry (pointy-top)."""

import math

Point = tuple[float, float]


def hexagon_points(cx: float, cy: float, r: float) -> list[Point]:
    """Return the 6 vertices of a pointy-top hexagon, starting from the top."""
    return [
        (
            cx + r * math.cos(math.radians(60 * k - 90)),
            cy + r * math.sin(math.radians(60 * k - 90)),
        )
        for k in range(6)
    ]


def hexagon_centers(width: float, height: float, r: float) -> list[Point]:
    """Return hexagon centers covering a width x height area (odd rows shifted)."""
    dx = math.sqrt(3) * r
    dy = 1.5 * r
    centers: list[Point] = []
    row = 0
    y = 0.0
    while y <= height + r:
        x = dx / 2 if row % 2 else 0.0
        while x <= width + dx / 2:
            centers.append((x, y))
            x += dx
        row += 1
        y = row * dy
    return centers

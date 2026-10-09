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


"""Hexagon geometry (pointy-top)."""

import math

Point = tuple[float, float]


def hexagon_points(cx: float, cy: float, r: float, orientation: str = "pointy") -> list[Point]:
    """Return the 6 vertices of a hexagon ("pointy" or "flat" top)."""
    if orientation not in ("pointy", "flat"):
        raise ValueError(f"Unknown orientation: {orientation}")
    start = -90 if orientation == "pointy" else 0
    return [
        (
            cx + r * math.cos(math.radians(60 * k + start)),
            cy + r * math.sin(math.radians(60 * k + start)),
        )
        for k in range(6)
    ]


def hexagon_centers(
    width: float, height: float, r: float, orientation: str = "pointy"
) -> list[Point]:
    """Return hexagon centers covering a width x height area."""
    if orientation not in ("pointy", "flat"):
        raise ValueError(f"Unknown orientation: {orientation}")
    centers: list[Point] = []
    if orientation == "pointy":
        dx, dy = math.sqrt(3) * r, 1.5 * r
        row, y = 0, 0.0
        while y <= height + r:
            x = dx / 2 if row % 2 else 0.0
            while x <= width + dx / 2:
                centers.append((x, y))
                x += dx
            row += 1
            y = row * dy
    else:
        dx, dy = 1.5 * r, math.sqrt(3) * r
        col, x = 0, 0.0
        while x <= width + r:
            y = dy / 2 if col % 2 else 0.0
            while y <= height + dy / 2:
                centers.append((x, y))
                y += dy
            col += 1
            x = col * dx
    return centers

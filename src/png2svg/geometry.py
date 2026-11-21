"""Hexagon and triangle geometry."""

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


def triangle_cells(width: float, height: float, side: float) -> list[list[Point]]:
    """Return triangle cells (3 vertices each) tiling a width x height area.

    Equilateral triangles of the given side length, laid out in rows and
    alternating between upward- and downward-pointing to interlock.
    """
    h = math.sqrt(3) / 2 * side
    cells: list[list[Point]] = []
    row, y_top = 0, 0.0
    while y_top <= height:
        y_bottom = y_top + h
        col, x = 0, 0.0
        while x <= width:
            if (row + col) % 2 == 0:
                cells.append([(x, y_bottom), (x + side, y_bottom), (x + side / 2, y_top)])
            else:
                cells.append([(x, y_top), (x + side, y_top), (x + side / 2, y_bottom)])
            col += 1
            x = col * side / 2
        row += 1
        y_top = row * h
    return cells


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


def centroid(points: list[Point]) -> Point:
    """Return the centroid (average of the vertices) of a polygon."""
    n = len(points)
    return (sum(x for x, _ in points) / n, sum(y for _, y in points) / n)

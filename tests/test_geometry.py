import math

import pytest

from png2svg.geometry import hexagon_centers, hexagon_points, triangle_cells


def test_hexagon_has_six_points():
    assert len(hexagon_points(0, 0, 10)) == 6


def test_points_are_at_distance_r_from_center():
    for x, y in hexagon_points(5, 7, 10):
        assert math.hypot(x - 5, y - 7) == pytest.approx(10)


def test_first_point_is_top_vertex():
    x, y = hexagon_points(5, 7, 10)[0]
    assert (x, y) == pytest.approx((5, -3))


def test_width_is_sqrt3_times_r():
    xs = [p[0] for p in hexagon_points(0, 0, 10)]
    assert max(xs) - min(xs) == pytest.approx(math.sqrt(3) * 10)


def test_first_center_is_origin():
    assert hexagon_centers(100, 100, 10)[0] == (0.0, 0.0)


def test_horizontal_spacing_is_sqrt3_r():
    centers = hexagon_centers(100, 100, 10)
    assert centers[1][0] - centers[0][0] == pytest.approx(math.sqrt(3) * 10)


def test_odd_rows_are_shifted_and_closer():
    centers = hexagon_centers(100, 100, 10)
    row2 = [c for c in centers if c[1] == pytest.approx(15)]
    assert row2[0][0] == pytest.approx(math.sqrt(3) * 10 / 2)


def test_grid_covers_the_image():
    centers = hexagon_centers(100, 100, 10)
    assert max(c[0] for c in centers) >= 100
    assert max(c[1] for c in centers) >= 100


def test_flat_top_has_flat_top_edge():
    pts = hexagon_points(0, 0, 10, orientation="flat")
    ys = sorted(round(p[1], 6) for p in pts)
    assert ys[0] == ys[1]


def test_flat_top_width_is_2r():
    xs = [p[0] for p in hexagon_points(0, 0, 10, orientation="flat")]
    assert max(xs) - min(xs) == pytest.approx(20)


def test_flat_top_column_spacing_is_1_5_r():
    centers = hexagon_centers(100, 100, 10, orientation="flat")
    assert centers[0] == (0.0, 0.0)
    assert any(c[0] == pytest.approx(15) for c in centers)


def test_unknown_orientation_raises():
    with pytest.raises(ValueError):
        hexagon_points(0, 0, 10, orientation="diagonal")


def test_triangle_cells_are_triangles():
    cells = triangle_cells(50, 50, 10)
    assert cells
    assert all(len(points) == 3 for points in cells)


def test_triangle_side_length_matches_the_parameter():
    cells = triangle_cells(50, 50, 10)
    for i, j in ((0, 1), (1, 2), (2, 0)):
        (x1, y1), (x2, y2) = cells[0][i], cells[0][j]
        assert math.hypot(x1 - x2, y1 - y2) == pytest.approx(10)


def test_triangle_grid_covers_the_image():
    cells = triangle_cells(100, 100, 10)
    xs = [x for points in cells for x, _ in points]
    ys = [y for points in cells for _, y in points]
    assert max(xs) >= 100
    assert max(ys) >= 100


def test_triangle_grid_alternates_up_and_down():
    cells = triangle_cells(40, 10, 10)
    # In a tiling strip, both upward and downward triangles must appear.
    apex_above_base = []
    for points in cells:
        ys = sorted(p[1] for p in points)
        apex_above_base.append(ys[0] == pytest.approx(ys[1]))
    assert any(apex_above_base) and not all(apex_above_base)

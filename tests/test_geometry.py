import math

import pytest

from png2svg.geometry import hexagon_centers, hexagon_points


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

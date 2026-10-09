import math

import pytest

from png2svg.geometry import hexagon_points


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

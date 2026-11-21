import pytest

from png2svg.tiling import HexagonTiling, TriangleTiling, make_tiling


def test_hexagon_tiling_produces_six_point_cells():
    cells = HexagonTiling(10, "flat").cells(60, 60)
    assert cells
    assert all(len(cell) == 6 for cell in cells)


def test_triangle_tiling_produces_three_point_cells():
    cells = TriangleTiling(10).cells(60, 60)
    assert cells
    assert all(len(cell) == 3 for cell in cells)


def test_triangle_sample_radius_is_half_side():
    assert TriangleTiling(10).sample_radius == 5


def test_make_tiling_selects_the_class():
    assert isinstance(make_tiling("hexagon", 10), HexagonTiling)
    assert isinstance(make_tiling("triangle", 10), TriangleTiling)


def test_make_tiling_rejects_unknown_shape():
    with pytest.raises(ValueError):
        make_tiling("square", 10)


def test_hexagon_tiling_rejects_unknown_orientation():
    with pytest.raises(ValueError):
        HexagonTiling(10, "diagonal")

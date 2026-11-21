import pytest
from PIL import Image

from png2svg.converter import convert_file, image_to_svg


def test_image_to_svg_has_polygons():
    svg = image_to_svg(Image.new("RGB", (60, 60), (9, 9, 9)), 10)
    assert "<polygon" in svg
    assert "rgb(9,9,9)" in svg


def test_convert_file_writes_svg(tmp_path):
    src, dst = tmp_path / "a.png", tmp_path / "a.svg"
    Image.new("RGB", (60, 60), (1, 2, 3)).save(src)
    convert_file(src, dst, 10)
    assert dst.read_text(encoding="utf-8").startswith("<svg")


def test_triangle_shape_produces_triangles():
    svg = image_to_svg(Image.new("RGB", (60, 60), (9, 9, 9)), 10, shape="triangle")
    first_polygon = svg.split('points="')[1].split('"')[0]
    assert len(first_polygon.split()) == 3


def test_unknown_shape_raises():
    with pytest.raises(ValueError):
        image_to_svg(Image.new("RGB", (60, 60)), 10, shape="circle")

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

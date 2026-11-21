import pytest
from PIL import Image

from png2svg.cli import build_parser, main


def test_parser_defaults():
    args = build_parser().parse_args(["in.png", "out.svg"])
    assert args.radius == 13.0


def test_parser_radius():
    assert build_parser().parse_args(["a.png", "b.svg", "--radius", "5"]).radius == 5.0


def test_main_creates_svg(tmp_path):
    src, dst = tmp_path / "a.png", tmp_path / "a.svg"
    Image.new("RGB", (60, 60), (5, 5, 5)).save(src)
    main([str(src), str(dst), "--radius", "8"])
    assert dst.exists()


def test_main_requires_arguments():
    with pytest.raises(SystemExit):
        main([])


def test_parser_orientation_default_is_flat():
    assert build_parser().parse_args(["a.png", "b.svg"]).orientation == "flat"


def test_parser_orientation_pointy():
    args = build_parser().parse_args(["a.png", "b.svg", "--orientation", "pointy"])
    assert args.orientation == "pointy"


def test_parser_shape_default_is_hexagon():
    assert build_parser().parse_args(["a.png", "b.svg"]).shape == "hexagon"


def test_parser_shape_triangle():
    args = build_parser().parse_args(["a.png", "b.svg", "--shape", "triangle"])
    assert args.shape == "triangle"


def test_main_creates_triangle_svg(tmp_path):
    src, dst = tmp_path / "a.png", tmp_path / "a.svg"
    Image.new("RGB", (60, 60), (5, 5, 5)).save(src)
    main([str(src), str(dst), "--shape", "triangle"])
    assert dst.read_text(encoding="utf-8").startswith("<svg")


def test_generate_parser_defaults():
    from png2svg.cli import build_generate_parser

    args = build_generate_parser().parse_args(["out.svg"])
    assert args.size == (1920, 1080)
    assert args.distribution == "diagonal"


def test_generate_main_writes_svg(tmp_path):
    from png2svg.cli import generate_main

    dst = tmp_path / "w.svg"
    generate_main([str(dst), "--size", "60x40", "--palette", "#ff0000,#00ff00", "--radius", "10"])
    assert dst.read_text(encoding="utf-8").startswith("<svg")

import pytest
from PIL import Image

from png2svg.cli import build_parser, main


def test_parser_defaults():
    args = build_parser().parse_args(["in.png", "out.svg"])
    assert args.radius == 10.0


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
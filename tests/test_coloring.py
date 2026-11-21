import pytest
from PIL import Image

from png2svg.coloring import (
    DISTRIBUTIONS,
    ImageColorizer,
    PaletteColorizer,
    parse_color,
    parse_palette,
    radial,
)


def test_image_colorizer_averages_the_source():
    img = Image.new("RGB", (20, 20), (10, 20, 30))
    colorizer = ImageColorizer(img, 5)
    assert colorizer.color([(0, 0), (10, 0), (5, 10)]) == (10, 20, 30)


def test_palette_colorizer_picks_from_the_palette():
    palette = [(0, 0, 0), (255, 255, 255)]
    colorizer = PaletteColorizer(palette, lambda u, v: u, 100, 100)
    left = colorizer.color([(0, 0), (2, 0), (1, 2)])
    right = colorizer.color([(98, 0), (100, 0), (99, 2)])
    assert left == (0, 0, 0)
    assert right == (255, 255, 255)


def test_palette_colorizer_rejects_empty_palette():
    with pytest.raises(ValueError):
        PaletteColorizer([], lambda u, v: u, 10, 10)


def test_parse_color_handles_hash_prefix():
    assert parse_color("#1ac7ea") == (26, 199, 234)
    assert parse_color("1ac7ea") == (26, 199, 234)


def test_parse_color_rejects_bad_length():
    with pytest.raises(ValueError):
        parse_color("#abc")


def test_parse_palette_splits_colors():
    assert parse_palette("#000000, #ffffff") == [(0, 0, 0), (255, 255, 255)]


def test_radial_is_zero_at_center():
    assert radial(0.5, 0.5) == pytest.approx(0)


def test_distributions_registry_is_not_empty():
    assert "diagonal" in DISTRIBUTIONS

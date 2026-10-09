from PIL import Image

from png2svg.imaging import load_image


def test_load_image_returns_rgb(tmp_path):
    path = tmp_path / "a.png"
    Image.new("RGBA", (10, 5), (255, 0, 0, 255)).save(path)
    img = load_image(path)
    assert img.mode == "RGB"
    assert img.size == (10, 5)

from PIL import Image

from png2svg.imaging import load_image, average_color

def test_load_image_returns_rgb(tmp_path):
    path = tmp_path / "a.png"
    Image.new("RGBA", (10, 5), (255, 0, 0, 255)).save(path)
    img = load_image(path)
    assert img.mode == "RGB"
    assert img.size == (10, 5)

def test_average_of_uniform_image():
    img = Image.new("RGB", (50, 50), (10, 20, 30))
    assert average_color(img, 25, 25, 10) == (10, 20, 30)


def test_average_of_two_halves():
    img = Image.new("RGB", (40, 40), (0, 0, 0))
    img.paste((200, 200, 200), (20, 0, 40, 40))
    r, g, b = average_color(img, 20, 20, 10)
    assert 80 <= r <= 120


def test_center_outside_image_does_not_crash():
    img = Image.new("RGB", (10, 10), (1, 2, 3))
    assert average_color(img, 500, 500, 5) == (1, 2, 3)
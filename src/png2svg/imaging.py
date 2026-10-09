"""Image loading and color sampling."""

from pathlib import Path

from PIL import Image


def load_image(path: str | Path) -> Image.Image:
    """Open an image file and convert it to RGB."""
    with Image.open(path) as img:
        return img.convert("RGB")


Color = tuple[int, int, int]


def average_color(image: Image.Image, cx: float, cy: float, r: float) -> Color:
    """Average RGB color of the pixels inside the circle of radius r around (cx, cy)."""
    rgb = image.convert("RGB")
    width, height = rgb.size
    total = [0, 0, 0]
    count = 0
    for y in range(max(0, int(cy - r)), min(height, int(cy + r) + 1)):
        for x in range(max(0, int(cx - r)), min(width, int(cx + r) + 1)):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                pixel = rgb.getpixel((x, y))
                assert isinstance(pixel, tuple)
                total[0] += pixel[0]
                total[1] += pixel[1]
                total[2] += pixel[2]
                count += 1
    if count == 0:
        nearest = rgb.getpixel((min(max(int(cx), 0), width - 1), min(max(int(cy), 0), height - 1)))
        assert isinstance(nearest, tuple)
        return (nearest[0], nearest[1], nearest[2])
    return (round(total[0] / count), round(total[1] / count), round(total[2] / count))

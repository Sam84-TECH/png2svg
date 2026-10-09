"""Image loading and color sampling."""

from pathlib import Path

from PIL import Image


def load_image(path: str | Path) -> Image.Image:
    """Open an image file and convert it to RGB."""
    with Image.open(path) as img:
        return img.convert("RGB")

"""Command-line interfaces for png2svg."""

import argparse
from pathlib import Path

from png2svg.coloring import DISTRIBUTIONS, parse_palette
from png2svg.converter import convert_file, generate_wallpaper


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="png2svg", description="Convert a PNG into a hexagonal SVG wallpaper."
    )
    parser.add_argument("input", help="Input PNG file")
    parser.add_argument("output", help="Output SVG file")
    parser.add_argument("--radius", type=float, default=13.0, help="Hexagon radius in pixels")
    parser.add_argument(
        "--orientation",
        choices=["pointy", "flat"],
        default="flat",
        help="Hexagon orientation (default: flat)",
    )
    parser.add_argument(
        "--shape",
        choices=["hexagon", "triangle"],
        default="hexagon",
        help="Cell shape (default: hexagon); --orientation applies to hexagons only",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    convert_file(Path(args.input), Path(args.output), args.radius, args.orientation, args.shape)


def _size(text: str) -> tuple[int, int]:
    width, _, height = text.lower().partition("x")
    return int(width), int(height)


def build_generate_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="png2svg-generate",
        description="Generate an SVG wallpaper from a color palette and a distribution.",
    )
    parser.add_argument("output", help="Output SVG file")
    parser.add_argument(
        "--size", type=_size, default=(1920, 1080), help="Canvas size WxH (default: 1920x1080)"
    )
    parser.add_argument(
        "--palette",
        default="#1a1a2e,#16213e,#0f3460,#e94560",
        help="Comma-separated hex colors, e.g. '#1a1a2e,#e94560'",
    )
    parser.add_argument(
        "--distribution",
        choices=sorted(DISTRIBUTIONS),
        default="diagonal",
        help="Color distribution (default: diagonal)",
    )
    parser.add_argument("--radius", type=float, default=13.0, help="Cell radius/side in pixels")
    parser.add_argument("--orientation", choices=["pointy", "flat"], default="flat")
    parser.add_argument("--shape", choices=["hexagon", "triangle"], default="hexagon")
    return parser


def generate_main(argv: list[str] | None = None) -> None:
    args = build_generate_parser().parse_args(argv)
    width, height = args.size
    svg = generate_wallpaper(
        width,
        height,
        parse_palette(args.palette),
        DISTRIBUTIONS[args.distribution],
        args.radius,
        args.orientation,
        args.shape,
    )
    Path(args.output).write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
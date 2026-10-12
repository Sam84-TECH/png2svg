"""Command-line interface for png2svg."""

import argparse
from pathlib import Path

from png2svg.converter import convert_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="png2svg", description="Convert a PNG into a hexagonal SVG wallpaper."
    )
    parser.add_argument("input", help="Input PNG file")
    parser.add_argument("output", help="Output SVG file")
    parser.add_argument("--radius", type=float, default=12.0, help="Hexagon radius in pixels")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    convert_file(Path(args.input), Path(args.output), args.radius)


if __name__ == "__main__":
    main()

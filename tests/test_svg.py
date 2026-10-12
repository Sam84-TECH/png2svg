from png2svg.svg import build_svg


def test_svg_has_header_and_viewbox():
    svg = build_svg(100, 50, [])
    assert svg.startswith("<svg")
    assert 'viewBox="0 0 100 50"' in svg
    assert svg.rstrip().endswith("</svg>")


def test_svg_contains_one_polygon_per_hexagon():
    pts = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.5, 1.5), (0.0, 0.5)]
    svg = build_svg(10, 10, [(pts, (255, 0, 0)), (pts, (0, 255, 0))])
    assert svg.count("<polygon") == 2
    assert "rgb(255,0,0)" in svg
    
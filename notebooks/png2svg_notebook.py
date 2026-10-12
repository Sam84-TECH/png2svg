import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")

with app.setup:
    import io

    import marimo as mo
    from PIL import Image

    from png2svg.converter import image_to_svg


@app.cell
def _():
    mo.md("""
    # png2svg
    Choisis une image (PNG ou JPG) et la taille des hexagones.
    """)
    return


@app.cell
def _():
    upload = mo.ui.file(filetypes=[".png", ".jpg", ".jpeg"], kind="area")
    radius = mo.ui.slider(3, 40, value=12, label="Rayon")
    mo.vstack([upload, radius])
    return radius, upload


@app.cell
def _(radius, upload):
    mo.stop(not upload.value, mo.md("Charge une image pour lancer la conversion."))
    img = Image.open(io.BytesIO(upload.contents()))
    svg = image_to_svg(img, radius.value)
    mo.Html(svg)
    return (svg,)


@app.cell
def _(svg):
    mo.download(data=svg.encode("utf-8"), filename="output.svg", mimetype="image/svg+xml")
    return


if __name__ == "__main__":
    app.run()

# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import matplotlib
import matplotlib.pyplot as plt
import PySide6.QtGui

import freud

# Activate 'agg' backend for off-screen plotting.
matplotlib.use("Agg")


def render(
    args,
    bins: int = 300,
    r_max: float = 5.0,
    dpi: float = 150,
    draw_x: float = 10
    width:float = None,
    height:float = None,
    draw_y: float = 10,
    align: str = "top right",
):
    plt.close()
    pipeline = args.scene.selected_pipeline
    if not pipeline:
        return
    data = pipeline.compute(args.frame)

    rdf = freud.density.RDF(bins=bins, r_max=r_max)
    rdf.compute(data)

    # Get size of rendered viewport image in pixels.

    viewport_width = args.painter.window().width()
    viewport_height = args.painter.window().height()
    if width is None:
        width = viewport_width/600
    if height is None:
        height = viewport_height/800
    if "right" in align:
        draw_x = viewport_width - dpi * width - draw_x
    if "bottom" in align:
        draw_y = viewport_height - dpi * height - draw_y

    # Create figure
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
    rdf.plot(ax=ax)
    fig.patch.set_alpha(0.0)
    plt.tight_layout()

    # Render figure to an in-memory buffer.
    buf = fig.canvas.print_to_buffer()

    # Create a QImage from the memory buffer
    res_x, res_y = buf[1]
    img = PySide6.QtGui.QImage(
        buf[0], res_x, res_y, PySide6.QtGui.QImage.Format_RGBA8888
    )

    # Paint QImage onto rendered viewport
    args.painter.drawImage(draw_x, draw_y, img)

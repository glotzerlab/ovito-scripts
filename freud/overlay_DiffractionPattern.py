# Copyright (c) 2021 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import PySide6.QtGui
import rowan

import freud
import numpy as np

print("Diffraction, freud version", freud.__version__)


def render(
    args,
    grid_size=256,
    output_size=256,
    draw_x: float = 10,
    draw_y: float = 10,
    zoom: float = 1,
):
    pipeline = args.scene.selected_pipeline
    if not pipeline:
        return
    data = pipeline.compute(args.frame)
    view_orientation = rowan.from_matrix(args.viewport.viewMatrix[:, :3])
    dp = freud.diffraction.DiffractionPattern(
        grid_size=grid_size,
        output_size=output_size,
    )
    dp.compute(
        system=data,
        view_orientation=view_orientation,
        zoom=zoom,
        peak_width=1,
    )
    buf = dp.to_image(cmap="afmhot", vmax=np.max(dp.diffraction))
    width, height, bytes_per_pixel = buf.shape
    img = PySide6.QtGui.QImage(
        buf,
        width,
        height,
        width * bytes_per_pixel,
        PySide6.QtGui.QImage.Format_RGBA8888,
    )
    # Paint QImage onto viewport canvas
    args.painter.drawImage(draw_x, draw_y, img)

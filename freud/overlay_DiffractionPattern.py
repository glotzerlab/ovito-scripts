

# Copyright (c) 2021 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import PySide6.QtGui
import numpy as np

import rowan
import freud

from ovito.vis import *
from ovito.data import *

class MyOverlay(ViewportOverlayInterface):

    def render(
        self,
        canvas,
        data,
        pipeline,
        frame,
        grid_size=256,
        output_size=256,
        draw_x: float = 10,
        draw_y: float = 10,
        zoom: float = 1,
        **kwargs,
    ):

        if not pipeline:
            return
        data = pipeline.compute(frame)
        view_orientation = rowan.from_matrix(canvas.view_tm[:, :3])
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
        canvas.drawImage(draw_x, draw_y, img)

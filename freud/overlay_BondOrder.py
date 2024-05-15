# Copyright (c) 2021 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.
from typing import Tuple

import numpy as np
import PySide6.QtGui
import rowan

import freud


def to_view(bod, view_orientation, image_size):
    lin_grid = np.linspace(-1, 1, image_size)
    x, y = np.meshgrid(lin_grid, lin_grid)
    y = -y
    r2 = x**2 + y**2
    z = np.sqrt(np.clip(1 - r2, 0, None))
    xyz = np.dstack((x, y, z))
    xyz = rowan.rotate(rowan.inverse(view_orientation), xyz)
    x, y, z = xyz[:, :, 0], xyz[:, :, 1], xyz[:, :, 2]
    view = np.zeros((image_size, image_size))
    phi = np.arccos(z)
    theta = np.arctan2(y, x) % (2 * np.pi)
    num_theta_bins, num_phi_bins = bod.nbins
    theta_bin_edges, phi_bin_edges = bod.bin_edges
    theta_bins = np.trunc(theta / (2 * np.pi) * num_theta_bins).astype(int)
    phi_bins = np.trunc(phi / np.pi * num_phi_bins).astype(int)
    view = bod.bond_order[theta_bins, phi_bins]
    view[r2 > 1] = np.nan
    return view


def to_image(
    arr, cmap="afmhot", vmin=0, vmax=None, clip_percentile=0.6, viewmode="percentile"
):
    import matplotlib.cm
    import matplotlib.colors

    if vmax is None:
        if viewmode == "percentile":
            vmax = np.nanpercentile(arr, clip_percentile)
        else:
            vmax = np.nanmax(arr) * 0.6
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    cmap = matplotlib.cm.get_cmap(cmap)
    image = cmap(norm(arr))
    return (image * 255).astype(np.uint8)


def render(
    args,
    bins: Tuple[int] = (200, 200),
    mode: str = "bod",
    neighbors: dict = {"r_max": 1.4},
    image_size: float = None,
    draw_x: int = None,
    draw_y: int = None,
    clip_percentile: float = 99.9,
    viewmode: str = "percentile",
    n_frames_to_average: int = 10,
):
    """Render a bond order diagram that rotates with the view.
        Args:
            args:
                OVITO viewport modifier arguments.
            bins:
                Passed to freud.environment.BondOrder.
            mode:
                Passed to freud.environment.BondOrder.
            neighbors:
                Passed to freud.environment.BondOrder.compute. It is recommended
                to use a cutoff distance at the first trough of the radial
                distribution function g(r). See
                https://freud.readthedocs.io/en/latest/topics/querying.html for
                more information.
            image_size:
                Rendered size of the bond order diagram.
            draw_x:
                X coordinate of the top-left corner of the drawn image.
            draw_y:
                Y coordinate of the top-left corner of the drawn image.
            clip_percentile:
                Percentile at which to clip data from the BOD. Default value = 99.9.
            viewmode:
                Whether to clip values based on percentile (recommended), or fall back to the old style
    of 0.6*max(bod). Any value other than "percentile" will use the old clipping method.
                Any value other than "percentile" will use the old clipping method.
                Default value: "percentile"
    """
    if image_size is None:
        image_size = args.size[1] // 4
    if draw_x is None:
        draw_x = args.size[1] - 10 - image_size
    if draw_y is None:
        draw_y = args.size[0] - 10 - image_size

    pipeline = args.scene.selected_pipeline
    if not pipeline:
        return

    view_orientation = rowan.from_matrix(args.viewport.viewMatrix[:, :3])
    bod = freud.environment.BondOrder(bins, mode)
    data = pipeline.compute(args.frame)
    bod.compute(
        system=data,
        neighbors=neighbors,
        orientations=data.particles.orientations,
        reset=True,
    )

    view = to_view(bod, view_orientation, image_size)
    buf = to_image(
        view, cmap="afmhot", clip_percentile=clip_percentile, viewmode=viewmode
    )
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

# Copyright (c) 2021 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import numpy as np
import PySide2.QtGui
import rowan

import freud


def to_view(bod, view_orientation):
    image_size = 200
    lin_grid = np.linspace(-1, 1, image_size)
    x, y = np.meshgrid(lin_grid, lin_grid)
    y = -y
    r2 = x ** 2 + y ** 2
    z = np.sqrt(np.clip(1 - r2, 0, None))
    xyz = np.dstack((x, y, z))
    xyz = rowan.rotate(rowan.inverse(view_orientation), xyz)
    x, y, z = xyz[:, :, 0], xyz[:, :, 1], xyz[:, :, 2]
    view = np.zeros((image_size, image_size))
    phi = np.arccos(z)
    theta = np.arctan2(y, x) % (2 * np.pi)
    num_theta_bins, num_phi_bins = bod.nbins
    theta_bin_edges, phi_bin_edges = bod.bin_edges
    theta_bins = np.digitize(theta, theta_bin_edges[:-1])
    phi_bins = np.digitize(phi, phi_bin_edges[:-1])
    theta_bins[theta_bins == num_theta_bins] = 0
    phi_bins[phi_bins == num_phi_bins] = 0
    view = bod.bond_order[theta_bins, phi_bins]
    view[r2 > 1] = np.nan
    return view


def to_image(arr, cmap="afmhot", vmin=0, vmax=None):
    import matplotlib.cm
    import matplotlib.colors

    if vmax is None:
        vmax = np.nanmax(arr)
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    cmap = matplotlib.cm.get_cmap(cmap)
    image = cmap(norm(arr))
    return (image * 255).astype(np.uint8)


def render(args):
    pipeline = args.scene.selected_pipeline
    if not pipeline:
        return
    data = pipeline.compute(args.frame)
    view_orientation = rowan.from_matrix(args.viewport.viewMatrix[:, :3])
    n_bins_theta = 100
    n_bins_phi = 100
    bod = freud.environment.BondOrder((n_bins_theta, n_bins_phi))
    bod.compute(system=data, neighbors={"r_max": 1.6})
    view = to_view(bod, view_orientation)
    buf = to_image(view, cmap="afmhot")
    width, height, bytes_per_pixel = buf.shape
    img = PySide2.QtGui.QImage(
        buf,
        width,
        height,
        width * bytes_per_pixel,
        PySide2.QtGui.QImage.Format_RGBA8888,
    )
    # Paint QImage onto viewport canvas
    args.painter.drawImage(10, 10, img)

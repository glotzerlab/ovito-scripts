# Copyright (c) 2021 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import matplotlib.cm
import matplotlib.colors
import PySide6.QtGui
from ovito.data import DataCollection
from ovito.vis import ViewportOverlayInterface
from traits.api import Dict, Enum, Range, String, Tuple

import freud
import numpy as np


class BondOrderOverlay(ViewportOverlayInterface):
    # Adjustable user parameters:
    bins = Tuple((220, 220), label="(θ,φ) Bins", dtype=tuple[int, int])
    output_size = Range(value=440, low=1, label="Output Image Size", dtype=int)

    neighbors = Dict({"r_max": 1.4}, label="Neighbor Query")

    cmap = String(value="afmhot", label="Colormap")

    clip_percentile = Range(value=99.9, low=0.0, high=100.0, label="Clip Percentile")

    mode = Enum(
        ["bod", "obcd", "lbod", "oocd"],
        value="bod",
        label="BOD Mode",
    )

    # Code image position to the anchor parameter of canvas.draw_image
    anchor = Enum(
        ["south west", "south east", "north west", "north east"],
        value="south east",
        label="Image Position",
    )

    def render(self, canvas: ViewportOverlayInterface.Canvas, data: DataCollection, **kwargs):
        bod = freud.environment.BondOrder(bins=self.bins, mode=self.mode)
        bod.compute(
            system=data,
            neighbors=dict(self.neighbors),  # Ovito api 'Dict' to python base version
            orientations=data.particles.orientations,
            reset=True,
        )

        # Conver the BOD to a 2D image with the correct size and view orientation
        view = to_view(bod, canvas.view_tm[:, :3], image_size=self.output_size)

        vmin, vmax = 0.0, np.nanpercentile(view, self.clip_percentile)
        norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
        cmap = matplotlib.cm.get_cmap(self.cmap)
        image = cmap(norm(view))
        buf = (image * 255).astype(np.uint8)

        width, height, bytes_per_pixel = buf.shape
        img = PySide6.QtGui.QImage(
            buf, width, height, width * bytes_per_pixel, canvas.preferred_qimage_format
        )

        size_fraction = self.output_size / np.array(canvas.logical_size)
        image_pos = (
            0.01 if "west" in self.anchor else 0.99,
            0.01 if "south" in self.anchor else 0.99,
        )

        canvas.draw_image(img, pos=image_pos, size=size_fraction, anchor=self.anchor)

        return


def to_view(bod, view_matrix, image_size):
    """Convert a BOD in spherical coordinates to a hemispherical image on a plane."""
    lin_grid = np.linspace(-1, 1, image_size)
    x, y = np.meshgrid(lin_grid, -lin_grid)
    r2 = x**2 + y**2
    z = np.sqrt(np.clip(1 - r2, 0, None))
    xyz = np.dstack((x, y, z))

    xyz = xyz @ view_matrix
    x, y, z = xyz[..., 0], xyz[..., 1], xyz[..., 2]

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

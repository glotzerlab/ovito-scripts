# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import matplotlib
import matplotlib.pyplot as plt
import ovito
import PySide2.QtGui
import rowan
from matplotlib import patches

import freud
import numpy as np


def get_unit_area_ngon(n):
    """Compute vertices of a regular n-gon of area 1."""
    r = 1  # The radius of the circle
    theta = np.linspace(0, 2 * np.pi, num=n, endpoint=False)
    pos = np.array([np.cos(theta), np.sin(theta)])

    # First normalize to guarantee that the limiting case of an infinite number
    # of vertices produces a circle of area r^2.
    pos /= np.sqrt(np.pi) / r

    # Area of an n-gon inscribed in a circle
    # A_poly = ((n*r**2)/2)*np.sin(2*np.pi/n)
    # A_circ = np.pi*r**2
    # pos *= np.sqrt(A_circ/A_poly)
    a_circ_a_poly = np.pi / ((n / 2) * np.sin(2 * np.pi / n))
    pos *= np.sqrt(a_circ_a_poly)

    return pos.T


# Activate 'agg' backend for off-screen plotting.
matplotlib.use("Agg")


def render(args):
    plt.close()
    painter = args.painter
    node = ovito.dataset.selected_node
    data = node.compute()

    box = freud.Box.from_matrix(data.cell.matrix[:, :3], dimensions=2 if data.cell.is2D else 3)

    # The z positions are O(1e-15) but not quite zero.
    positions = data.particles.position[...].copy()
    positions[:, 2] = 0

    pmft = freud.pmft.PMFTXY(bins=100, x_max=5, y_max=5)
    angles = rowan.geometry.angle(data.particles["Orientation"].array[:, [1, 2, 3, 0]])
    pmft.compute((box, positions), query_orientations=angles)

    # Get size of rendered viewport image in pixels.
    viewport_width = painter.window().width()
    viewport_height = painter.window().height()

    #  Compute plot size in inches (DPI determines label size)
    dpi = 80
    plot_width = 0.5 * viewport_width / dpi
    plot_height = 0.5 * viewport_height / dpi

    # Create figure
    fig, ax = plt.subplots(figsize=(plot_width, plot_height), dpi=dpi)
    im = ax.contourf(pmft.bin_centers[0], pmft.bin_centers[1], pmft.pmft)
    ax.set_title("PMFT")
    cb = fig.colorbar(im, ax=ax)
    cb.set_label("$k_b T$", fontsize=12)

    # CHANGE THIS FOR DIFFERENT SHAPES.
    ax.add_patch(patches.Polygon(xy=get_unit_area_ngon(6)))
    plt.tight_layout()

    # Render figure to an in-memory buffer.
    buf = fig.canvas.print_to_buffer()

    # Create a QImage from the memory buffer
    res_x, res_y = buf[1]
    img = PySide2.QtGui.QImage(buf[0], res_x, res_y, PySide2.QtGui.QImage.Format_RGBA8888)

    # Paint QImage onto rendered viewport
    painter.drawImage(0, 0, img)

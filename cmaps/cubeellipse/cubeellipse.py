import matplotlib.pyplot as plt
import numpy.linalg as la

import numpy as np

"""
This helper script generates a cyclic colormap based on D.A. Green's
cubehelix colormap as decribed in:
https://ui.adsabs.harvard.edu/abs/2011BASI...39..289G/abstract

Last tested with:
* numpy 1.17.3
* matplotlib 3.0.2
"""


def py_ang(v2, v1=[1, 0]):
    """
    Returns the angle in radians between vectors 'v1' and 'v2'
    By default, this calculates radians on the unit circle from 0 = [1,0]
    Note the correction for angles greater than 180 degrees, i.e. having y-value<0
    """
    cosang = np.dot(v1, v2)
    sinang = la.norm(np.cross(v1, v2))
    if v2[1] < 0:
        return 2 * np.pi - np.arctan2(sinang, cosang)
    else:
        return np.arctan2(sinang, cosang)


def cubeellipse(theta, lam=0.5, gamma=1.0, s=4.0, r=1.0, h=2.0):
    """
    :param lam:
        intensity value 0 to 1
    :param gamma:
        nonlinear reweighting power to emphasize low-intensity values
        (gamma < 1) or high-intensity values (gamma > 1)
    :param s:
        The hue of the starting color: (0, 1, 2) -> (blue, red, green)
    :param r:
        Number of rotations through R->G->B to make
    :param h:
        Hue parameter controlling saturation
    """
    lam = lam**gamma

    a = h * lam * (1 - lam) * 0.5
    v = np.array([[-0.14861, 1.78277], [-0.29227, -0.90649], [1.97294, 0.0]], dtype=np.float32)
    ctarray = np.array([np.cos(theta * r + s), np.sin(theta * r + s)], dtype=np.float32)
    return (lam + a * v.dot(ctarray)).T


def generate_linear_colormap():
    """Generate a linear colormap.

    Prints out linear version of colormap that is 50 pixels wide and 600 pixels
    tall. In this configuration, the user needs to save, crop, and rotate the
    colormap COUNTER-CLOCKWISE to get a 0.1-1.0 linear scale.
    """
    width = 50
    height = 600
    # To get the final linear colormap, we rotate this counter-clockwise since
    # values will save top->bottom.
    rgb = np.asarray(
        [width * [cubeellipse(theta)] for theta in np.arange(0, 2 * np.pi, 2 * np.pi / height)]
    )
    plt.imshow(rgb)
    plt.axis("off")
    plt.show()
    return


def generate_cyclic_colormap():
    """Generate a square colormap.

    Generates a square colored by the cubeellipse angle color at that point on
    a unit circle. Use this output to make colormaps for papers using images
    colored by the linear colormap above.
    """
    n = 100
    x = np.linspace(-1, 1, n)
    y = np.linspace(1, -1, n)
    xx, yy = np.meshgrid(x, y)
    rgb = np.empty((n, n, 3))
    for i in range(n):
        for j in range(n):
            rgb[i][j] = cubeellipse(py_ang([xx[i][j], yy[i][j]]))
    plt.imshow(rgb)
    plt.axis("off")
    plt.show()
    return


if __name__ == "__main__":
    generate_linear_colormap()
    generate_cyclic_colormap()

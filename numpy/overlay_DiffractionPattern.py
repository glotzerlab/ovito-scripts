import matplotlib
import PySide6.QtGui
import scipy.ndimage
from ovito.data import DataCollection
from ovito.vis import ViewportOverlayInterface
from traits.api import Enum, Range, String

import numpy as np


class DiffractionPatternOverlay(ViewportOverlayInterface):
    # Adjustable user parameters:
    num_bins_input = Range(value=512, low=1, label="Input Image Size", dtype=int)
    output_size = Range(value=512, low=1, label="Output Image Size", dtype=int)

    input_blur_width = Range(value=0.0, low=0.0, label="σ for input blur")
    output_blur_width = Range(value=0.0, low=0.0, label="σ for output blur")

    intensity_cutoff = Range(value=0.0, low=0.0, high=1.0, label="Intensity Cutoff")

    zoom = Range(value=1.0, low=0.0, label="Zoom Factor")

    cmap = String(value="afmhot", label="Colormap")
    cmap_oom_offset = Range(value=3, low=0, label="Colormap Scale Offset")

    # Code image position to the anchor parameter of canvas.draw_image
    anchor = Enum(
        ["south west", "south east", "north west", "north east"],
        value="south west",
        label="Image Position",
    )

    act_safe = False

    def render(
        self, canvas: ViewportOverlayInterface.Canvas, data: DataCollection, **kwargs
    ):
        print(self.output_blur_width, type(self.output_blur_width))

        # By default, we do not prune points "inside" the camera
        xy = [canvas.project_location(xyz) for xyz in data.particles.positions]

        try:
            xy = np.array(xy, dtype=float)

        except ValueError:  # One or more points lie behind the camera
            xy = np.array(
                [p if p is not None else [np.nan, np.nan] for p in xy], dtype=float
            )

        # Create image by making a 2D histogram (copying freud)
        hist, _, _ = np.histogram2d(*xy.T, bins=self.num_bins_input)

        # Apply gaussian blur if desired
        image = scipy.ndimage.gaussian_filter(
            hist, self.input_blur_width, order=0, mode="wrap"
        )

        # Take FFT
        fft_image = np.fft.fft2(image)
        fft_image = np.fft.fftshift(fft_image)
        fft_image = np.sqrt(np.real(fft_image * np.conjugate(fft_image)))
        if not np.isclose(self.output_blur_width, 0):
            fft_image = scipy.ndimage.gaussian_filter(
                fft_image, self.output_blur_width, order=0, mode="wrap"
            )

        # make image out of FFT
        norm = matplotlib.colors.LogNorm(
            vmin=10 ** (-np.log10(data.particles.count) + self.cmap_oom_offset),
            vmax=data.particles.count,
            clip=True,
        )

        cmap = matplotlib.colormaps.get_cmap(self.cmap)
        fft_image = cmap(norm(fft_image.T))

        # Resample fft_image to output_size
        scale = self.output_size / self.num_bins_input

        if not np.isclose(scale, 1):
            resample_tuple = (scale,) * 2 + (1,) * (fft_image.ndim - 2)
            fft_image = scipy.ndimage.zoom(fft_image, resample_tuple, order=0)

        # Bounding box of the zoomed-in region within the input array

        if self.zoom > 1:
            zoom_tuple = (self.zoom, self.zoom) + (1,) * (fft_image.ndim - 2)
            h, w = fft_image.shape[:2]
            zh = np.ceil(h / self.zoom).astype(int)
            zw = np.ceil(w / self.zoom).astype(int)
            top = (h - zh) // 2
            left = (w - zw) // 2
            fft_image = scipy.ndimage.zoom(
                fft_image[top : top + zh, left : left + zw], zoom_tuple, order=0
            )

        width, height, bytes_per_pixel = fft_image.shape
        buf = (fft_image * 255).astype(np.uint8)

        intensity_cutoff = (1 - self.intensity_cutoff) * 255
        buf[np.mean(buf, axis=2) > intensity_cutoff] = 0

        # Paint QImage onto viewport canvas
        img = PySide6.QtGui.QImage(
            buf,
            width,
            height,
            canvas.preferred_qimage_format,
        )

        size_fraction = self.output_size / np.array(canvas.logical_size)
        image_pos = (
            0.01 if "west" in self.anchor else 0.99,
            0.01 if "south" in self.anchor else 0.99,
        )

        canvas.draw_image(img, pos=image_pos, size=size_fraction, anchor=self.anchor)

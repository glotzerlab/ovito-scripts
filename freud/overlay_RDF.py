# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.
import freud
import matplotlib.pyplot as plt
import numpy as np
from ovito.data import DataCollection
from ovito.vis import ViewportOverlayInterface
from traits.api import Bool, Enum, Range, Tuple


class RadialDistributionOverlay(ViewportOverlayInterface):
    # Adjustable user parameters:
    bins = Range(value=300, low=1, label="RDF Bins", dtype=int)
    r_max = Range(value=5.0, low=0.0, label="Maximum Radius")
    font_scale = Range(value=2.75, low=0.0, label="Font Scale")

    output_size = Tuple((512, 384), label="Output Image Size", dtype=tuple[int, int])

    anchor = Enum(
        ["south west", "south east", "north west", "north east"],
        value="north east",
        label="Image Position",
    )

    compute_first_shell_min = Bool(value=False, label="Compute first shell radius")

    cmap = "afmhot"

    def render(
        self,
        canvas: ViewportOverlayInterface.Canvas,
        data: DataCollection,
        **kwargs,
    ):
        rdf = freud.density.RDF(bins=self.bins, r_max=self.r_max)
        rdf.compute(data)

        image_pos = (
            0.01 if "west" in self.anchor else 0.99,
            0.01 if "south" in self.anchor else 0.99,
        )

        size = self.output_size / np.array(canvas.logical_size)

        # Create figure
        with canvas.mpl_figure(
            pos=image_pos,
            size=size,
            anchor=self.anchor,
            tight_layout=True,
            font_scale=self.font_scale,
        ) as fig:
            ax = fig.subplots()
            rdf.plot(ax=ax)
            ax.set_xticks(np.arange(rdf.bin_centers[0], self.r_max + 1).astype(int))
            ax.set_yticks([])

            if self.compute_first_shell_min:
                import scipy

                rdf_minima = scipy.signal.argrelmin(rdf.rdf)[0]
                min_point = rdf.bin_centers[rdf_minima[np.argmin(rdf.rdf[rdf_minima])]]
                plt.vlines(
                    [min_point], *ax.get_ylim(), "k", "dashed", label=min_point.round(3)
                )
                plt.legend()
                print(f"RDF_MIN: {min_point:.6f}")

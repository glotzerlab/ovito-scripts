# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import numpy as np

import freud


def modify(frame, data):
    # USER SHOULD SET THIS MANUALLY BEFORE RUNNING SCRIPT
    director = np.array([1, 0, 0])

    if data.particles is not None:
        orientations = data.particles["Orientation"][:]
        nematic = freud.order.Nematic(director)
        nematic.compute(orientations)
        print(f"Nematic order parameter = {nematic.order}")

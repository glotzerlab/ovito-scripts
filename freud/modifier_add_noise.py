# Copyright (c) 2021 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

# Keeps a certain particle at the center of the box by shifting and wrapping other particles.

import freud
import numpy as np


def modify(frame, data, sigma=0.05, wrap=True):
    if data.particles is not None:
        system = freud.AABBQuery.from_system(data)
        N = len(system.points)
        noise = np.random.multivariate_normal(
            mean=(0, 0, 0),
            cov=sigma * np.eye(3),
            size=N,
        )
        print(system.box)

        # This is a writeable array, denoted by the underscore.
        pos_property = data.particles_["Position_"]
        with pos_property:
            new_positions = system.points + noise
            if wrap:
                new_positions = system.box.wrap(new_positions)
            pos_property[:] = new_positions
        print("Added noise with sigma=", sigma)

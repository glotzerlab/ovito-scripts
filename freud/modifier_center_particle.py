# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

# Keeps a certain particle at the center of the box by shifting and wrapping other particles.

import freud


def modify(frame, data):
    # Index of the particle to be centered.
    center_index = 0

    if data.particles is not None:
        system = freud.AABBQuery.from_system(data)
        new_center = system.points[center_index]

        # This is a writeable array, denoted by the underscore.
        pos_property = data.particles_["Position_"]
        with pos_property:
            pos_property[:] = system.box.wrap(system.points - new_center)
        print("Shifted", new_center, "to center.")

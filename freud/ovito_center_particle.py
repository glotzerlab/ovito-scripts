# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

# Keeps a certain particle at the center of the box by shifting and wrapping other particles.

import freud


def modify(frame, data):
    if data.particles is not None:
        box = freud.box.Box.from_matrix(data.cell.matrix)
        pos_property = data.particles_["Position_"]
        new_center = data.particles.position[0]
        with pos_property:
            pos_property[:] = box.wrap(data.particles.position - new_center)
        print("Shifted", new_center, "to center.")

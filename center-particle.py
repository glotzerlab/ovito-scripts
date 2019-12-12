# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

# Keeps a certain particle at the center of the box by shifting and wrapping other particles.

import freud

def modify(frame, data):
    if data.particles != None:
        box = freud.box.Box.from_matrix(data.cell.matrix)
        pos_property = data.particles_['Position_']
        with pos_property:
            pos_property[:] = box.wrap(data.particles.position - data.particles.position[0])

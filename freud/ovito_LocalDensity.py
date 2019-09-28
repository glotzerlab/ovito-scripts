# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import freud

def modify(frame, input, output):
    if input.particles is not None:
        box = freud.box.Box.from_matrix(input.cell.matrix)
	positions = input.particles.position

        ld = freud.density.LocalDensity(r_cut=3, volume=1, diameter=0.05)
        ld.compute(box, input.particles.position)
        output.create_user_particle_property(name='LocalDensity', data_type=float, data=ld.density)
        print('Created property for {} particles.'.format(input.particles.count))

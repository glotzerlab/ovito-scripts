# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import freud
from ovito.data import *

def sense_check(r_max, diameter):
    if r_max==0 or diameter==0:
        print('WARNING! OVERWRITE VALUES IN SCRIPT')
    return

def modify(frame, data):
    #   USER SHOULD SET THESE MANUALLY BEFORE RUNNING SCRIPT
    r_max = 3
    diameter = 0.05
    sense_check(r_max, diameter)

    if input.particles is not None:
        box = freud.box.Box.from_matrix(data.cell.matrix)
        points = data.particles.positions
        system = (box, points)
        ld = freud.density.LocalDensity(r_max,diameter)
        ld.compute(system)
        data.create_user_particle_property(name='LocalDensity', data_type=float, data=ld.density)
        print('Created property for {} particles.'.format(data.particles.count))

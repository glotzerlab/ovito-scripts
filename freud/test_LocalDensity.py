# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import freud
from ovito.data import *

def sense_check(r_max, diameter, dimensions):
    if r_max==0 or diameter==0 or dimensions==0:
        print('WARNING! OVERWRITE VALUES IN SCRIPT')
    return

def modify(frame, input, output):
    #   USER SHOULD SET THESE MANUALLY BEFORE RUNNING SCRIPT
    dimensions = 2
    r_max = 0
    diameter = 0
    sense_check(r_max, diameter, dimensions)
    
    if input.particles is not None:
        box = freud.box.Box.from_matrix(input.cell.matrix, dimensions)
        points = input.particles.position
        system = (box, points)
        print(system)
        # can we automatically detect particle circumsphere diameter?

        ld = freud.density.LocalDensity(r_max,diameter)
        ld.compute(system, input.particles.position)
        output.create_user_particle_property(name='LocalDensity', data_type=float, data=ld.density)
        print('Created property for {} particles.'.format(input.particles.count))

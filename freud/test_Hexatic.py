# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import freud
from ovito.data import *

def sense_check(k):
    if k==0: print('WARNING! OVERWRITE k VALUE IN SCRIPT')
    return

def modify(frame, input, output):
    #   USER SHOULD SET THIS MANUALLY BEFORE RUNNING SCRIPT
    k = 6
    sense_check(k)
    
    if input.particles is not None:
        box = freud.box.Box.from_matrix(input.cell.matrix, dimensions=2)
        points = input.particles.position
        system = (box, points)

        order_param = freud.order.Hexatic(k)
        order_param.compute(system)
        output.create_user_particle_property(name='HexaticOrderParameter', data_type=float, data=order_param.particle_order)
        print('Created property for {} particles.'.format(input.particles.count))

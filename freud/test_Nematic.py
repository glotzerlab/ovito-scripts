# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import freud
import numpy as np
from ovito.data import *

def sense_check(director):
    if director==[]: print('WARNING! OVERWRITE DIRECTOR VALUE IN SCRIPT')
    return

def modify(frame, input, output):
    #   USER SHOULD SET THIS MANUALLY BEFORE RUNNING SCRIPT
    director = np.array([1,1,0])
    sense_check(director)
    
    if input.particles is not None:
        box = freud.box.Box.from_matrix(input.cell.matrix, dimensions=2)
        points = input.particles.position
        system = (box, points)

        order_param = freud.order.Nematic(director)
        order_param.compute(input.particles.orientations)
        output.create_user_particle_property(name='NematicOrderParameter', data_type=float, data=order_param.particle_tensor)
        print('Created property for {} particles.'.format(input.particles.count))

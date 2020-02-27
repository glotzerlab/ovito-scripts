# This software is licensed under the BSD 3-Clause License.

import freud
import numpy as np
from ovito.data import *

def sense_check(director):
    if director==[]: print('WARNING! OVERWRITE DIRECTOR VALUE IN SCRIPT')

def modify(frame, data):
    #   USER SHOULD SET THIS MANUALLY BEFORE RUNNING SCRIPT
    director = np.array([1,1,0])
    sense_check(director)

    if data.particles is not None:
        box = freud.box.Box.from_matrix(data.cell.matrix)
        points = data.particles.positions
        system = (box, points)
        order_param = freud.order.Nematic(director)
        order_param.compute(points.orientations)  # Hasn't been tested.
        data.create_user_particle_property(name='NematicOrderParameter', data_type=float, data=order_param.particle_tensor)
        print('Created property for {} particles.'.format(data.particles.count))

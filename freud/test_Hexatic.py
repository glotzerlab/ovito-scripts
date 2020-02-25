# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import freud
from ovito.data import *
import numpy as np

def sense_check(k):
    if k==0: print('WARNING! OVERWRITE k VALUE IN SCRIPT')
    return

def modify(frame, data):
    #   USER SHOULD SET THIS MANUALLY BEFORE RUNNING SCRIPT
    k = 6
    sense_check(k)

    if data.particles is not None:
        box = freud.box.Box.from_matrix(data.cell.matrix, dimensions=2)
        points = data.particles.positions
        system = (box, points)

        order_param = freud.order.Hexatic(k)
        order_param.compute(system)
        psi_k = np.copy(order_param.particle_order)
        psi_k -= np.mean(psi_k)
        data.create_user_particle_property(name='HexaticOrderParameter', data_type=float, data=np.angle(psi_k, deg=True)/order_param.k)
        print('Created property for {} particles.'.format(data.particles.count))

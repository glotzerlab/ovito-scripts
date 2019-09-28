# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import freud

def modify(frame, input, output):
    if input.particles is not None:
        box = freud.box.Box.from_matrix(input.cell.matrix)
	positions = input.particles.position

        ql = freud.order.LocalQl(box, rmax=3, l=6)
        ql.compute(input.particles.position)
        ql_property = output.create_user_particle_property(name='Ql', data_type=float, data=ql.Ql)
        print('Created Ql property for {} particles.'.format(input.particles.count))

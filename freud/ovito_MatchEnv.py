# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import freud

def modify(frame, input, output):
    if input.particles is not None:
        box = freud.box.Box.from_matrix(input.cell.matrix)
	positions = input.particles.position

        me = freud.environment.MatchEnv(box, rmax=3, k=6)
        me.cluster(input.particles.position, threshold=0.4)
        output.create_user_particle_property(name='MatchEnv', data_type=int, data=me.clusters)
        print('Created property for {} particles.'.format(input.particles.count))

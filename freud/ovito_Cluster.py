# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import freud
import numpy as np

def modify(frame, input, output):
    if input.particles is not None:
	box = freud.box.Box.from_matrix(input.cell.matrix)
	positions = input.particles.position

	bonds_array = input.bonds['Topology'][:]
	distances = np.linalg.norm(box.wrap([positions[j] - positions[i] for i, j in bonds_array]), axis=-1)
	nlist = freud.locality.NeighborList.from_arrays(
	    len(positions), len(positions), bonds_array[:, 0], bonds_array[:, 1], distances)

	cl = freud.cluster.Cluster()
	cl.compute(box, positions, neighbors=nlist)

	cl_props = freud.cluster.ClusterProperties()
	cl_props.compute(box, positions, cl.cluster_idx)

	output.create_user_particle_property(name='ClusterIndex', data_type=int, data=cl.cluster_idx)
	output.create_user_particle_property(name='ClusterSize', data_type=int, data=cl_props.sizes)

	print('Created property for {} particles.'.format(input.particles.count))

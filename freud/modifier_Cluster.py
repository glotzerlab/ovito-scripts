# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import freud
import numpy as np


def modify(frame, data):
    # If neighbors is set to "bonds", it will use the system's
    # bond topology to determine neighbors. Otherwise it should
    # be a dictionary of query arguments like {"r_max": 1.5}.
    neighbors = "bonds"

    if data.particles is not None:
        if neighbors == "bonds":
            bonds_array = data.bonds["Topology"][:]
            system = freud.AABBQuery.from_system(data)
            distances = np.linalg.norm(
                system.box.wrap(
                    system.points[bonds_array[:, 1]] - system.points[bonds_array[:, 0]]
                ),
                axis=-1,
            )
            neighbors = freud.locality.NeighborList.from_arrays(
                len(system.points),
                len(system.points),
                bonds_array[:, 0],
                bonds_array[:, 1],
                distances,
            )

        cl = freud.cluster.Cluster()
        cl.compute(system=data, neighbors=neighbors)

        cl_props = freud.cluster.ClusterProperties()
        cl_props.compute(data, cl.cluster_idx)

        data.create_user_particle_property(
            name="ClusterIndex", data_type=int, data=cl.cluster_idx
        )
        data.create_user_particle_property(
            name="ClusterSize", data_type=int, data=cl_props.sizes[cl.cluster_idx]
        )

        print(f"Created property for {data.particles.count} particles.")

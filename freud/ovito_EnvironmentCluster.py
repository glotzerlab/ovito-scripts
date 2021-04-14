# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import freud


def modify(frame, data):
    r_max = 1.5
    num_neighbors = 12
    threshold = 0.45 * r_max
    registration = False  # Very slow if enabled!
    global_search = False  # Very slow if enabled!

    if data.particles is not None:
        env_cluster = freud.environment.EnvironmentCluster()
        env_cluster.compute(
            system=data,
            threshold=threshold,
            neighbors={"num_neighbors": num_neighbors},
            registration=registration,
            global_search=global_search,
        )
        data.create_user_particle_property(
            name="EnvironmentCluster", data_type=int, data=env_cluster.cluster_idx
        )
        print(f"Created property for {data.particles.count} particles.")

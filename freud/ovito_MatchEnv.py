from ovito.data import *

import freud

def modify(frame, input, output):
    
    r_max = 1.5
    num_neighbors = 12
    threshold = 0.45 * r_max
    registration = False  # Very slow if enabled!
    global_search = False  # Very slow if enabled!
    
    if input.particles is not None:
        env_cluster = freud.environment.EnvironmentCluster()
        env_cluster.compute(input, threshold=threshold,
			    neighbors={'num_neighbors': num_neighbors},
                            registration=registration, global_search=global_search)
        output.create_user_particle_property(name='EnvironmentCluster', data_type=int, data=env_cluster.cluster_idx)
        print('Created property for {} particles.'.format(input.particles.count))

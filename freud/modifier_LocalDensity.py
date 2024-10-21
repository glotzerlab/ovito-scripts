# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import freud


def modify(frame, data):
    if data.particles is not None:
        ld = freud.density.LocalDensity(r_max=3, diameter=0.05)
        ld.compute(data)
        data.create_user_particle_property(name="LocalDensity", data_type=float, data=ld.density)
        print(f"Created property for {data.particles.count} particles.")

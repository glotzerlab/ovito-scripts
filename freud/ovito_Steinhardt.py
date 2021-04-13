# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

import freud


def modify(frame, data):
    if data.particles is not None:
        box = freud.box.Box.from_matrix(data.cell.matrix)
        points = data.particles.positions
        system = (box, points)

        ql = freud.order.Steinhardt(l=6)
        ql.compute(system, {"r_max": 3})
        data.create_user_particle_property(
            name="Ql", data_type=float, data=ql.particle_order
        )
        print(f"Created Ql property for {data.particles.count} particles.")

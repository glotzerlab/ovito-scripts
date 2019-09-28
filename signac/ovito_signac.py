# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

"""Prints signac statepoints."""

import os
import signac

def modify(frame, data):
    source_file = data.attributes['SourceFile']
    dirname = os.path.dirname(source_file)
    job = signac.get_job(dirname)
    for k, v in job.sp.items():
        print(k, v)

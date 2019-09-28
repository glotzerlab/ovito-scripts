# Copyright (c) 2019 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.

"""Prints (nested) statepoints and job documents recursively."""

import os
import signac
from collections.abc import Mapping

def print_recursive(mapping, indent=0):
    indention = '  ' * indent
    for key, value in mapping.items():
        if isinstance(value, Mapping):
            print(f'{indention}{key}:')
            print_recursive(value, indent+1)
        else:
            print(f'{indention}{key}:\t{value}')

def modify(frame, data):
    source_file = data.attributes['SourceFile']
    dirname = os.path.dirname(source_file)
    job = signac.get_job(dirname)
    print('Statepoint:')
    print_recursive(job.sp, 1)
    print('Document:')
    print_recursive(job.doc, 1)

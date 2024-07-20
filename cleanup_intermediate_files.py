#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 15:07:50 2024

@author: vickybuffy
"""

import os
import glob

def cleanup_intermediate_files(source_path, schemes, hemisphere):
    """
    Remove intermediate files created by the get_percentile.py script.

    Parameters
    ----------
    dir_path : str
        Directory where the intermediate files are stored.
    schemes : list of str
        List of schemes used in the project.
    hemisphere : str
        Hemisphere identifier ('ant' for the southern hemisphere, 'arc' for the northern hemisphere).
    """
    for scheme in schemes:
        pattern = os.path.join(source_path, f"{scheme}_per*_{hemisphere}.nc")
        files = glob.glob(pattern)
        for file in files:
            try:
                os.remove(file)
                print(f"Removed file: {file}")
            except OSError as e:
                print(f"Error removing file {file}: {e}")
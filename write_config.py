#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 15:14:09 2024

@author: vickybuffy
"""

import json
import os


# Step 1: Create a dictionary with configuration settings
config = {
    "schemes": ["ILH"],
    "start_year": 1979,
    "end_year": 2023,
    "percentile": 98,
    "hemisphere": "ant",
    "scan_extent": [15, 85],
    "source_path": "/path/where/to/put/input/files/",
    "dir_path": "/path/where/to/put/enar/detection/catalogs/output/",
}

# Step 2: Serialize the dictionary to a JSON formatted string
json_string = json.dumps(config, indent=4)

# Step 3: Write the JSON string to a file
with open('config_ILH.json', 'w') as json_file:
    json_file.write(json_string)

print("Configuration file 'config.json' has been written successfully.")
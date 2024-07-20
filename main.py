#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 14:39:18 2024

@author: vickybuffy
"""    
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from download_era5 import download_data_main
from get_percentile import get_percentile_main
from extract_enar import extract_enar_main
from cleanup_intermediate_files import cleanup_intermediate_files


def load_config(config_file):
    if config_file.endswith('.json'):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        raise ValueError("Config file must be .json file")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    config = load_config(config_file)

    # Download the data
    print('Downloading data...')
    download_data_main(config)

    # Calculate the percentiles
    get_percentile_main(config)

    # Extract atmospheric rivers
    print('Extracting energy atmospheric rivers...')
    extract_enar_main(config)
    
    # Clean up intermediate files
    print('Cleaning intermediate files...')
    cleanup_intermediate_files(config['source_path'], config['schemes'], config['hemisphere'])

    print("Process completed successfully.")
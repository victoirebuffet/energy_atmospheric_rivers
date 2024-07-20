#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 14:34:39 2024

@author: vickybuffy
"""

import cdsapi
import shutil
import os
import glob
from multiprocessing import Pool

# Define parameters and their corresponding datasets
params_datasets = {
    'vSHT': ['vertical_integral_of_northward_heat_flux'],
    'vLHT': ['vertical_integral_of_northward_water_vapour_flux'],
    'ISH': ['vertical_integral_of_thermal_energy'],
    'ILH': ['total_column_water'],
}

param_dataset_map = {
    'vertical_integral_of_thermal_energy': 'reanalysis-era5-single-levels',
    'total_column_water': 'reanalysis-era5-single-levels',
    'vertical_integral_of_northward_water_vapour_flux': 'reanalysis-era5-single-levels',
    'vertical_integral_of_northward_heat_flux': 'reanalysis-era5-single-levels',
}

def download_era5(schemes, years, hemisphere, scan_extent, source_path):
    """
    Parameters
    ----------
    schemes : list of strings
        Desired schemes of the energy atmospheric rivers detection algorithm.
    
    years : tuple of int (starting year, ending year)
        Years to apply the energy atmospheric rivers detection algorithm to.
        
    scan_extent : tuple of int (min lat, max lat)
    
        Latitude extent to apply the energy atmospheric rivers detection algorithm to.
        
    hemisphere : string
        'ant' for the southern hemisphere, 'arc' for the northern hemisphere.
        
    path_to_copy : string
        Path to the folder where to put the data.

    Returns
    -------
    Downloads ERA5 data needed to run the energy atmospheric rivers detection algorithm.
    """
    for scheme in schemes:
        if scheme not in params_datasets:
            print(f'Scheme {scheme} not valid.')
            continue

        params = params_datasets[scheme]
        scan_extent_sorted = sorted([abs(i) for i in scan_extent])
        if max(scan_extent_sorted) > 90 or min(scan_extent_sorted) < 0:
            print('Latitude extents outside of the hemisphere.')

        if hemisphere == 'ant':
            area = '-{}/0/-{}/360'.format(scan_extent_sorted[0], scan_extent_sorted[1])
        elif hemisphere == 'arc':
            area = '{}/0/{}/360'.format(scan_extent_sorted[1], scan_extent_sorted[0])
        else:
            raise ValueError(f"Unknown hemisphere: {hemisphere}")

        c = cdsapi.Client()

        for param in params:
            dataset = param_dataset_map[param]
            list_files = glob.glob(os.path.join(source_path, '*_reanaHS.nc'))
            print(f"Processing parameter: {param}")

            for year in range(years[0], years[1] + 1):
                year_str = str(year)
                file_path = os.path.join(source_path, f'{param}_{year_str}_reanaHS.nc')

                if file_path not in list_files:
                    try:
                        print(f'Downloading {param} for year {year_str} from {dataset}...')
                        c.retrieve(
                            dataset,
                            {
                                'product_type': 'reanalysis',
                                'format': 'netcdf',
                                'variable': [param],
                                'year': year_str,
                                'month': [f'{i:02d}' for i in range(1, 13)],
                                'day': [f'{i:02d}' for i in range(1, 32)],
                                'area': area,
                                'time': ['00:00', '06:00', '12:00', '18:00']
                            },
                            f'{param}_{year_str}_reanaHS.nc'
                        )

                        shutil.copy(f'{param}_{year_str}_reanaHS.nc', file_path)
                        os.remove(f'{param}_{year_str}_reanaHS.nc')
                    except Exception as e:
                        print(f'Error downloading {param} for year {year_str}: {e}')

def download_data_main(config):
    schemes = config['schemes']
    years = (config['start_year'], config['end_year'])
    hemisphere = config['hemisphere']
    scan_extent = config['scan_extent']
    source_path = config['source_path']

    with Pool(4) as p:
        p.starmap(download_era5, [(schemes, years, hemisphere, scan_extent, source_path)])

    print("Download process completed.")
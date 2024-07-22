#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 14:35:06 2024

@author: vickybuffy
"""

import xarray as xr
import os
import numpy as np

# Define constants
latent_heat_vaporization = 2.5008E6  # Latent heat of vaporization

def get_percentile(schemes, years, scan_extent, percentile=98, hemisphere='ant', source_path='.'):
    scan_extent_sorted = sorted([abs(i) for i in scan_extent])
    if max(scan_extent_sorted) > 90 or min(scan_extent_sorted) < 0:
        print('Latitude extents outside of the hemisphere.')

    for scheme in schemes:
        if scheme == 'vLHT':
            long_varname = 'vertical_integral_of_northward_water_vapour_flux'
            varname = 'p72.162'
            factor = latent_heat_vaporization
        elif scheme == 'vSHT':
            long_varname = 'vertical_integral_of_northward_heat_flux'
            varname = 'p70.162'
            factor = 1  # No conversion
        elif scheme == 'ISH':
            long_varname = 'vertical_integral_of_thermal_energy'
            varname = 'p60.162'
            factor = 1  # No conversion
        elif scheme == 'ILH':
            long_varname = 'total_column_water'
            varname = 'tcw'
            factor = latent_heat_vaporization
        else:
            raise ValueError(f"Unknown scheme: {scheme}")

        for month in range(1, 13):
            combined_ds = None
            for year in years:
                filepath = os.path.join(source_path, f"{long_varname}_{year}_reanaHS.nc")
                try:
                    ds = xr.open_dataset(filepath)[varname]
                    ds = ds.sel(time=ds['time.month'] == month) * factor

                    if combined_ds is None:
                        combined_ds = ds
                    else:
                        combined_ds = xr.concat([combined_ds, ds], dim='time')
                except FileNotFoundError:
                    print(f"File not found: {filepath}")
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

            if combined_ds is None:
                print(f"No data found for scheme {scheme} in month {month}. Skipping...")

            if scheme in ['vLHT', 'vSHT']:
                if hemisphere == 'ant':
                    combined_ds = combined_ds.sel(latitude=slice(-scan_extent_sorted[0], -scan_extent_sorted[1]))
                    combined_ds = xr.where(combined_ds < 0, -combined_ds, np.nan)
                elif hemisphere == 'arc':
                    combined_ds = combined_ds.sel(latitude=slice(scan_extent_sorted[1], scan_extent_sorted[0]))
                    combined_ds = xr.where(combined_ds > 0, combined_ds, np.nan)
                else:
                    raise ValueError(f"Unknown hemisphere: {hemisphere}")
            else:
                if hemisphere == 'ant':
                    combined_ds = combined_ds.sel(latitude=slice(-scan_extent_sorted[0], -scan_extent_sorted[1]))
                elif hemisphere == 'arc':
                    combined_ds = combined_ds.sel(latitude=slice(scan_extent_sorted[1], scan_extent_sorted[0]))
                else:
                    raise ValueError(f"Unknown hemisphere: {hemisphere}")

            ds_per = combined_ds.quantile(percentile / 100, dim='time', skipna=True).rename('per')

            # Convert to a new Dataset
            ds_per = ds_per.to_dataset()
            ds_per.attrs['description'] = f"{percentile}th Percentile of {scheme} in ERA-5"

            output_filename = os.path.join(source_path, f"{scheme}_per{percentile}_{month}_{hemisphere}.nc")
            ds_per.to_netcdf(output_filename, mode='w', format='NETCDF4')

def get_percentile_main(config):
    schemes = config['schemes']
    years = range(config['start_year'], config['end_year'] + 1)
    scan_extent = config['scan_extent']
    percentile = config['percentile']
    hemisphere = config['hemisphere']
    source_path = config['source_path']
    
    get_percentile(schemes, years, scan_extent, percentile, hemisphere, source_path)

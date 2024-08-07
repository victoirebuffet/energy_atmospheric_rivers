#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 14:38:46 2024

@author: vickybuffy
"""

import xarray as xr
import numpy as np
from skimage.measure import label, regionprops
import os

len_requirement = 20 # energy AR should extend at least over 20° in the meridional (latitude) direction
latent_heat_vaporization = 2.5008E6  # Latent heat of vaporization

def filter_enARs(ds, lat_resolution):
    """
    Filter out energy atmospheric rivers that are not filamentary enough.
    
    Parameters
    ----------
    ds : xarray dataset of shape (time, lat, lon)
        Binary dataset of values above (1's) the percentile threshold.
                                    
    lat_resolution : float
        The resolution of the data in the meridional direction.

    Returns
    -------
    out_ : array
        Array of similar shape of ds (time,lat,lon) but with only energy atmospheric rivers 
        extending at least over 20° in the meridional (latitude) direction that remain.

    """
    number_of_pixels = int(1 / lat_resolution)*len_requirement
    
    out_ = np.zeros(np.shape(ds.values))

    for i in range(len(ds.time)):
        ar = ds.values[i, :, :].astype(int)
        labeled_ar, num_features = label(ar, return_num=True, connectivity=2)
        regions = regionprops(labeled_ar)

        for region in regions:
            if region.bbox[2] - region.bbox[0] > number_of_pixels :
                for coord in region.coords:
                    out_[i, coord[0], coord[1]] = 1

    return out_


def extract_enar(source_path, year, dir_path, scheme, scan_extent, percentile, hemisphere):
    """
    Extract energy (based on sensible heat and latent heat) atmospheric rivers according to Buffet et al, following the method Wille et al. (2021).

    Parameters
    ----------
    source_path : string
        Path to the era5 data is, as well as the intermediate percentile files.
    year : tuple
        A tuple of two ints, the first being the starting year and the second the ending year.
    output_path : string
        Path to where the energy atmospheric rivers catalogs will be stored.
    scheme : string
        Name of the detection scheme used, can be 'vLHT', 'vSHT', 'ISH' or 'ILH'.
    scan_extent : tuple
        A tuple of two ints, the first being the starting latitde and the second the ending latitude.
    percentile : int
       The percentile used for the detection, by default it is 98, but should be within (excluding) 0-100.
    hemisphere : string
        'ant' for the southern hemisphere, 'arc' for the northern hemisphere.


    Returns
    -------
    Netcdf dataset of binary detection of {scheme} energy atmospheric river for a given year and over a given area according to Buffet et al, following the method Wille et al. (2021).

    """
    months = np.arange(1, 13)
    
    scan_extent_sorted = sorted([abs(i) for i in scan_extent])
    if max(scan_extent_sorted) > 90 or min(scan_extent_sorted) < 0:
        print('Latitude extents outside of the hemisphere.')
    
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

    for month in months:
        ds_open = xr.open_dataset(os.path.join(source_path, f"{long_varname}_{year}_reanaHS.nc"))[varname]
        ds_open = ds_open.sel(time=ds_open['time.month'] == month) * factor
        try :
            ds_per = xr.open_mfdataset(os.path.join(source_path, f"{scheme}_per{percentile}_{month}_{hemisphere}.nc"))['per']
        except OSError:
            print('Please first execute the get_percentile.py script for the needed scheme, percentile and hemisphere setting.')
        
        if hemisphere == 'ant':
            ds_open = ds_open.sel(latitude=slice(-scan_extent_sorted[0], -scan_extent_sorted[1]))
            ds_per = ds_per.sel(latitude=slice(-scan_extent_sorted[0], -scan_extent_sorted[1]))
        elif hemisphere == 'arc':
            ds_open = ds_open.sel(latitude=slice(scan_extent_sorted[1], scan_extent_sorted[0]))
            ds_per = ds_per.sel(latitude=slice(scan_extent_sorted[1], scan_extent_sorted[0]))

        else:
            raise ValueError(f"Unknown hemisphere: {hemisphere}")
            
        lat = ds_open.latitude
        lon = ds_open.longitude
        lat_res = abs(np.array(ds_open.latitude.diff(dim='latitude').min()))
        
        if scheme in ['vLHT', 'vSHT']:
            if hemisphere == 'ant':
                ds = xr.where(ds_open < 0, -ds_open, ds_open * 0.0)  # non-poleward transports are set to 0
            elif hemisphere == 'arc':
                ds = xr.where(ds_open > 0, ds_open, ds_open * 0.0)  # non-poleward transports are set to 0
            else : 
                raise ValueError(f"Unknown hemisphere: {hemisphere}")
        else :
            ds = ds_open.copy()
            
        ds_open.close()

        excess = ds - ds_per
        ds.close()

        out_ar = xr.where(excess > 0, 1, 0).copy().squeeze()
        
        excess.close()
        
        df_loc = xr.concat([out_ar, out_ar], dim='longitude')
        
        df_loc = filter_enARs(df_loc, lat_res)
        outy = df_loc[:,:,:len(lon)]+df_loc[:,:,len(lon):]
        outy[outy>1] = 1
        out_ar.values = outy.astype(int)
        
        if month == 1:
            ds_combined = xr.Dataset(
                {
                    "enar_binary_tag": (["time", "lat", "lon"], out_ar.data)
                },
                coords={
                    "time": out_ar.time.data,
                    "lat": lat.data,
                    "lon": lon.data,
                },
            )
        else:
            ds = xr.Dataset(
                {
                    "enar_binary_tag": (["time", "lat", "lon"], out_ar.data)
                },
                coords={
                    "time": out_ar.time.data,
                    "lat": lat.data,
                    "lon": lon.data,
                },
            )
            ds_combined = xr.concat([ds_combined, ds], dim='time')

    ds_combined.attrs['description'] = f"Binary indicator of energy atmospheric river using {scheme} ERA-5"
    ds_combined.attrs['credits'] = "Developed by V. Buffet, B. Pohl and V. Favier from Wille et al. 2021 & Lapere et al. 2024."

    try:
        from dask.diagnostics import ProgressBar

        delayed_obj = ds_combined.to_netcdf(
            os.path.join(dir_path, f'artmip_enar_tag_buffet_{year}_era5_{scheme}_{percentile}p_{scan_extent[0]}-{scan_extent[-1]}_{hemisphere}.nc4'),
            compute=False
        )

        with ProgressBar():
            delayed_obj.compute()

    except ImportError:
        ds_combined.to_netcdf(
            os.path.join(dir_path, f'artmip_enar_tag_buffet_{year}_era5_{scheme}_{percentile}p_{scan_extent[0]}-{scan_extent[-1]}_{hemisphere}.nc4')
        )

    ds_combined.close()

def extract_enar_main(config):
    source_path = config['source_path']
    dir_path = config['dir_path']
    schemes = config['schemes']
    scan_extent = config['scan_extent']
    years = range(config['start_year'], config['end_year'] + 1)
    percentile = config['percentile']
    hemisphere = config['hemisphere']
    
    for scheme in schemes:
        for year in years:
            extract_enar(source_path, year, dir_path, scheme, scan_extent, percentile, hemisphere)

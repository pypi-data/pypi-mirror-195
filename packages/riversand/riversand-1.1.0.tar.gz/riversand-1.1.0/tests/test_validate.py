#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 09:29:46 2023

@author: Konstanze Stübner, kstueb@gmail.com

"""

import pytest
from pytest import mark

import sys, os
import pandas as pd
import numpy as np

import rasterio
import fiona
from pyproj.crs import CRS
#import pyproj.exceptions
import xarray as xr

import riversand

def test_params():
    assert riversand.params.url == "http://stoneage.hzdr.de/cgi/matweb"


def test_validate_empty_project(path):
    rv = riversand.Riversand(path)
    out = rv.validate(verbose=False)
    assert out==(['No elevation raster defined'],
                 ['No sample data defined'],
                 ['No catchment data defined'])
    
def test_validate_single_catchment(path):
    """ single-catchment dataset, different rasters """
    rv = riversand.Riversand(path)
    
    # no raster data
    rv.add_catchments('test_single_catchment.shp')
    out = rv.validate(verbose=False)
    assert out==(['No elevation raster defined'],
                 ['No sample data defined'],
                 ['No valid raster data, cannot validate shapefile projection'])

    # shielding but no elevation
    rv.add_raster('toposhielding_35m.tif', dtype='shielding')
    out = rv.validate(verbose=False)
    assert out==(['No elevation raster defined'],
                 ['No sample data defined'],
                 ['No valid raster data, cannot validate shapefile projection'])
    
    # elevation raster invalid projection
    rv.add_raster('dem_WGS.tif', dtype='elevation')
    out = rv.validate(verbose=False)
    assert out==(['Conflicting projections in raster data'],
                 ['No sample data defined'],
                 ['No valid raster data, cannot validate shapefile projection'])
    assert rv.epsg is None
    assert rv.res is None
    
    # valid raster data
    rv.add_raster('dem_utm_35m.tif', dtype='elevation')
    out = rv.validate(verbose=False)
    assert out==([],
                 ['No sample data defined'],
                 [])
    assert rv.epsg==32632
    assert rv.res==(35,35)
    assert rv.valid_catchments is None # not set for single-catchment
    
    rv.set_cid('name')
    out = rv.validate(verbose=False, multi=True)
    assert out==([],
                 ['No sample data defined'],
                 [])
    assert rv.epsg==32632
    assert rv.res==(35,35)
    assert rv.valid_catchments==[] # no valid catchments found
    
    

def test_validate_out_of_bounds(path):
    """ single / doesn't matter for multi-catchment """
    rv = riversand.Riversand(path)
    rv.add_raster('dem_utm_35m.tif', dtype='elevation')
    rv.add_raster('toposhielding_35m_tooSmall.tif', dtype='shielding')
    rv.add_samples('test_samples1.ods')
    rv.add_catchments('test_single_catchment.shp')
    
    out = rv.validate(verbose=False)
    assert out==([],
                 [],
                 ['Catchment polygon out of bounds of raster data'])
    
    rv.add_catchments('test_multi_catchment.shp')
    rv.set_cid('name')
    out = rv.validate(verbose=False)
    assert out==([],
                 [],
                 [])
    assert rv.valid_catchments==['DB02', 'DB04', 'DB05', 'DB12', 'DB17', 'DB19']


def test_validate_valid_complete_single_catchment(path):
    """ validate as single (auto) or as multi (multi=True) """
    
    rv = riversand.Riversand(path)
    rv.add_raster('dem_utm_35m.tif', dtype='elevation')
    rv.add_raster('toposhielding_35m.tif', dtype='shielding')
    rv.add_raster('quartz_35m.tif', dtype='quartz')    
    rv.add_samples({'N': 5e+4, 'delN': 5e+2})
    #rv.add_samples(fname='test_samples_single.ods', path=path)
    rv.add_catchments('test_single_catchment.shp')
    
    out = rv.validate(verbose=False)
    assert out==([],[],[])
    assert rv.epsg==32632
    assert rv.res==(35,35)
    assert rv.valid_catchments is None # not set for single-catchment
    
    out = rv.validate(verbose=False, multi=True)
    assert out[2]==['No catchment identifier defined; use .set_cid()']
    assert rv.valid_catchments is None
    
    rv.set_cid('bogus') # will print an error message
    
    rv.set_cid('name')
    out = rv.validate(verbose=False, multi=True)
    assert out==([],[],[])
    assert rv.valid_catchments==[] # no valid catchments found
    
    rv.add_samples({'name': 'DB05', 'N': 5e+4, 'delN': 5e+2})
    out = rv.validate(verbose=False, multi=True)
    assert out==([],[],[])
    assert rv.valid_catchments==['DB05']
    
def test_validate_valid_complete_multi_catchment(path):
    """ validate as multi (auto) or as single (multi=False) """
    
    rv = riversand.Riversand(path)
    rv.add_raster('dem_utm_35m.tif', dtype='elevation')
    rv.add_raster('toposhielding_35m.tif', dtype='shielding')
    rv.add_raster('quartz_35m.tif', dtype='quartz')    
    rv.add_samples('test_samples1.ods')
    rv.add_catchments('test_multi_catchment.shp')
    
    rv.set_cid('name')
    out = rv.validate(verbose=False)
    assert out==([],[],[])
    assert rv.epsg==32632
    assert rv.res==(35,35)
    assert rv.valid_catchments==['DB02', 'DB04', 'DB05', 'DB12', 'DB17', 'DB19']
    
    out = rv.validate(verbose=False, multi=False)
    assert out[2]==['Not a single-catchment dataset (8 polygons)']
    assert rv.valid_catchments is None

    
    
    
    
    
    
    
    
    
    
    
import numpy as np
import pandas as pd
import xarray as xr
import pymannkendall as pymk

from datarie.time import index

def anom_trends(arrays_: dict[str, np.ndarray],
                y0: int,
                y1: int,
                time_res: str,
                baseline_y0: int,
                baseline_y1: int,
                m0:int = 1,
                m1: int = 12,
                test: str = 'original_test',
                leapday: bool = False,
                **kwargs):
        
    for k, v in arrays_.items():
        
        if ((k == 'SM') and (v.ndim > 1)):
            sm12 = xr.DataArray(v[:, 0:2],
                                dims = ('time', 'levsoi'),
                                name = 'SM')
            
            weights = xr.DataArray([0.01, 0.04], 
                                   dims = ('levsoi',),
                                   name = 'weights')
            
            sm12_weighted = sm12.weighted(weights)
            sm12_weighted_mean = sm12_weighted.mean(dim = 'levsoi')
            
            arrays_[k] = sm12_weighted_mean.to_numpy().astype('float64')

    time_index = index(y0 = y0,
                       y1 = y1,
                       month0 = m0,
                       month1 = m1,
                       t_res = time_res,
                       leapday = leapday)
    
    anomalies = baseline_anomalies(arrays = arrays_,
                                   baseline_y0 = baseline_y0,
                                   baseline_y1 = baseline_y1,
                                   time_index = time_index)
    
    trends = mannkendall(anomalies,
                         test,
                         **kwargs)
    
    return trends


def baseline_anomalies(arrays: dict[str, np.ndarray],
                       baseline_y0: int,
                       baseline_y1: int,
                       time_index: pd.Series):
    
    xarr = xr.Dataset(data_vars = {k: (['time'], v)
                                   for k, v in arrays.items()},
                      coords = {'time': time_index}).convert_calendar('noleap')
    
    xarr.coords['dayofyear'] = xarr['time'].dt.dayofyear

    base_mean = xarr.sel(time=slice(f'{baseline_y0}-01-01', 
                                    f'{baseline_y1}-12-31'))\
                                    .groupby(dayofyear = xr.groupers.UniqueGrouper())\
                                    .mean()
    
    xarr_anom = xarr.groupby(dayofyear = xr.groupers.UniqueGrouper()) - base_mean

    return {str(k): v.to_numpy() 
            for k, v in xarr_anom.items()}


def mannkendall(arrays: dict[str, np.ndarray],
                test: str = 'original_test',
                **kwargs):

        dict_out = {}

        for v, array in arrays.items():
        
            if np.isnan(array).all(): 
            
                dict_out[f'{v}_slope'] = np.nan
                dict_out[f'{v}_p'] = np.nan
        
                continue

            if np.all(array == array[0]):
                
                dict_out[f'{v}_slope'] = np.nan
                dict_out[f'{v}_p'] = np.nan
                
                continue
            
            if np.count_nonzero(np.isnan(array)) > 0.7 * len(array):
                
                dict_out[f'{v}_slope'] = np.nan
                dict_out[f'{v}_p'] = np.nan
                
                continue

            if array.ndim == 1:

                func = getattr(pymk, test)
            
                result = func(array, **kwargs)
    
            else: 
            
                NotImplementedError('Input array needs to be one-dimensional.')
    
            dict_out[f'{v}_slope'] = result.slope
            dict_out[f'{v}_p'] = result.p
    
        return dict_out

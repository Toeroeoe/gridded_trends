import netCDF4 as nc
import numpy as np
from pathlib import Path

from neoplot import figures, plots
from datarie import grids, templates, PRUDENCE

# Data settings
indir = '/p/scratch/cjibg31/jibg3105/projects/papers/CLM5EU3_trends/out/trend_data/eCLM_trends/'
infile = 'CLM5_detect_SP_upd_0_3km.nc'
outdir = '/p/scratch/cjibg31/jibg3105/projects/papers/CLM5EU3_trends/out/plots/eCLM_paper/'

variable = 'SM'
source = 'CLM5-SP-EU3'
grid = 'EU3'
units = {'TWS': r'mm month$^{-1}$',
         'ET': r'mm month$^{-1}$',
         'SM': r'm$^{3}$ m$^{-3}$ month$^{-1}$'}

outfile = f'{variable}_{source}_trend_prudence_boxplot'
plot_args = {
            'fs_title': 12,
            'fs_label': 10,
            'TWS': {'vmax': 7,
                     'vmin': -7},
            'SM': {'vmax': 0.001,
                   'vmin': -0.001},
            'ET': {'vmax': 0.005,
                   'vmin': -0.005},
            'significance': 0.05,
            'hatch_density': 3,
            'hatch_pattern': '.'
            }


if __name__ == '__main__':

    data = nc.Dataset(f'{indir}/{infile}')

    array = data.variables[f'{variable}_slope'][:]

    p_val = data.variables[f'{variable}_p'][:]

    EU_grid = templates.grid(**getattr(grids, grid))

    lat, lon = EU_grid.load_coordinates()

    fig = figures.single_001(fx = 5.,
                             fy = 4.,).create()
    
    ax = plots.boxplot(ax = fig.axs[0],
                       title = f'{source} {variable} trends in PRUDENCE regions',
                       fs_title = plot_args['fs_title'],
                       ylabel = f'slope [{units[variable]}]',
                       fs_label = plot_args['fs_label'],).create()
    
    regions = list(PRUDENCE.regions.keys())
    
    prudence_arrays = [PRUDENCE.mask_prudence(array,
                                              lat = lat,
                                              lon = lon,
                                              sel_regions = r)
                       for r in regions]
    
    prudence_arrays_clean = [arr[~np.isnan(arr)]
                             for arr in prudence_arrays]
    
    boxp = ax.boxplot(data = prudence_arrays_clean,
                      tick_labels = regions,
                      fliers = False)
    
    fig.save(Path(f'{outdir}/{outfile}'))
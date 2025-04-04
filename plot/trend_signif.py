
import netCDF4 as nc
from pathlib import Path

from neoplot import figures, plots
from datarie import grids, templates

# Data settings
indir = '/p/scratch/cjibg31/jibg3105/projects/papers/CLM5EU3_trends/out/trend_data/eCLM_trends/'
infile = 'CLM5_detect_SP_upd_0_3km.nc'
variable = 'TWS'
units = {'TWS': r'mm month$^{-1}$',
         'ET': r'mm month$^{-1}$',
         'SM': r'm$^{3}$ m$^{-3}$ month$^{-1}$'}
outdir = '/p/scratch/cjibg31/jibg3105/projects/papers/CLM5EU3_trends/out/plots/eCLM_paper/'
outfile = f'{variable}_CLM5EU3_SP_trend_signif'


# Plot settings
plot_args = {
            'fs_title': 12,
            'fs_label': 10,
            'TWS': {'vmax': 5,
                     'vmin': -5},
            'SXI_SM_r': {'vmax': 0.002,
                         'vmin': -0.002},
            'significance': 0.05,
            'hatch_density': 3,
            'hatch_pattern': '.'
            }



if __name__ == '__main__':

    data = nc.Dataset(f'{indir}/{infile}')

    array = data.variables[f'{variable}_slope'][:]

    p_val = data.variables[f'{variable}_p'][:]

    EU3_grid = templates.grid(**grids.EU3)

    lat, lon = EU3_grid.load_coordinates()

    fig = figures.single_001(fx = 5,
                             fy = 4.,
                             projection = 'EU3').create()

    ax = plots.amap(ax = fig.axs[0],
                    lon_extents = EU3_grid.lon_extents,
                    lat_extents = EU3_grid.lat_extents,
                    title = f'{variable}',
                    fs_label = plot_args['fs_label'],
                    fs_title = plot_args['fs_title'],
                    fs_ticks = plot_args['fs_label']).create()
    
    trend = ax.colormesh(lon = lon,
                         lat = lat,
                         array = array,
                         cmap = 'coolwarm_r',
                         vmin = plot_args[variable]['vmin'],
                         vmax = plot_args[variable]['vmax'])
    
    signif = ax.contourf(lon = lon,
                         lat = lat,
                         array = p_val,
                         levels = [0.0, 
                                   plot_args['significance']],
                         hatches = [plot_args['hatch_pattern']*plot_args['hatch_density'],
                                    ''],
                         colors = 'none',
                         alpha = None,
                         extend = 'neither')
    
    ax.colorbar(trend, 
                ax = ax.ax,
                label = f'Trend [{units[variable]}]',
                shrink = 0.6,
                fs_label = plot_args['fs_label'])

    ax.hatch_legend(fig = fig.fig,
                    dict_hatch = {'p ≤ 0.05': {'hatch': plot_args['hatch_pattern']*5,
                                               'facecolor': 'none'}},
                    anchor = (0.1, 0.9),)
    
    fig.save(Path(f'{outdir}/{outfile}'))
    



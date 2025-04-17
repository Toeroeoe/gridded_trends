
import netCDF4 as nc
from pathlib import Path

from neoplot import figures, plots
from datarie import grids, templates

# Data settings
indir = '/p/scratch/cjibg31/jibg3105/projects/papers/CLM5EU3_trends/out/trend_data/eCLM_trends/'
infile = 'GLEAM_ET_upd_1_3km.nc'
outdir = '/p/scratch/cjibg31/jibg3105/projects/papers/CLM5EU3_trends/out/plots/eCLM_paper/'

variable = 'ET'
source = 'GLEAM-EU3'
grid = 'EU3'
units = {'TWS': r'mm month$^{-1}$',
         'ET': r'mm day$^{-1}$ month$^{-1}$',
         'SM': r'm$^{3}$ m$^{-3}$ month$^{-1}$'}



# Plot settings
outfile = f'{variable}_{source}_trend_signif_map_upd_1'
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
    
    fig = figures.single_001(fx = 5,
                             fy = 4.,
                             projection = 'EU3').create()

    ax = plots.amap(ax = fig.axs[0],
                    lon_extents = EU_grid.lon_extents,
                    lat_extents = EU_grid.lat_extents,
                    title = f'{source} {variable}',
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
                    dict_hatch = {f"p ≤ {plot_args['significance']}": {'hatch': plot_args['hatch_pattern']*5,
                                               'facecolor': 'none'}},
                    anchor = (0.1, 0.92),)
    
    fig.save(Path(f'{outdir}/{outfile}'))
    



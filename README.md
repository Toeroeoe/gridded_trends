## Changes (need to update README):
- new parameters for script including function arguments
- plot script included.


# Calculate model trends on HPC
This was developed to calculate Mann-Kendall trend statistics on a per-pixel basis over any domain.

Your data requirements:
- Dataset must be in netcdf format
- The dataset must be stored in yearly files (e.g., 1995.nc, 1996.nc, etc.)

## Step by step
### 1. Create your own data dictionary based on the template in `data_config.py`
| Parameter | data type | Description |
| --- | --- | --- |
| name | str | Any name of your choice, not relevant |
| version | tuple[int] | A tuple of the size three, not relevant |
| path | str | The path to the yearly data files |
| type_file | str | The data type format. Only netcdf is supported |
| year_start | int | The first year with available data |
| month_start | int | The month in the first year from which data is available |
| year_end | int | The last year with available data |
| month_end | int | The month in the last year until data is available |
| leapday | bool | True if leapday (29th February is present in the data) |
| resolution_time | str | [time offset string](https://pandas.pydata.org/docs/user_guide/timeseries.html#dateoffset-objects) of data time resolution |
| grid | str | name of the grid the data is based on, not relevant |
| variables | list[str] | All the variables available in the dataset |
| variable_names | dict[str, str] | dict relating common variable names to the ones in the dataset |
| variable_dimensions | dict[str, list] | The dimensions of the data. Lat and Lon must be last two dimensions |
| variable_units | dict[str, str] | units of the variables, not relevant | 
| mask_values | None or int or float | Potential mask values in the data, e.g. -9999 that will be considered nan |

### 2. Adjust the settings in `calculate_trends.py`
1. `data`: The name of the data dictionary you created before 
2. `variables`: The variable names you want to calculate the trends for
3. `outfile`: The name of the output file
4. `units`: The units of the variable for the slope variable

### 3. Adjust the loaded environment in `submit.sh`
Please source your environment file in `submit.sh` in line 8. Importantly, the environment must contain the `crusty` PyPI package and its dependencies. It can be installed by `pip install crusty`.

## To Do
- Probably it is more convinient to define all the settings in the submit.sh, and parse it as arguments to the pythons script.
- Functionally allow for different pymannkendall functions by parameter setting.
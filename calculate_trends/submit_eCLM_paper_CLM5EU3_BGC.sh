#!/bin/bash -x
#SBATCH --job-name=trends
#SBATCH --account=jibg31
#SBATCH --ntasks=128
#SBATCH --mem=512000
#SBATCH --time=30:00

# Environment
source /p/scratch/cjibg31/jibg3105/projects/venvs/test_crusty/activate.sh

# Data
data=CLM5_detect_BGC_3
outdir=/p/scratch/cjibg31/jibg3105/projects/papers/CLM5EU3_trends/out/trend_data/eCLM_trends/
outfile=CLM5_detect_BGC_upd_1_3km.nc
variables=(
    TWS
    ET
    SM
)

units="{'TWS_slope': 'mm month^-1',
        'ET_slope': 'mm day^-1 month^-1',
        'SM_slope': 'm^3 m^-3 month^-1',
        'TWS_intercept': 'mm month^-1',
        'ET_intercept': 'mm day^-1 month^-1',
        'SM_intercept': 'm^3 m^-3 month^-1',
        'TWS_p': 'dimensionless',
        'ET_p': 'dimensionless',
        'SM_p': 'dimensionless'}"

# function name and arguments
# please provide a string in python dict form
func_name=anom_trends
year_start=2002
year_end=2022
month_start=4
month_end=7
func_args="{'y0': 2002,
            'y1': 2022,
            'm0': 4,
            'm1': 7,
            'baseline_y0': 2003,
            'baseline_y1': 2016,
            'test': 'seasonal_test',
            'time_res': 'MS',
            'period': 12}"

# run parallel
srun \
    python calculate_trends.py \
        --data $data \
        --variables ${variables[@]} \
        --year_start $year_start \
        --year_end $year_end \
        --month_start $month_start \
        --month_end $month_end \
        --slope_units "$units" \
        --outfile ${outdir}/${outfile} \
        --func_name $func_name \
        --func_args "$func_args"

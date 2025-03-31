#!/bin/bash -x
#SBATCH --job-name=trends
#SBATCH --account=jibg31
#SBATCH --ntasks=128
#SBATCH --mem=512000
#SBATCH --time=30:00

# Environment
source /p/scratch/cjibg31/jibg3105/projects/venvs/test_crusty/activate.sh

# Data
data=GLEAM_ET
outdir=/p/scratch/cjibg31/jibg3105/projects/papers/CLM5EU3_trends/out/trend_data/
outfile=GLEAM_ET_upd_0.nc
variables=(
    ET
)

slope_units="mm day^-1 month^-1"

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
        --slope_units "$slope_units" \
        --outfile ${outdir}/${outfile} \
        --func_name $func_name \
        --func_args "$func_args"

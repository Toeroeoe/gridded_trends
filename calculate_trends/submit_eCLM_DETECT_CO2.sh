#!/bin/bash -x
#SBATCH --job-name=trends
#SBATCH --account=jibg31
#SBATCH --ntasks=256
#SBATCH --mem=512000
#SBATCH --time=10:00:00

# Environment
source /p/scratch/cjibg31/jibg3105/projects/venvs/test_crusty/activate.sh

# Data
data=CLM5_detect_SP
outdir=/p/scratch/cjibg31/jibg3105/projects/papers/CLM5EU3_trends/out/trend_data/
outfile=CLM5_detect_SP_TWS_trends.nc
variables=(
    TWS
)
slope_units="mm day^-1"

# function name and arguments
# please provide a string in python dict form
func_name=anom_trends
func_args="{'y0': 2000,
            'y1': 2022,
            'baseline_y0': 2003,
            'baseline_y1': 2016,
            'test': 'seasonal_test',
            'time_res': 'D'}"

# run parallel
srun \
    python calculate_trends.py \
        --data $data \
        --variables ${variables[@]} \
        --slope_units "$slope_units" \
        --outfile $outfile \
        --func_name $func_name \
        --func_args "$func_args"

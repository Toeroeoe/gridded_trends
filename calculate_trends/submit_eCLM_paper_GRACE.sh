#!/bin/bash -x
#SBATCH --job-name=trends
#SBATCH --account=jibg31
#SBATCH --ntasks=128
#SBATCH --mem=512000
#SBATCH --time=30:00

# Environment
source /p/scratch/cjibg31/jibg3105/projects/venvs/test_crusty/activate.sh

# Data
data=GRACE_TWS
outdir=/p/scratch/cjibg31/jibg3105/projects/papers/CLM5EU3_trends/out/trend_data/
outfile=GRACE_TWS_upd_0.nc
variables=(
    TWS
)

slope_units="mm month^-1"

# function name and arguments
# please provide a string in python dict form
func_name=mannkendall
year_start=2002
year_end=2022
month_start=4
month_end=7

func_args="{'test': 'seasonal_test',
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

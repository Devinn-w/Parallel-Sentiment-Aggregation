#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=0-5:00:00
#SBATCH --output=output_144g_%j.txt

module load Python/3.10.4
module load mpi4py/3.1.4

INPUT_FILE="${1:-mastodon-144g.ndjson}" 

echo "Processing file: $INPUT_FILE"
time mpiexec -n $SLURM_NTASKS python sentiment_mpi_analysis.py -i $INPUT_FILE

#!/bin/bash
#SBATCH --job-name=v2g_annotate
#SBATCH --output=logfile_sbatch.txt
#SBATCH --partition=cpuq
#SBATCH --cpus-per-task=5
#SBATCH --mem=10G
#SBATCH --time=00:40:00

source /ssu/gassu/miniconda3/etc/profile.d/conda.sh
conda activate tiledb
python v2g_dask_query.py -i variants_query.txt -o variants_anno_out.tsv
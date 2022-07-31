#!/bin/bash
#SBATCH --job-name=mpi-bc

#SBATCH --output=output_100.txt
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=10
#SBATCH -A cpu-s2-hpdic-0
#SBATCH -p cpu-s2-core-0

#SBATCH --mem-per-cpu=2000M

#module load python
#module load mpi4py

time mpiexec python key_distribution_in_cluster.py
#srun hostname

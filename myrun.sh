#!/bin/bash
#SBATCH --job-name=mpi-bc

#SBATCH --output=consensus_output_100.txt
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=20
#SBATCH -A cpu-s2-hpdic-0
#SBATCH -p cpu-s2-core-0

#SBATCH --mem-per-cpu=2000M

#module load python
#module load mpi4py

time mpiexec python consensus.py
#srun hostname

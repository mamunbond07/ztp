#!/bin/bash
#SBATCH --job-name=mpi-bc

#SBATCH --output=keysend_output_40.txt
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=20
#SBATCH -A cpu-s2-hpdic-0
#SBATCH -p cpu-s2-core-0

#SBATCH --mem-per-cpu=2000M

#module load python
#module load mpi4py

time mpiexec python key_send.py
#srun hostname

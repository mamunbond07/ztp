#!/bin/bash

time mpiexec -n 20 python key_distribution_in_cluster.py
time mpiexec -n 40 python key_distribution_in_cluster.py
time mpiexec -n 60 python key_distribution_in_cluster.py
time mpiexec -n 80 python key_distribution_in_cluster.py
time mpiexec -n 100 python key_distribution_in_cluster.py 

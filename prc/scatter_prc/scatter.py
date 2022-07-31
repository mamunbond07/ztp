import numpy as np
from mpi4py import MPI
from pprint import pprint
comm = MPI.COMM_WORLD

pprint("-" * 78)
pprint(" Running on %d cores" % comm.size)
pprint("-" * 78)

N = 100
my_N = N // 8

if comm.rank == 0:
    A = np.arange(N, dtype=np.float64)
else:
    A = np.empty(N, dtype=np.float64)

my_A = np.empty(my_N, dtype=np.float64)

# Scatter data 
comm.Scatter([A, MPI.DOUBLE], [my_A, MPI.DOUBLE])

pprint("After Scatter:")
for r in range(comm.size):
    if comm.rank == r:
        print("[%d] %s" % (comm.rank, len(my_A)))
    comm.Barrier()

# Allgather data into A
comm.Allgather([my_A, MPI.DOUBLE], [A, MPI.DOUBLE])

pprint("After Allgather:")
for r in range(comm.size):
    if comm.rank == r:
        print("[%d] %s" % (comm.rank, len(A)))
    comm.Barrier()


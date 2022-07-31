#!/usr/bin/env python

'''
Author: Abdullah Al Mamun.
Email: aalmamun@nevada.unr.edu
Code revisions:
3/21/2022: key distribution among the HPC cluster by the data owner.
'''


import json
import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
tasks = []

if comm.rank == 0:
    #json.dumps( { 'a':1,'x':2,'b':3 } )
    for i in range(comm.size):
        tasks.append(json.dumps( { 'a':1,'x':2,'b':3 } ))
    '''
    tasks = [
        json.dumps( { 'a':1,'x':2,'b':3 } ),
        json.dumps( { 'a':3,'x':1,'b':2 } ),
        json.dumps( { 'a':2,'x':3,'b':1 } )
    ]
    '''
else:
    tasks = None


# Scatter paramters arrays
unit = comm.scatter(tasks, root=0)

p = json.loads(unit)
print( "-"*18)
print("-- I'm rank %d in %d size task" % (comm.rank,comm.size) )
print("-- My paramters are: {}".format(p))
print("-"*18)

comm.Barrier()

calc = p['a']*p['x']**2+p['b']

# gather results
result = comm.gather(calc, root=0)
# do something with result

if comm.rank == 0:
    print("the result is ", result)
else:
    result = None

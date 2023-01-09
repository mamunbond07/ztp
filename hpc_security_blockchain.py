#!/usr/bin/env python
"""
Author:         
Usage:          mpiexec -n <thread #> python -O mpi_blockchain.py
Input:          None
Output:         <thread #> of files with commited transactions in ./output/
Start Date:     02/05/2022
Desc:           A quick prototype of blockchain using MPI
Change History:    
                02/09/2022: Reorg the output directory.
                02/08/2022: 2PQC is implemented.
                02/06/2022: came up with the idea of 2PQC.
"""


from mpi4py import MPI
import sys, datetime, os


### 2PQC: 2-Phase Quorum Commit Protocol: A MPI-based 2-phase commit protocol with quorum check
### The idea is simple: why can't we plug in the quorum check into the 2PC protocol in HPC blockchain?
### If we really think about 2PC and consensus, 2PC is nothing but checking all participants are ready/done for commit
### On the other hand, consensus requires us to reach 51% decision. That's it.
### In HPC, we don't care about Bazyntine failures; there's only fail-restart scenario.
def dc_2pqc(received_txn, output_path):
    """A distributed commit protocol named two-phase quorum commit.

    Args:
        received_txn (string): received transaction to be committed
        output_path (string): the output directory of the committed transactions

    Returns: 
        None

    """
    comm = MPI.COMM_WORLD
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()
    
    ##################
    # Phase 1: prepare
    ##################
    request = comm.bcast("prepare", root=0)
    if __debug__:
        sys.stdout.write("Rank %d receives request: %s\n" % (rank, request))

    # for now, assume all ranks are ready to commit; we can change it later
    ready = 1 # 1: ready; 0: not ready
    reply = comm.gather(ready, root=0)
    if __debug__:
        if 0 == rank:
            sys.stdout.write("Phase 1 done. Reply: %s (rank %d)\n" % (reply, rank))

    #################
    # Phase 2: commit
    #################
    ready_to_commit = 0
    if 0 == rank:
        if sum(reply) >= size/2: #we don't need to have all votes, but only the majority
            ready_to_commit = 1
    #broadcast the decision
    ready_to_commit = comm.bcast(ready_to_commit, root=0) #this is very important, easy to make mistakes
    
    if __debug__ and 0 == rank:
        sys.stdout.write("sum(reply) = %d, ready_to_commit = %d\n" % (sum(reply), ready_to_commit))

    local_commit = 0
    if ready_to_commit:
        #commit the local transaction, e.g., write the txn to a local file
        for r in range (0, size):
            if rank == r:
                fp = open(output_path+"/log"+str(rank)+".txt", "a+")
                fp.write("log"+str(rank)+" at "+str(datetime.datetime.now())+": "+received_txn+"\n")
                fp.close()
                local_commit = 1 #so, now the transaction is committed, i.e., written to the disk
    done = comm.gather(local_commit, root=0)

    #report the final result of the (decentralized) transaction
    if 0 == rank:
        if sum(done) >= size/2.0:
            sys.stdout.write("Transaction committed successfully.\n")
        else:
            sys.stdout.write("Transaction failed to commit.\n")


### submit a txn request from a client, which is always rank-0
def submit_txn(txn):
    txn = comm.bcast(txn, root=0)
    return txn


### process the txn on each ndoe (i.e., rank)
def process_txn():
    # For example, deduct $100 from A and credit it to B on a local replica
    pass


### commit a txn request
def commit_txn(received_txn, output_path):
    # there're many distributed commit protocols, e.g., 2PC, PBFT; we'll use 2pc for now
    dc_2pqc(received_txn, output_path)


### Entry point
if __name__ == '__main__':

    comm = MPI.COMM_WORLD
    size = MPI.COMM_WORLD.Get_size()
    rank = MPI.COMM_WORLD.Get_rank()
    name = MPI.Get_processor_name()

    # Create the output directory
    #if 0 == rank:
    output_path = "./output"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # simple test for various ranks
    if __debug__:
        if rank == 0:
            data = {'a': 7, 'b': 3.14}
            comm.send(data, dest=1, tag=11)
        elif rank == 1:
            data = comm.recv(source=0, tag=11)
            sys.stdout.write("%s received at rank %d\n"
                    % (data, rank))

    # transaction submitter, usually from a client, assuming always on rank 0, need a broadcast here
    txn = ""
    if 0 == rank:
        txn = "A transfers $100.00 USD to B."
    for i in range(4): 
        received_txn = submit_txn(txn+str(i))

        if __debug__: 
            sys.stdout.write("received_txn = %s received at rank %d \n" % (received_txn, rank))

    # proceed the transaction, on all nodes
        process_txn()

    # commit the transaction, usually initiated by a leader
        commit_txn(received_txn, output_path)


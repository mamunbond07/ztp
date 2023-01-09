# ZTP: Lightweight, Efficient, and Reliable Blockchain Privacy for Distibuted Systems
ZTP is an early prototype, designed with a lightweight decentralized parallel processing protocol fully compatible with MPI and the distributed-storage architecture to provide blockchain-like distributed resilience support while avoiding the conventional TCP/IP stack through the support of MPI for the heavy-workload applications..

## ZTP Workflow
<img src="https://user-images.githubusercontent.com/44820439/211341566-3651a90b-5d5a-4c6f-84f4-c9c3085c853b.png" width="600" height="500">

## ZTP Parallel Key Accumalator
<img src="https://user-images.githubusercontent.com/44820439/211342146-aa72d2f9-a149-41a7-9ea0-cb24403612b9.jpg" width="600" height="500">

## Quick facts on ZTP version 1.0.0
* ZTP is designed specifically for providing privacy support to blockchain architecture to provide distributed trustworthy resilience support.
* ZTP can be deployed both in the userspace as well as at the system level through a wrapper.
* ZTP does not use traditional resource intensive protocols (e.g., proof-of-work, practical byzantine fault tolerance, proof-of-stake).
* ZTP is fully compatible with OpenMP and MPI library.
* ZTP doesn't require TCP/IP stack.
* ZTP supports parallel transaction processing and comes with a scalable decentralized protocol to support distributed resiliency.
* During parallel processing ZTP keeps minimum 3f+1 nodes in a sub-cluster, where f is the maximum number of faulty nodes.
* A fault tolerance mechanism with a global hook is injected to provide consistent ZTP service during MPI rank failure.


## System requirements
Python 3.7.0, NumPy 1.15.4, mpi4py v2.0.0, and mpich2 v1.4.1

## ZTP execution
The ZTP has been developed with Python. The ZTP is executed with Slurm workload manager. Please see the slurm documentation (https://slurm.schedmd.com/documentation.html) for more details for all the parameters. If you prefer other workload manager, please follow the documentation to set up the parameters before executing the BAASH service.
Please set all properties mentioned in the script.sh following the documentation of your preferred workload manager before lauching the ZTP service.

### Brief explantion of the parameters in myrun.sh
 * time: Total time for execution.
 * nodes: Total nodes to use as distributed ledger.
 * ntasks-per-node: Number of threads to run in each node.
 * mem-per-cpu: Amount of memory allocated for each thread.
 * output: contains the execution/debugging output (if any).

### Quick Execution 
sbatch script.sh

## ZTP documentation
We have provided detailed inline comments for all the non-trivial code blocks in the code.


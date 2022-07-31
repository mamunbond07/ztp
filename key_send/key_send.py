from mpi4py import MPI

comm = MPI.COMM_WORLD
rank=comm.rank
size=comm.size
name=MPI.Get_processor_name()

for i in range(1,size):
    if rank == 0:
        shared = {'d1':55,'d2':42}
        comm.send(shared, dest=i)

if rank != 0:
    receive = comm.recv(source=0)
    print("key", receive,"received at node", rank)
    #print(receive['d1'])

        

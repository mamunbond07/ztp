from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

data2=0
data=0

if rank == 0:
   data = [1,2,3] #[(x+1)**x for x in range(size)]
   print('we will be scattering:',data)
else:
    try:
        f = open(str(rank)+".txt", "r")
        data2 = f.read()
    #data2 = [4,5,6]
    except:
        data2= "no data"
   
data3 = comm.bcast(data, root=0)

print('rank',rank,'has data:',data2)

newData = comm.gather(data2,root=0)

if rank == 0:
   print('master:',newData)

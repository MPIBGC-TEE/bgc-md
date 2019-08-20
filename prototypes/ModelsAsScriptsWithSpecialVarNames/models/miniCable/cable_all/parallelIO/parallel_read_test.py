#! /usr/bin/env python3 
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
#amode = MPI.MODE_WRONLY|MPI.MODE_CREATE
amode = MPI.MODE_RDONLY
fh = MPI.File.Open(comm, "./datafile.contig", amode)

buffer = np.empty(10, dtype=np.int32)
#buffer[:] = comm.Get_rank()

offset = comm.Get_rank()*buffer.nbytes
print("offset"+str(offset))
#fh.Write_at_all(offset, buffer)
fh.Read_at_all(offset, buffer)
print(buffer)

fh.Close()

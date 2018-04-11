#!/usr/bin/env python3
# vim: set expandtab ts=4

from mpi4py import MPI
import numpy
import sys
import dill
import pickle
from mpi_master_slave_common_mod_for_functions import g 

def mpi_wrapper(np=2):
    comm = MPI.COMM_SELF.Spawn(sys.executable,
                               args=['mpi_slave.py'],
                               maxprocs=np)
    
    # serialize and broadcast a function containing a lambda
    f=lambda x:g(x)**2
    comm.bcast(dill.dumps(f),root=MPI.ROOT)
    
    # now use recursive lambdas
    f1=lambda x:f(x)
    f2=lambda x:f1(x)
    l=locals()
    
    comm.bcast(dill.dumps(l),root=MPI.ROOT)
    
    
    # scatter data (one list element to every core)
    data=[i for i in range(np)]
    print(data)
    comm.scatter(data,root=MPI.ROOT)
    
    PI = numpy.array(0, dtype='d')
    comm.Reduce(None, [PI, MPI.DOUBLE],
                op=MPI.SUM, root=MPI.ROOT)
    ##
    comm.Disconnect()
    return(PI)

mpi_wrapper(3)
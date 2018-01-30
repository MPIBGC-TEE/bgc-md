
# vim: set expandtab ts=4
from mpi4py import MPI
import numpy
import dill
import pickle
from mpi_master_slave_common_mod_for_functions import g
#from pickle import loads 
comm = MPI.Comm.Get_parent()
size = comm.Get_size()
rank = comm.Get_rank()

# get values from the broadcasts
# note that the variables have to be defined before they can
# be used in as receiving buffers
f=None
f=dill.loads(comm.bcast(f,root=0))

l=None
l=dill.loads(comm.bcast(l,root=0))
data=None
data=comm.scatter(data,root=0)
#f=dill.loads(d["f"])
print(data)

# we can now even use recursively defined lamdas if we evaluate them
# in the environment in which they were defined
print("l:",l)
print(eval("f2(2)",l))
print("locals:",locals())


PI = numpy.array(f(rank), dtype='d')
comm.Reduce([PI, MPI.DOUBLE], None,
            op=MPI.SUM, root=0)
comm.Disconnect()

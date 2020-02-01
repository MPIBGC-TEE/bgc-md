from typing import List
from sympy import Symbol,symbols
from sympy.matrices import ImmutableMatrix
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel 

#Mvars...
class CompartmentalMatrix(ImmutableMatrix):
    pass

class InputTuple(ImmutableMatrix):
    # we could have the constructor check for a one 
    # dimensional and positive input
    pass

class StateTuple(ImmutableMatrix):
    # we could have the constructor check for a one 
    # dimensional and purely symbolic input
    pass

class TimeSymbol(Symbol):
    pass

# Computers
def reservoirModel(
        sv  :StateTuple
       ,t   :TimeSymbol
       ,A   :CompartmentalMatrix
       ,I   :InputTuple
    ) -> SmoothReservoirModel:
    return SmoothReservoirModel.from_B_u(sv,t,A,I) 
    

# start inspections
# to build graph
from inspect import signature 
sig=signature(reservoirModel)
print([val.annotation.__name__ for key,val in sig.parameters.items()])
# ['StateTuple', 'TimeSymbol', 'CompartmentalMatrix', 'InputTuple']


# testcode 
# should be constructed from a chosen path through the graph
a,b,t=symbols('a,b,t')
sv  = StateTuple([a,b])
cm  = CompartmentalMatrix([[1,a],[a,a]])
i   = InputTuple([3,2])
mod = reservoirModel(sv,t,cm,i)

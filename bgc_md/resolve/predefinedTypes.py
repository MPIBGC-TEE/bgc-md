# this is realated to a prototype that will try to identify Mvars by their type
# annotation in the model src file
from sympy import Matrix,Symbol,Basic
from typing import Tuple,NewType
# define type aliases
CompartmentalMatrix
# 
InternalFlux=Tuple[Symbol,Symbol,Basic]


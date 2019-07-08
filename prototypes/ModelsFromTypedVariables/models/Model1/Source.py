from bgc_md.resolve.predefinedTypes import CompartmentalMatrix,InternalFlux
from sympy import Matrix,Symbol
# correct example
A:CompartmentalMatrix=Matrix([[1,2],[3,4]])

# define an example variable
a=Symbol('a')
b=Symbol('b')
it_ab:InternalFlux =(a,b,4*a**2)

import helpers
from sympy import MatrixSymbol, Function, sympify

N = MatrixSymbol('N', 3, 3)
C = MatrixSymbol('C', 3, 1)
#f = symbols('f', cls=Function)
#s = helpers.non_commutative_sympify("")

s = sympify("C*N", locals={'N': N, 'C': C})

print(s)
print(type(s))



from __future__ import division 
from sympy import * 
from sympy.matrices import Matrix, diag

# Reference: 

#t = # units: sec

# State variables
C_f, C_r, C_w = symbols('C_f C_r C_w') #Carbon in foliage, roots and woody tissue

#Photosynthetic parameters/variables
G_max = symbols('G_max') # Maximum photosynthetic rate
I = symbols('I') # Light interception factor
E = symbols('E') # PAR use efficiency

# Allocation coefficients
eta_f, eta_r, eta_w = symbols('eta_f eta_r eta_w')

#Cycling rates
gamma_f, gamma_r, gamma_w = symbols('gamma_f gamma_r gamma_w')

# Model components
x = Matrix(3,1, [C_f, C_r, C_w])
u = G_max*I*E
b = Matrix(3,1,[eta_f, eta_r, eta_w])
A = diag(-gamma_f, -gamma_r, -gamma_w)

fv = u*b + A*x

pprint(fv)

#Parameters
eta_f = 0.5 # units


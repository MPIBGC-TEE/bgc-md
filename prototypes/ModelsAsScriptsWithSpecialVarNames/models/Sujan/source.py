from sympy import Symbol,symbols,Number
from sympy.vector import CoordSysND,express,Vector,Dyadic
# fixme mm:
# add this boilerplatecode automatically
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from CompartmentalSystems.smooth_model_run import SmoothModelRun
from CompartmentalSystems.helpers_reservoir import numerical_function_from_expression
from bgc_md.DescribedSymbol import DescribedSymbol
from bgc_md.DescribedQuantity import DescribedQuantity
# the next line will change to an import from CompartmentalSystem
# once the new constructor is established
from bgc_md.resolve.functions import srm_from_B_u_tens
# all variables starting with def_  are 
from sympy import Symbol,symbols,solve, pi, Eq, Min, Max ,Matrix, Function, Piecewise, exp
from sympy import pprint
from sympy.physics.units import mass,time
from sympy.physics.units import year,day,second,minute
from sympy.physics.units import meter, kilogram
from sympy.physics.units.dimensions import dimsys_SI
from sympy.physics.units import convert_to
from numpy import linspace,array
from pathlib import Path
import csv
def f(S):
    return 0.1*S
# local imports
t=Symbol('t')
## first we initialize the symbolic ReservoirModel

S_1, S_2, S_3 = symbols('S_1 S_2 S_3')
t = symbols('t')
I_1_expr = Function('I_1')(t)
alpha, beta = symbols('alpha beta')
k_3 = symbols('k_3')
S_1max = symbols('S_1max')

state_vector = Matrix(3,1, [S_1, S_2, S_3])

# flux rate from S_1 to S_2
a_21 = (f(S_1)*f(S_2))**(1/2)

# decomposition rate of S_1
a_11 = -(1/(S_1**(1/alpha))*(S_1+I_1_expr)/(S_1max))**alpha \
       -(1/(S_1**(1/alpha))*(S_1-((S_1+I_1_expr)/S_1max)**alpha/S_1max))**beta \
       -a_21

# no flux from S_1 to S_3
a_31 = 0

# no flux from S_2 to S_1
a_12 = 0

# decomposition rate of S_2
a_22 = -(f(S_2)*f(S_3))**(1/2)

# flux rate from S_2 to S_3
a_32 = (f(S_2)*f(S_3))**(1/2)

# no flux from S_3 to S_1
a_13 = 0

# no flux from S_3 to S_2
a_23 = 0

# outflow rate of S_3
a_33 = -k_3

# compose the (nonlinear) compartmental matrix
A = Matrix([[a_11, a_12, a_13],
            [a_21, a_22, a_23],
            [a_31, a_32, a_33]])

# input vector
I = Matrix(3,1,[I_1_expr,0,0])

srm = SmoothReservoirModel.from_B_u(
    state_vector,
    t,
    A,
    I
)
special_vars={
    #'coord_sys':CoordS #Coordinate syste
    'input_tuple':I
    ,'compartmental_matrix':A
    ,'time_symbol':t
    ,'state_vector':state_vector
    #,'smooth_reservoir_model':srm # this line should become obsolete since the preceding itmes clearly contain sufficient information . 
    #,'smooth_model_run_dictionary':{'default':smr}
    #,'smooth_model_run':smr 
}

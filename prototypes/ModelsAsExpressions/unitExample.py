from sympy import symbols,solve, pi, Eq
from sympy.physics.units import length, mass, acceleration, force
from sympy.physics.units import Quantity 
from sympy.physics.units import day, gravitational_constant as G
from sympy.physics.units import meter, kilogram
from sympy.physics.units.dimensions import dimsys_SI
from sympy.physics.units import convert_to
F = mass*acceleration
F
dimsys_SI.get_dimensional_dependencies(force)
dimsys_SI.equivalent_dims(F, force)
T = symbols("T")
a = Quantity("venus_a")
a.set_dimension(length,"SI")
a.set_scale_factor(108208000e3*meter, "SI")
M=Quantity("solar mass")
M.set_dimension(mass,"SI")
M.set_scale_factor(1.9891e30*kilogram,"SI")
eq=Eq(T**2/a**3,4*pi**2/G/M)
sols=solve(eq,T)
q=sols[1]
convert_to(q,day).n()

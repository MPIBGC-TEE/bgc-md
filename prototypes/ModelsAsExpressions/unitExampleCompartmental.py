
from sympy import symbols,solve, pi, Eq ,Matrix
from sympy.physics.units import mass,time
from sympy.physics.units import Quantity 
from sympy.physics.units import year,day,second,minute
from sympy.physics.units import meter, kilogram
from sympy.physics.units.dimensions import dimsys_SI
from sympy.physics.units import convert_to

class MyQuantity(Quantity):
    def set_description(self,description):
        self.description=description

class MySymbol(Symbol):
    def set_description(self,description):
        self.description=description

s=MyQuantity("s")
s.set_dimension(mass,"SI")
s.set_description("Soil carbon ")

s=MyQuantity("l")
s.set_dimension(mass,"SI")
s.set_description("Leaf carbon ")

k_s=MyQuantity("k_s")
k_s.set_dimension(mass/time,"SI")
k_s.set_description("Soil respiration rate")

k_l=MyQuantity("k_l")
k_l.set_dimension(mass/time,"SI")
k_l.set_description("Leaf respiration rate")

B=Matrix([[k_l,0],[0,k_s]])


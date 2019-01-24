from sympy.physics.units import Quantity 
class DescribedQuantity(Quantity):
    def set_description(self,description):
        self.description=description

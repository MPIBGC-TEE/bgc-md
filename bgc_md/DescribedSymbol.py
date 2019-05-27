from sympy import symbols,Symbol
class DescribedSymbol(Symbol):
    def set_description(self,description):
        self.description=description

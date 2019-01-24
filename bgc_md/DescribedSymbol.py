from sympy import symbols,Symbol
class DesribedSymbol(Symbol):
    def set_description(self,description):
        self.description=description

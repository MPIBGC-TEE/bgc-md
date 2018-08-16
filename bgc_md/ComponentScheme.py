from sympy import Symbol
class ComponentScheme:
    # this class will be merged with the corresponing class in the yaml_creator app 
    @classmethod
    def from_yaml_subdict(cls,ysd):
        cs=object.__new__(cls)
        cs.statevector_str=ysd['statevector']
        return cs

    @property
    def state_variable_symbols(self):
        cs_str=self.statevector_str
        symbol_set=set([Symbol(s) for s in cs_str.split(",")])
        return symbol_set

        

        

        

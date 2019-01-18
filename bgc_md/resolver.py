from sympy import Symbol,Number
from sympy.vector import CoordSysND,express,Vector,Dyadic
from typing import List
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
#from CompartmentalSystems import smooth_reservoir_model 
from testinfrastructure.helpers import pe
special_var_string="special_vars"
class MVar:
    # A (M)ultiply defined (Var)iable that can possibly be computed 
    # in several ways defined by the computers
    # and can check if one of them works given a namespace
    # the default [] for the computers means that the 
    # only known way to get the variable is that the user 
    # directly defined it.
    def __init__(self,name,computers:List['Computer']=[]):
        self.name       = name
        self.computers  = computers

    def is_computable(self,name_space:dict):
        if self.name in name_space.keys():
            return True
        else:
            return any( c.is_computable(name_space) for c in  self.computers) 

    def computable_computers(self,name_space):
        coms=[
            c for c in self.computers 
            if c.is_computable(name_space)
        ]
        pe('coms',locals())
        return coms

    def __call__(self,name_space):
        print('######### here ##############')
        print(self.name)
        print(name_space.keys())
        if self.name in name_space.keys():
            return name_space[self.name]
        # check which computers actually are computable and
        # take the first one
        else:
            working_computers=self.computable_computers(name_space)
            if len(working_computers)>0:
                return working_computers[0](name_space)
            else:
                raise Exception("The Mvar can not be computed from the given namespace")


class Computer:
    # this is like a function that knows what MVars it needs
    def __init__(self,func,args:List['MVar']):
        #to do:
        # make sure that the function func accomodates
        # the args 
        # (maybe also check the type if func has been annotated)
        self.func=func
        self.args=args
    
    def is_computable(self,name_space):
        return all( mvar.is_computable for mvar in  self.args) 
    
    def __call__(self,name_space):
        vals=[arg(name_space) for arg in self.args]
        pe('vals',locals())
        return self.func(*vals)

    


def srm_from_B_u_tens(
        C:CoordSysND
        ,state_vector:Vector
        ,time_symbol:Symbol
        ,B:Dyadic
        ,u:Vector
    )->'SmoothReservoirModel':
    state_vector_mat=express(state_vector,C).to_matrix(C)
    B_mat=express(B,C).to_matrix(C)
    u_mat=express(u,C).to_matrix(C)
    #pe('state_vector',locals())
    #pe('state_vector_mat',locals())
    #pe('B_mat',locals())
    #pe('u_mat',locals())
    return SmoothReservoirModel.from_B_u(state_vector_mat,time_symbol,B_mat,u_mat)

smr_bu_tens=Computer(
    func=srm_from_B_u_tens,args=[
         MVar(name='coord_sys') 
        ,MVar(name='state_vector') 
        ,MVar(name='time_symbol') 
        ,MVar(name='compartmental_dyad') 
        ,MVar(name='input_vector') 
     ]
)
smooth_reservoir_model=MVar('smooth_reservoir_model',computers=[smr_bu_tens])

    

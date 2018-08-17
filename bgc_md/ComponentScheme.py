from sympy import Symbol
import inspect
from abc import ABCMeta, abstractmethod
from bgc_md.helpers import pp,pe

def remove(mylist,i):
    left =mylist[:i]
    right=mylist[(i+1):]
    rest=left+right
    #print('left',left)
    #print('right',right)
    #print('rest',rest)
    return(rest)

def sigma_alg(myset):
    # compute the sigma algebra (the powerset of a set)
    l=len(myset)
    mylist=list(myset)
    if l==0:
        return []
    if l==1:
        return frozenset([myset]) # a set of one set...
    if l>1:
        result=set()
        for i in range(l):
            rest=frozenset(remove(mylist,i))
            sub_set=sigma_alg(rest)
            print('sub_set',sub_set)
            for s in sub_set:
                result.add(s)
        result.add(myset)   
        return frozenset(result)

class ComponentScheme(metaclass=ABCMeta):
    # this class will be merged with the corresponing class in the yaml_creator app 
    # It is an abstract class that can not be directly instanciated.
    # 

    # this method has to be implemented by every subclass
    @abstractmethod
    def reservoir_model(self):
        pass


    @classmethod
    def init_arg_sets(cls):
        # this function inspects the init method of the subclass cls
        # and returns a set of possible argument_names
        # which can be mached against the available one
        # in order to find the subclass that can be instantiated
        sig=inspect.signature(cls.__init__)
        fas=inspect.getfullargspec(cls.__init__)
        pars=dict(sig.parameters)

        #get rid of the first arg (usually self)
        pars.pop(fas.args[0])

        # filter out the parameters of init that have no default value
        required_arg_names=set([k  for k,v in pars.items() if v.default==inspect._empty])
        # args with default value are considered optional
        optional_arg_names=frozenset(pars.keys()).difference(required_arg_names)
        optional_arg_combies=sigma_alg(optional_arg_names)

        arg_combies=[ required_arg_names.union(fs) for fs in optional_arg_combies]

        # any com
        return arg_combies

    
    
    def args2attributes(self):
        # an optional helper method for lazy people who do not want to write
        # code self.x=x ;self.y=y and so on
        # Do not use it if you want init to check the values of its arguments before it populates the object 

        #get the calling func
        caller=inspect.currentframe().f_back
        #and its arguments
        arg_names,_,_,arg_val_dict,=inspect.getargvalues(caller)
        # remove the first argument (usually self) 
        del arg_val_dict[arg_names[0]]
        # now set attributes with the same name as the keywordarguments
        for k,v in arg_val_dict.items():
            setattr(self,k,v)


class Vegetation_Matrices(ComponentScheme):
    def __init__(self,scalar_func_phot,part_coeff,cyc_matrix,test=None,tes2=2):
        self.args2attributes()
    
    def reservoir_model(self):
        pass 

        
class Fluxes(ComponentScheme):
    def __init__(self,external_input_flux_dict=None,internal_flux_dict=None,external_output_flux_dict=None):
        self.args2attributes()
        
Vegetation_Matrices.init_arg_sets()
        

        


@unittest.skip
class TestDicts(unittest.TestCase):

    def test_computability(self):
        from sympy import Symbol,Number
        from typing import List
        from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
        from CompartmentalSystems.smooth_model_run import SmoothModelRun
        #from CompartmentalSystems import smooth_reservoir_model 
        from testinfrastructure.helpers import pe
        from bgc_md.resolve.ClassesWithIndex import MVar2,Computer2
        from bgc_md.resolve.functions import srm_from_B_u_tens
        
        # Here we explore the possibility to define both the 'args; of the 
        # Computer instance and the 'computers' in a MVar instance
        # not as objects but as strings interpreted with respect to a
        # dictionary of Mvars or Computers respectively and resolve
        # the relationship at runtime. This allows any kind of cross 
        # referencing even if the variables or computers do not 
        # exist yet or not at all. The latter possibility must be excluded
        # by a consistence check
        
        myComputers={}
        myMvars={
            'coord_sys':            MVar2(myComputers,'coord_sys') 
            ,
            'state_vector':          MVar2(myComputers,'state_vector')
            ,
            'time_symbol':           MVar2(myComputers,'time_symbol') 
            ,
            'compartmental_dyad':    MVar2(myComputers,'compartmental_dyad') 
            ,
            'input_vector':          MVar2(myComputers,'input_vector') 
            ,
            'parameter_dictionary':  MVar2(myComputers,'parameter_dictionary') 
            ,
            'start_vector':          MVar2(myComputers,'start_vector') 
            ,
            'time_vector':           MVar2(myComputers,'time_vector') 
            ,
            'function_dictionary':   MVar2(myComputers,'function_dictionary')
            ,
            'smooth_reservoir_model':
                MVar2(
                    'smooth_reservoir_model'
                    ,myComputers
                    ,computerNames=['srm_bu_tens']
                    ,description='A smooth reservroir Model'
                )
            ,'smooth_model_run_dictionary':
                MVar2(
                    'smooth_model_run_dictionary'
                    ,myComputers
                    ,computerNames=[] # at the moment empty list, consequently 
                    # only available when explicitly defined. 
                    # Although automatic computation would be simple 
                    # the keys make most sense if defined by the user
                    ,description= """
                    The dictionary values are SmoothModelRun objects. 
                    The keys can be used in user code to refer to special 
                    simulations. """
            )
            ,'smooth_model_run':MVar2(
                    'smooth_model_run'
                    ,myComputers
                    ,computerNames=['smr']
                    ,description= """A single simulation"""
            )
        }
        
# update the up to now empty ComputerDict        
        myComputers.update({
            'srm_bu_tens':
                Computer2(
                     myMvars
                    ,func=srm_from_B_u_tens
                    ,arg_names=[
                         'coord_sys'
                        ,'state_vector' 
                        ,'time_symbol' 
                        ,'compartmental_dyad' 
                        ,'input_vector' 
                     ]
                    ,description="""Produces a smoth reservoir model"""
                )
            ,'smr':
                Computer2(
                     myMvars
                    ,SmoothModelRun
                    ,arg_names=[
                         'smooth_reservoir_model'
                        ,'parameter_dictionary'
                        ,'start_vector'
                        ,'time_vector'
                        ,'function_dictionary'
                    ]
                    ,description="""Creates a single instance of a SmoothModelRun"""
                )
        })
        md=get2(var_name="smooth_reservoir_model",allMvars=myMvars,model_id='testFivePool')
        pe('md.compartmental_matrix',locals())





import unittest
from bgc_md.resolve.helpers import  get3, computable_mvars
from bgc_md.resolve.MVar import MVar
from bgc_md.resolve.Computer import Computer
from bgc_md.resolve.functions import srm_from_B_u_tens
from bgc_md.resolve.IndexedSet import IndexedSet
class TestResolveFramework(unittest.TestCase):

    def test_computability(self):
        # Here we explore the possibility to define both the 'args; of the 
        # Computer instance and the 'computers' in a MVar instance
        # not as objects but as strings interpreted with respect to a
        # set of Mvars or Computers respectively and resolve
        # the relationship at runtime by the name attribute of both. 
        # This finally removes the duplication and allows any kind of cross 
        # referencing even if the variables or computers do not 
        # exist yet or not at all. The latter possibility must be excluded
        # by a consistence check

        myMvars=IndexedSet({
            MVar('a',description= """ a varible we assume to be given """)
            ,MVar('b')
            ,MVar('c')
            ,MVar('d')
            ,MVar('f') 
            ,MVar('e')
        })
        myComputers=IndexedSet({
            Computer(
                'd(a,c)'
                ,func=lambda a,c:(a+3)+c # we make it consistent to the other computeer d_from_b_c
                ,description="""computes d from a  and c """
            )
            ,Computer(
                'd(b,c)'
                ,func=lambda b,c:b+c
                ,description="""computes d from a  and c """
            )
            ,Computer(
                'c(b)'
                ,func=lambda b:2*b
                ,description="""computes c from b"""
            )
            ,Computer(
                'b(a)'
                ,func=lambda a: a+3
                ,description="""computes b from a"""
            )
            ,Computer(
                'f(e)'
                ,func=lambda e: e**2
                ,description="""computes f from e"""
            )
        })
        names_of_available_mvars=frozenset(['a']) 
        
        # check computers 
        
        self.assertTrue(    myComputers['b(a)'].is_computable(myMvars,myComputers,names_of_available_mvars))

        #c is recursively computable through b
        self.assertTrue(    myComputers['c(b)'].is_computable(myMvars,myComputers,names_of_available_mvars))
        
        #d is recursively computable through c
        self.assertTrue(    myComputers['d(a,c)'].is_computable(myMvars,myComputers,names_of_available_mvars))
        
        #d is recursively computable through b and c
        self.assertTrue(    myComputers['d(b,c)'].is_computable(myMvars,myComputers,names_of_available_mvars))
        
        #f is not computable since e is neither defined nor computable
        self.assertTrue(not myComputers['f(e)'].is_computable(myMvars,myComputers,names_of_available_mvars))
      
        # check mvars separately
        self.assertTrue(    myMvars['a'].is_computable(myMvars,myComputers,names_of_available_mvars))
        self.assertTrue(    myMvars['b'].is_computable(myMvars,myComputers,names_of_available_mvars))
        self.assertTrue(    myMvars['c'].is_computable(myMvars,myComputers,names_of_available_mvars))
        self.assertTrue(    myMvars['d'].is_computable(myMvars,myComputers,names_of_available_mvars))
        self.assertTrue(not myMvars['e'].is_computable(myMvars,myComputers,names_of_available_mvars))
        self.assertTrue(not myMvars['f'].is_computable(myMvars,myComputers,names_of_available_mvars))

        mvars=computable_mvars(
                allMvars=myMvars
                ,allComputers=myComputers
                ,names_of_available_mvars=frozenset(['a']) 
        )
        #pe('mvars',locals())
        # e and f are not computable
        self.assertEqual(mvars,frozenset({
            MVar( 'a' ,description= """ a varible we assume to be given """)
            ,MVar( 'b')
            ,MVar( 'c')
            ,MVar( 'd')
         }))


    def test_computability_bgc(self):
        # here we test the (growing) sets of Mvars and Computers included in the packe
        from bgc_md.resolve.MvarsAndComputers import Mvars as myMvars
        from bgc_md.resolve.MvarsAndComputers import Computers as myComputers
        
        
        # compute the set of computable Mvars from the names of defined variables 
        # this is the set of mvars supposedly given in the model file 
        names_of_available_mvars=frozenset([
             'coord_sys'
            ,'state_vector' 
            ,'time_symbol' 
            ,'compartmental_dyad' 
            ,'input_vector'
        ]) 
        C=myComputers['smooth_reservoir_model(coord_sys,state_vector,time_symbol,compartmental_dyad,input_vector)']
        ref=[ 'coord_sys' ,'state_vector' ,'time_symbol' ,'compartmental_dyad' ,'input_vector' ]
        self.assertEqual( C.arg_names , ref)
        
        mvars=computable_mvars(
                allMvars=myMvars
                ,allComputers=myComputers
                ,names_of_available_mvars=names_of_available_mvars
        )
        res=set([v.name for v in mvars])
        ref=set([
            'coord_sys'
            ,'state_vector'
            ,'state_tuple'
            ,'time_symbol'
            ,'compartmental_dyad'
            ,'input_vector'
            ,'input_tuple'
            ,'smooth_reservoir_model' # new (provided by computers)
            ,'compartmental_matrix'   # new (provided by computers)
        ])
        self.assertEqual(res,ref)


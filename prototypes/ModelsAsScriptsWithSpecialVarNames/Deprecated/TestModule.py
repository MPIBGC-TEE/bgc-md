@unittest.skip
class TestModules(InDirTest):

    def test_defined_mvars(self):
        # we want to see what variables are at least defined
        # in an example namespace defined by a module
        mls=remove_leading_whitespace('''
        from bgc_md.resolve.Classes import MVar,Computer
        from bgc_md.resolve.helpers import srm_from_B_u_tens
        
        coord_sys           = MVar(name='coord_sys') 
        state_vector        = MVar(name='state_vector') 
        time_symbol         = MVar(name='time_symbol') 
        compartmental_dyad  = MVar(name='compartmental_dyad') 
        input_vector        = MVar(name='input_vector') 
        srm_bu_tens=Computer(
            func=srm_from_B_u_tens
            ,args=[
                 coord_sys 
                ,state_vector 
                ,time_symbol 
                ,compartmental_dyad 
                ,input_vector 
             ]
            ,description="""Produces a smoth reservoir model"""

        smooth_reservoir_model=MVar(
                 name='smooth_reservoir_model'
                ,computers=[srm_bu_tens]
                ,description='A smooth reservroir Model'
        )
        
        ''',8)
        mp=Path('mymod.py')
        with mp.open('w') as f:
            f.write(mls)

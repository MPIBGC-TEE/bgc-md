import unittest
from testinfrastructure.helpers import pe
from sympy import Symbol,Number,symbols,Matrix,Rational
from sympy.vector import CoordSysND,express,Vector,Dyadic,matrix_to_vector
from bgc_md.resolve.functions import permutationMatrix
from bgc_md.resolve.MvarsAndComputers import Mvars as allMvars 
from bgc_md.resolve.MvarsAndComputers import Computers as allComputers
from bgc_md.DescribedSymbol import DesribedSymbol
from bgc_md.DescribedQuantity import DescribedQuantity
from bgc_md.reports import produce_model_report_markdown, produce_model_report_markdown_directory,  defaults,render
from sympy import symbols,solve, pi, Eq ,Matrix
from sympy.physics.units import mass,time
from sympy.physics.units import Quantity 
from sympy.physics.units import year,day,second,minute
from sympy.physics.units import meter, kilogram
from sympy.physics.units.dimensions import dimsys_SI
from sympy.physics.units import convert_to

class TestReportTemplates(unittest.TestCase):
    def test_documented_Quanteties(self):
        s=DescribedQuantity("s")
        s.set_dimension(mass,"SI")
        s=DescribedQuantity("s")
        s.set_dimension(mass,"SI")
        s.set_description("Soil carbon ")
        
        l=DescribedQuantity("l")
        l.set_dimension(mass,"SI")
        l.set_description("Leaf carbon ")
        
        k_s=DescribedQuantity("k_s")
        k_s.set_dimension(mass/time,"SI")
        k_s.set_description("Soil respiration rate")
        
        k_l=DescribedQuantity("k_l")
        k_l.set_dimension(mass/time,"SI")
        k_l.set_description("Leaf respiration rate")

        B=Matrix([[k_l,0],[0,k_s]])
        

        #s.set_description("Soil carbon ")
        # the model defining script or the UI can add symbols and quanteties to the model
        # It should an ordered dict to give control to the user
        name_space={
                'documented_identifiers':[k_s,k_l,l,s]
                ,'compartmental_matrix':B
                ,'state_tuple':Matrix([l,s])
        }
        #d=defaults() 
        #tp=d['paths']['static_report_templates'].joinpath('SectionVariablesTable.py')
        #rel=render(tp,name_space)
        rel=allMvars['documented_identifiers_table_rel'](allMvars,allComputers,name_space)

    def test_render_cable(self):
        d=defaults() 
        sp=d['paths']['new_models_path'].joinpath('miniCable')
        tp=d['paths']['static_report_templates'].joinpath('SectionVariablesTable.py')
        mns=populated_namespace_from_path(sp)
        render2(tp,mns)
            #m=Model.from_path(rec)
            #rel=render(tp,model=m)
#

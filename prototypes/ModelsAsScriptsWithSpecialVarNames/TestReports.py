import unittest
from testinfrastructure.helpers import pe 
from testinfrastructure.InDirTest import InDirTest
from pathlib import Path
from sympy import Symbol,Number,symbols,Matrix,Rational
from sympy.vector import CoordSysND,express,Vector,Dyadic,matrix_to_vector
from bgc_md.resolve.functions import permutationMatrix
from bgc_md.resolve.MvarsAndComputers import Mvars as allMvars 
from bgc_md.resolve.MvarsAndComputers import Computers as allComputers
from bgc_md.resolve.helpers import special_vars 
from bgc_md.DescribedSymbol import DescribedSymbol
from bgc_md.DescribedQuantity import DescribedQuantity
from bgc_md.reports import produce_model_report_markdown, produce_model_report_markdown_directory,  defaults,render2
from sympy import symbols,solve, pi, Eq ,Matrix
from sympy.physics.units import mass,time
from sympy.physics.units import Quantity 
from sympy.physics.units import year,day,second,minute
from sympy.physics.units import meter, kilogram
from sympy.physics.units.dimensions import dimsys_SI
from sympy.physics.units import convert_to

class TestReportTemplates(unittest.TestCase):
    @unittest.skip
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

class TestReportGeneration(InDirTest):
    def test_render_cable_overview(self):
        #    There are two kinds of templates:
        #    1. Overview templates with possibly missing parts:
        #       We will have overview templates that do not know beforehand which of their
        #       parts can be filled with values. These templates should receive 
        #       a collection of MVars (maybe the whole namespace as extracted from a model file) 
        #       as argument. Even if some of the MVars they would present are unavailable 
        #       The overview should still be presented (in a shortened way).
        #       It does not make sense to treat these templates as MVars since we would
        #       have to provide a computer for every still presentable subset of the 
        #       MVars they need.
        #    2. Specific subtemplates that make only sense if all the presented MVars are available: 
        #       They are in fact MVars themselves with one specific Computer and we can check if 
        #       they are computable given a namespace as for other MVars.
        #       This is interesting for the GUI which can on the fly decide which things to show
        #   
        #    In this test we render a template of the first kind, which in turn renders subtemplates
        #    of the second kind if the required information is available. 
        d=defaults() 
        tp=d['paths']['static_report_templates'].joinpath('single_model','CompleteSingleModelReport.py')
        rel=render2(tp,'miniCable')
        target_dir_path=Path('.').joinpath('html')
        target_dir_path.mkdir(parents=True,exist_ok=True)
        targetFileName='Report.html'
        rel.write_pypandoc_html(target_dir_path.joinpath(targetFileName))

# vim:set ff=unix expandtab ts=4 sw=4:
import unittest
import yaml
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import shutil
from pathlib import Path
from concurrencytest import ConcurrentTestSuite, fork_for_tests
from bgc_md.IncompleteModel import IncompleteModel
from bgc_md.Model import Model, load_bibtex_entry, load_abstract, load_further_references, load_reviews, load_sections_and_titles, load_df, load_expressions_and_symbols, section_subdict, load_model_run_data, load_parameter_sets, load_initial_values, check_parameter_set_valid, check_parameter_sets_valid, check_parameter_set_complete, check_initial_values_set_valid, check_initial_values_complete, load_run_times, load_model_run_combinations, YamlException
from bgc_md.ModelList import ModelList
from bgc_md.reports import  defaults

from testinfrastructure.InDirTest import InDirTest
class TestModelList(InDirTest):
    def setUp(self):
        yaml_str = """\
        model:
            - environmental_paramters: 
                - T:
                    key: Temperature
                - f:
                    key: foliage

            - components:
                - b:
                    exprs: b = Matrix(3,1, [1, 0, 1])
                    key: input_vector
                - u:
                    exprs: u=T*f
                    key: scalar_func_phot
                - f_s:
                    exprs: "f_s = u*b"
                    key: state_vector_derivative
        """
        model_0 = IncompleteModel(yaml_str,"mod0")
        model_0.sections, model_0.section_titles, model_0.complete_dict = load_sections_and_titles(model_0.complete_dict)
        model_0.df = load_df(model_0.complete_dict, model_0.sections)
        model_0.syms_dict, model_0.exprs_dict, model_0.symbols_by_type = load_expressions_and_symbols(model_0.df) 
        model_0.set_component_keys()


        yaml_str = """\
        model:
            - environmental_paramters: 
                - a:
                - T:
                    key: Temperature
                - f:
                    key: roots
                    exprs: f=5*a 

            - components:
                - b:
                    exprs: b = Matrix(3,1, [1, 0, 1])
                    key: input_vector
                - u:
                    exprs: u=T*f
                    key: scalar_func_phot
                - f_s:
                    exprs: "f_s = u*b"
                    key: state_vector_derivative
        """
        model_1 = IncompleteModel(yaml_str,"mod1")
        model_1.sections, model_1.section_titles, model_1.complete_dict = load_sections_and_titles(model_1.complete_dict)
        model_1.df = load_df(model_1.complete_dict, model_1.sections)
        model_1.syms_dict, model_1.exprs_dict, model_1.symbols_by_type = load_expressions_and_symbols(model_1.df) 
        model_1.set_component_keys()
        
        
        self.ml=ModelList([model_0,model_1])

####################################################################################################
    def test_plot_model_key_dependencies_scatter_plot(self):
        ml=self.ml
        fig = plt.figure()
        ax=fig.add_subplot(1,2,1)
        ml.plot_model_key_dependencies_scatter_plot("scalar_func_phot",ax)
        ax=fig.add_subplot(1,2,2)
        ml.plot_model_key_dependencies_scatter_plot("state_vector_derivative",ax)
        fig.savefig("plot.pdf")
        plt.close(fig.number)
        
####################################################################################################
    def test_create_overview_table(self):
        # we create a target directory populated with only a few files and create a overview html from it
        d=defaults() 
        sp=d['paths']['tested_records']
        src_dir_name='localDataBase'
        src_dir_path=Path(src_dir_name)
        src_dir_path.mkdir()
        rec_list=[ rec  for rec in sp.glob('*.yaml')][0:1]
        
        for rec in rec_list:
            print(rec)
            src=(sp.joinpath(rec)).as_posix()
            target=(src_dir_name)
            shutil.copy(src,src_dir_name)
         
        ml=ModelList.from_dir_path(src_dir_path)
        target_dir_path=Path('.').joinpath('html')
        rel=ml.create_overview_table(target_dir_path)
        targetFileName='table.html'
        targetPath=target_dir_path.joinpath(targetFileName)
        rel.write_pandoc_html(targetPath)
        print(targetPath)
        self.assertTrue(targetPath.exists())

####################################################################################################
if __name__ == '__main__':
    suite=unittest.defaultTestLoader.discover(".",pattern=__file__)

    # Run same tests across 16 processes
    concurrent_suite = ConcurrentTestSuite(suite, fork_for_tests(16))
    runner = unittest.TextTestRunner()
    res=runner.run(concurrent_suite)
    # to let the buildbot fail we set the exit value !=0 if either a failure or error occurs
    if (len(res.errors)+len(res.failures))>0:
        sys.exit(1)

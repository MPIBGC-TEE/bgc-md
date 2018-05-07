#!/usr/bin/env python3
# vim:set ff=unix expandtab ts=4 sw=4:
import unittest
import sys
from concurrencytest import ConcurrentTestSuite, fork_for_tests
import yaml
from sympy import Symbol, Matrix, var, sin, cos, Matrix, lambdify, symbols, MatrixSymbol, diag, Eq, simplify
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from bgc_md.helpers import  retrieve_this_or_that
from bgc_md.yaml_creator_mod import example_yaml_string_list
from bgc_md.Model import Model, load_bibtex_entry, load_abstract, load_further_references, load_reviews, load_sections_and_titles, load_df, load_expressions_and_symbols, section_subdict, load_model_run_data, load_parameter_sets, load_initial_values, check_parameter_set_valid, check_parameter_sets_valid, check_parameter_set_complete, check_initial_values_set_valid, check_initial_values_complete, load_run_times, load_model_run_combinations, YamlException
from bgc_md.ModelList import ModelList
from bgc_md.bibtexc import BibtexEntry, DoiNotFoundException, online_entry
from bgc_md.SmoothModelRun import SmoothModelRun 
from bgc_md.SmoothReservoirModel import SmoothReservoirModel 
from testinfrastructure.InDirTest import InDirTest
from bgc_md.IncompleteModel import IncompleteModel

######### TestClass #############
class TestModel(InDirTest):

    def setUp(self):
        self.yaml_str_list = example_yaml_string_list() 


    # we would need to parse the yaml file first and test if the parsing method is correct
    # we test all subroutines separately
    @unittest.skip("Need to test the initalization of a model here.")
    def test_init(self):
        pass

#        for yaml_str in self.yaml_str_list:
#            complete_dict = yaml.load(yaml_str)
#            del complete_dict['model']
#
#            with self.assertRaises(Exception) as cm:
#                m = Model(complete_dict)
#            e = cm.exception
#            self.assertEqual(e.__str__(), "yaml file does not contain a model section")

    def test_jacobian(self):
        # note that the order of the state varibles in the yaml file is different
        # from the order in the state vector
        # We make sure that the latter is used.
        yaml_str="""\
        model:
            - state_variables:
                - C_f:
                - C_r: 
                - C_w:
            
            - components:
                - x: 
                    exprs: "x=Matrix(3,1,[C_f, C_w, C_r])"
                    key: state_vector
                - A:   
                    exprs: "A=diag(1,1,1)"
                    key: cyc_matrix
                - f_v: 
                    exprs: "f_v =  A*x"
                    key: state_vector_derivative
        """
        # __init__ replacement
        model=IncompleteModel(yaml_str)
        model.sections, model.section_titles, model.complete_dict = load_sections_and_titles(model.complete_dict)
        model.df = load_df(model.complete_dict, model.sections)
        model.syms_dict, model.exprs_dict, model.symbols_by_type = load_expressions_and_symbols(model.df) 
        model.set_component_keys()

        # assertions
        Jref=diag(1,1,1)
        Jres=model.jacobian()
        self.assertEqual(Jref,Jres)

    def test_different_symbol_notations(self):
        # -u without description or unit but with colon 
        # -k without description, without colon
        yaml_str="""\
        model-id: V0001
        model:
            - parameters:
                - k 
            - components:
                - u:   
                - b:   
                    exprs: "b=Matrix(3,1,[u, 2, 3])"
        """
        model = IncompleteModel(yaml_str)
        #model.bibtex_entry = load_bibtex_entry(self.complete_dict)
        #model.abstract = load_abstract(self.complete_dict, self.bibtex_entry)
        #model.further_references = load_further_references(self.complete_dict)
        #model.reviews, self.deeply_reviewed = load_reviews(self.complete_dict)
        model.sections, model.section_titles, model.complete_dict = load_sections_and_titles(model.complete_dict)
        model.df = load_df(model.complete_dict, model.sections)
        syms_dict, exprs_dict, symbols_by_type = load_expressions_and_symbols(model.df) 
        u = Symbol('u')
        k = Symbol('k')
        self.assertEqual(syms_dict, {'u': u, 'k': k})
        self.assertEqual(exprs_dict, {'b': Matrix(3,1,[u,2,3])})

    @unittest.skip
    # the model-id is no longer used
    def test_load_complete_dict_and_id(self):
        # test good case
        yaml_str = """\
            model-id: S0019
            model:
                - state_variables:
                    - X:
        """
        complete_dict = yaml.load(yaml_str)
        complete_dict, modelID = load_complete_dict_and_id(complete_dict)
        self.assertEqual(modelID, "S0019")
        
        # test empty model section
        yaml_str = """\
            model-id: S0019
            model:
        """
        complete_dict = yaml.load(yaml_str)
        with self.assertRaises(YamlException) as cm:
            complete_dict, modelID = load_complete_dict_and_id(complete_dict)
        e = cm.exception
        self.assertEqual(e.__str__()[:20], "yaml file does not contain a model section:"[:20])


    def test_load_bibtex_entry(self):
        # test bibtex over doi
        yaml_str = """\
                        doi: 10.1038/ngeo846
                        bibtex: "@article{Key_to_check,
                                     author={Li, Jianwei and Wang, Gangsheng and Allison, Steven D and Mayes, Melanie A and Luo, Yiqi},
                                     title={Soil carbon sensitivity to temperature and carbon use efficiency compared across microbial-ecosystem models of varying complexity},
                                     journal={Biogeochemistry},
                                     volume={119},
                                     number={1-3},
                                     pages={67--84},
                                     year={2014},
                                     publisher={Springer}
                                }"
                    """
        complete_dict = yaml.load(yaml_str)
        bibtex_entry = load_bibtex_entry(complete_dict)
        self.assertEqual(bibtex_entry.key, 'Key_to_check')

    def test_load_bibtex_entry_from_doi(self):
        # test loading from doi
        yaml_str = """\
                        doi: 10.1038/ngeo846
                    """
        complete_dict = yaml.load(yaml_str)
        bibtex_entry = load_bibtex_entry(complete_dict)
        self.assertEqual(bibtex_entry.key, 'Allison2010NatureGeoscience')

    def test_load_bibtex_entry_from_invalid_doi(self):
        # test invalid doi
        yaml_str = """\
                        doi: xyzbgcv12y.122
                    """
        complete_dict = yaml.load(yaml_str)
        bibtex_entry = load_bibtex_entry(complete_dict)
        self.assertEqual(bibtex_entry,None)


    def test_load_bibtex_entry_no_doi_no_yaml(self):
        # test missing doi and bibtex
        yaml_str = """\
                    modelID : S0019
                   """
        complete_dict = yaml.load(yaml_str)
        self.assertEqual(load_bibtex_entry(complete_dict), None)


    def test_load_abstract(self):
        # test yaml abstract over bibtex abstract and correction of special terms
        yaml_str = """\
            abstract: "This abstract will be taken. CO2 will be corrected."
            bibtex: "@article{Li2014Biogeochemistry,
                         author={Li, Jianwei and Wang, Gangsheng and Allison, Steven D and Mayes, Melanie A and Luo, Yiqi},
                         title={Soil carbon sensitivity to temperature and carbon use efficiency compared across microbial-ecosystem models of varying complexity},
                         journal={Biogeochemistry},
                         volume={119},
                         number={1-3},
                         pages={67--84},
                         year={2014},
                         publisher={Springer},
                         abstract={This abstract will be ignored.}
                        }"
           
        """
        complete_dict = yaml.load(yaml_str)
        bibtex_entry = load_bibtex_entry(complete_dict)
        abstract = load_abstract(complete_dict, bibtex_entry)
        self.assertEqual(abstract, "This abstract will be taken. CO$_2$ will be corrected.")

        # test no abstract
        yaml_str = """\
            modelID: S0019
        """
        complete_dict = yaml.load(yaml_str)
        bibtex_entry = load_bibtex_entry(complete_dict)
        abstract = load_abstract(complete_dict, bibtex_entry)
        self.assertEqual(abstract, None)


    def test_load_further_references(self):
        # test good case
        yaml_str = """\
        further_references:
            - doi: 10.1038/ngeo846
              desc: "Original paper, just by doi"
            - bibtex: "@article{Li2014Biogeochemistry,
                         author={Li, Jianwei and Wang, Gangsheng and Allison, Steven D and Mayes, Melanie A and Luo, Yiqi},
                         title={Soil carbon sensitivity to temperature and carbon use efficiency compared across microbial-ecosystem models of varying complexity},
                         journal={Biogeochemistry},
                         volume={119},
                         number={1-3},
                         pages={67--84},
                         year={2014},
                         publisher={Springer}
                        }"
              desc: "Another paper"
        """
        complete_dict = yaml.load(yaml_str)
        further_references = load_further_references(complete_dict)
        self.assertEqual(further_references[0]['bibtex_entry'].key, 'Allison2010NatureGeoscience')
        self.assertEqual(further_references[1]['bibtex_entry'].key, 'Li2014Biogeochemistry')

        # test missing doi and bibtex
        yaml_str = """\
        further_references:
            - doi: 
              desc: "Original paper, just by doi"
        """
        complete_dict = yaml.load(yaml_str)
        with self.assertRaises(YamlException) as cm:
            further_references = load_further_references(complete_dict)
        e = cm.exception
        self.assertEqual(e.__str__(), "Missing 'doi' and 'bibtex' in further_references.")

        # test invalid doi
        yaml_str = """\
        further_references:
            - doi: 34.xxcvj8Fs0
              desc: "Invalid doi"
        """
        complete_dict = yaml.load(yaml_str)
        with self.assertRaises(YamlException) as cm:
            further_references = load_further_references(complete_dict)
        e = cm.exception
        ref_str = "Invalid doi in further_references.\nThe doi 34.xxcvj8Fs0 could not be resolved."
        self.assertEqual(e.__str__(), ref_str)


    def test_load_reviews(self):
        # test good case
        yaml_str = """\
        reviews:
            - reviewer: Holger Metzler
              orcid: 0000-0002-8239-1601
              date: 24/03/2016
              desc: "I just looked at the report and saw a typo. Changed \\alfa to \\alpha."
              type: shallow
            - reviewer: Markus Müller
              date: 25/03/2016
              desc: "I checked all the equations by reading the paper."
              type: deep
        """
        complete_dict = yaml.load(yaml_str)
        reviews, deeply_reviewed = load_reviews(complete_dict)
        self.assertEqual(reviews[0]['type'], 'shallow')
        self.assertEqual(deeply_reviewed, True)

        # test missing obligatory key: type
        yaml_str = """\
        reviews:
            - reviewer: Holger Metzler
              orcid: 0000-0002-8239-1601
              date: 24/03/2016
              desc: "I just looked at the report and saw a typo. Changed \\alfa to \\alpha."
            - reviewer: Markus Müller
              date: 25/03/2016
              desc: "I checked all the equations by reading the paper."
              type: deep
        """
        complete_dict = yaml.load(yaml_str)
        with self.assertRaises(YamlException) as cm:
            reviews, deeply_reviewed= load_reviews(complete_dict)
        e = cm.exception
        self.assertEqual(e.__str__(), "Missing 'type' in review list.")


    def test_load_sections_and_titles(self):
        # test normal usage
        yaml_str = """\
        model:
            - state_variables:
                - A:
                - B:
            
            - additional_variables[Alternative Title]:
                - c
                - d:
        """
        complete_dict = yaml.load(yaml_str)
        sections, section_titles, complete_dict = load_sections_and_titles(complete_dict)

        self.assertEqual(sections, ["state_variables", "additional_variables"])
        self.assertEqual(section_titles, {'state_variables': 'State Variables', 'additional_variables': 'Alternative Title'})
        self.assertTrue('additional_variables' in complete_dict['model'][1].keys())

        # test double section name
        yaml_str = """\
        model:
            - state_variables:
                - A:
                - B:
            
            - additional_variables[Alternative Title]:
                - c
                - d:

            - additional_variables[different title]:
                - e:
        """
        complete_dict = yaml.load(yaml_str)
        with self.assertRaises(YamlException) as cm:
            sections, section_titles = load_sections_and_titles(complete_dict)
        e = cm.exception

        self.assertEqual(e.__str__(), "The model contains more than one subsection called 'additional_variables'.")


    def test_load_df(self):
        # test good case
        yaml_str = """\
        model:
            - state_variables:
                - X:
                    desc: X pool
                - Y:
                    desc: Y pool

            - additional_variables:
                - p:
                    desc: "product of $X$ and $Y$"
                    exprs: "p = X * Y"
                    type: variable

            - decomposition_rates:
                - k:
                    desc: "decomposition rate of pool $X$"
                    unit: "time^{-1}"
                    type: parameter
        """
        complete_dict = yaml.load(yaml_str)
        sections, section_titles, complete_dict = load_sections_and_titles(complete_dict)
        df = load_df(complete_dict, sections)
        self.assertEqual(df.list_of_rows, [['name', 'category', 'desc', 'exprs', 'type', 'unit'],
                                          ['X', 'state_variables', 'X pool', None, None, None],
                                          ['Y', 'state_variables', 'Y pool', None, None, None],
                                          ['p', 'additional_variables', 'product of $X$ and $Y$', 'p = X * Y', 'variable', None],
                                          ['k', 'decomposition_rates', 'decomposition rate of pool $X$', None, 'parameter', 'time^{-1}']])
    
        # test double definition of variable
        yaml_str = """\
        model:
            - state_variables:
                - X:
                    desc: X pool
                - Y:
                    desc: Y pool

            - additional_variables:
                - p:
                    desc: "product of $X$ and $Y$"
                    exprs: "p = X * Y"
                    type: variable

            - decomposition_rates:
                - k:
                    desc: "decomposition rate of pool $X$"
                    unit: "time^{-1}"
                    type: parameter
                - X:
        """
        complete_dict = yaml.load(yaml_str)
        sections, section_titles, complete_dict = load_sections_and_titles(complete_dict)
        with self.assertRaises(YamlException) as cm:
            df = load_df(complete_dict, sections)
        e = cm.exception
        self.assertEqual(e.__str__(), "Variable 'X' defined more than once.")

    
    def test_expressions_and_symbols(self):
        yaml_str = """\
        model:
            - state_variables:
                - X:
                    desc: X pool
                - Y:
                    desc: Y pool

            - additional_variables:
                - p:
                    desc: "product of $X$ and $Y$"
                    exprs: "p = X * Y"
                    type: variable

            - decomposition_rates:
                - k:
                    desc: "decomposition rate of pool $X$"
                    unit: "time^{-1}"
                    type: parameter
    
            - components:
                - A:
                    desc: decomposition operator
                    exprs: "A = diag(k*X, p*Y)"
        """
        complete_dict = yaml.load(yaml_str)
        sections, section_titles, complete_dict = load_sections_and_titles(complete_dict)
        df = load_df(complete_dict, sections)
        syms_dict, exprs_dict, symbols_by_type = load_expressions_and_symbols(df)

        X, Y, k = symbols('X Y k')
        p = X * Y
        A = diag(k*X,p*Y)
        self.assertEqual(syms_dict, {'X': X, 'Y': Y, 'k': k})
        self.assertEqual(exprs_dict, {'p': X*Y, 'A': diag(k*X, X*Y**2)})
        self.assertFalse(symbols_by_type['k'].is_Matrix)
        self.assertTrue(symbols_by_type['A'].is_Matrix)


    def test_section_subdict(self):
        yaml_str = """\
        model:
            - state_variables:
                - A:
                    desc: first state variable
                - B:
            - additional_variables[Alternative Title]:
                - c
                - d:
        """
        complete_dict = yaml.load(yaml_str)

        # test normal usage
        subdict = section_subdict(complete_dict, 'state_variables')
        self.assertEqual(subdict['state_variables'], [{'A': {'desc': 'first state variable'}}, {'B': None}])

        # test wrong target key: correct key is 'additional_variables[Alternative Title]'
        # since load_sections_and_titles was not yet run
        with self.assertRaises(YamlException) as cm:
            subdict = section_subdict(complete_dict, 'additional_variables')
        e = cm.exception
        self.assertEqual(e.__str__(), "Subsection additional_variables not found.")
        
        # test changed target_key after run of load_sections_and_titles
        sections, section_titles, complete_dict = load_sections_and_titles(complete_dict)
        subdict = section_subdict(complete_dict, 'additional_variables')
        self.assertEqual(subdict['additional_variables'], ['c', {'d': None}])
            
    
    def test_reservoir_model(self):
        yaml_str = """\
            model:
                - state_variables: [C_0, C_1]
                - parameters: [k_01, k_10, k_0o, k_1o]
                - variables:
                    - t:
                        key: time_symbol
                    - K_0:
                        exprs: "K_0 = k_01*C_1**2+k_0o*C_0**2"
                    - K_1:
                        exprs: "K_1 = k_10*C_0+k_1o*C_1**2"
                - input_components: 
                    - u_0:
                        exprs: "u_0 = 2 + sin(t)" 
                    - u_1:
                        exprs: "u_1 = 2 + cos(t)"
                - components:
                    - C:
                        exprs: "C = Matrix([C_0, C_1])"
                        key: state_vector
                    - u:
                        exprs: "u = Matrix([u_0, u_1])"
                        key: input_vector
                    - T:
                        exprs: "T = Matrix([[-1, k_10*C_0/K_1],
                                           [k_01*C_1**2/K_0, -1]])"
                        key: trans_op
                    - N:
                        exprs: "N = diag(K_0, K_1)"
                        key: decomp_op_nonlin
                    - f_s:
                        exprs: "f_s = u + T * N * C"
                        key: state_vector_derivative                        
                    
            model_run_data:
                parameter_sets:
                    - Set1:
                        values:       
                            k_01: 0.01
                            k_10: 0.01
                            k_0o: 0.5
                            k_1o: 0.5
                    - Set2:
                        values:       
                            k_01: 0.02
                            k_10: 0.02
                            k_0o: 1.0
                            k_1o: 1.0

                initial_values:
                    - IV1:
                        values:
                            C_0: 1
                            C_1: 2
                    - IV2:
                        values:
                            C_0: 3
                            C_1: 4

                run_times:
                    - RT1:
                        start: 0
                        end: 10
                        step_size: 0.1
                    - RT2:
                        start: 5
                        end: 12
                        step_size: 1

                possible_combinations:
                    - [Set1, IV1, RT1]
                    - [Set1, IV2, RT1]
                    - [Set2, IV1, RT2]
        """
        model = IncompleteModel(yaml_str)
        model.sections, model.section_titles, model.complete_dict = load_sections_and_titles(model.complete_dict)
        model.df = load_df(model.complete_dict, model.sections)
        model.syms_dict, model.exprs_dict, model.symbols_by_type = load_expressions_and_symbols(model.df) 
        model.set_component_keys()

        model.model_run_data = load_model_run_data(model.complete_dict)
        model.parameter_sets = load_parameter_sets(model.model_run_data)
        check_parameter_sets_valid(model.parameter_sets, model.symbols_by_type)
        model.initial_values = load_initial_values(model.model_run_data)
        model.run_times = load_run_times(model.model_run_data)

        model.model_run_combinations, msg = load_model_run_combinations(model.model_run_data, model.parameter_sets, model.initial_values, 
                                                 model.run_times, model.state_vector, model.time_symbol, model.state_vector_derivative)
        
        ##create prerequisites model 
        ##first create an example model
        t, k_01, k_10,k_0o, k_1o = symbols("t, k_01,k_10,k_0o,k_1o")
        C_0, C_1 = symbols("C_0,C_1")

        state_variables=[C_0,C_1] # order is important
        inputs={
            0: sin(t)+2,#input to pool 0
            1: cos(t)+2 #input to pool 1
            }
        outputs={
            0: k_0o*C_0**3,#output from pool 0
            1: k_1o*C_1**3 #output from pool 0
            }
        internal_fluxes={
            (0,1): k_01*C_0*C_1**2, #flux from pool0  to pool 1
            (1,0): k_10*C_0*C_1 #flux from pool1  to pool 0
            }
        time_symbol=t
        m = SmoothReservoirModel(state_variables,time_symbol,inputs,outputs,internal_fluxes)
        
        params_0 = {
            k_01: 0.01,
            k_10: 0.01,
            k_0o: 0.5,
            k_1o: 0.5
            }
        times_0 = np.arange(0, 10.1, 0.1)   # time grid forward
        start_values_0 = np.array([1,2])

        params_1 = {
            k_01: 0.02,
            k_10: 0.02,
            k_0o: 1.0,
            k_1o: 1.0
            }
        times_1 = np.arange(5, 13, 1)   # time grid forward
        start_values_1 = np.array([3,4])

        ref_runs = [
                SmoothModelRun(m, parameter_set= params_0, start_values= start_values_0, times= times_0),
                SmoothModelRun(m, parameter_set= params_0, start_values= start_values_1, times= times_0),
                SmoothModelRun(m, parameter_set= params_1, start_values= start_values_0, times= times_1)
        ]
        
        res_mod = model.reservoir_model
        
        # check if reservoir model uses really the right hand side of the model for its calculations
        self.assertEqual(res_mod.F, simplify(model.rhs))
        self.assertEqual(len(model.model_runs), len(ref_runs))

        for i in range(len(ref_runs)):
            # check created model run
            ref_mr = ref_runs[i]
            mr = model.model_runs[i]
            self.assertEqual(mr.parameter_set, ref_mr.parameter_set)        
            self.assertTrue(np.allclose(mr.start_values, ref_mr.start_values))
            self.assertTrue(all(mr.times==ref_mr.times))

            # check if correct model belongs to model runs
            self.assertEqual(mr.model.state_variables, m.state_variables)
            self.assertEqual(mr.model.input_fluxes, m.input_fluxes)
            self.assertEqual(mr.model.output_fluxes, m.output_fluxes)
            self.assertEqual(mr.model.internal_fluxes, m.internal_fluxes)
            self.assertEqual(mr.model.time_symbol, m.time_symbol)

            

    def test_check_parameter_set_complete(self):
        yaml_str = """\
            model:
                - state_variables: [C_0, C_1]
                - parameters: [k_01, k_10, k_0o, k_1o]
                - variables:
                    - t:
                        key: time_symbol
                    - K_0:
                        exprs: "K_0 = k_01*C_1**2+k_0o*C_0**2"
                    - K_1:
                        exprs: "K_1 = k_10*C_0+k_1o*C_1**2"
                - input_components: 
                    - u_0:
                        exprs: "u_0 = 2 + sin(t)" 
                    - u_1:
                        exprs: "u_1 = 2 + cos(t)"
                - components:
                    - C:
                        exprs: "C = Matrix([C_0, C_1])"
                        key: state_vector
                    - u:
                        exprs: "u = Matrix([u_0, u_1])"
                        key: input_vector
                    - T:
                        exprs: "T = Matrix([[-1, k_10*C_0/K_1],
                                           [k_01*C_1**2/K_0, -1]])"
                        key: trans_op
                    - N:
                        exprs: "N = diag(K_0, K_1)"
                        key: decomp_op_nonlin
                    - f_s:
                        exprs: "f_s = u + T * N * C"
                        key: state_vector_derivative                        
                    
            model_run_data:
                parameter_sets:
                    - Set1:
                        values:       
                            k_01: 0.01
                            k_10: 0.01
                            k_0o: 0.5
                            k_1o: 0.5
                    - Set2:
                        values:       
                            k_01: 0.02
                            k_10: 0.02
                            k_0o: 1.0
        """
        model = IncompleteModel(yaml_str)
        model.sections, model.section_titles, model.complete_dict = load_sections_and_titles(model.complete_dict)
        model.df = load_df(model.complete_dict, model.sections)
        model.syms_dict, model.exprs_dict, model.symbols_by_type = load_expressions_and_symbols(model.df) 
        model.set_component_keys()

        model.model_run_data = load_model_run_data(model.complete_dict)
        model.parameter_sets = load_parameter_sets(model.model_run_data)

        par_set = model.parameter_sets[0]
        complete = check_parameter_set_complete(par_set, model.state_vector, model.time_symbol, model.state_vector_derivative)
        self.assertTrue(complete)

        par_set = model.parameter_sets[1]
        complete = check_parameter_set_complete(par_set, model.state_vector, model.time_symbol, model.state_vector_derivative)
        self.assertFalse(complete)
            

    def test_check_initial_values_complete(self):
        yaml_str = """\
            model:
                - state_variables: [C_0, C_1]
                - components:
                    - C:
                        exprs: "C = Matrix([C_0, C_1])"
                        key: state_vector
                    
            model_run_data:
                initial_values:
                    - IV1:
                        values:
                            C_0: 1
                            C_1: 2
                    - IV2:
                        values:
                            C_0: 3

        """
        model = IncompleteModel(yaml_str)
        model.sections, model.section_titles, model.complete_dict = load_sections_and_titles(model.complete_dict)
        model.df = load_df(model.complete_dict, model.sections)
        model.syms_dict, model.exprs_dict, model.symbols_by_type = load_expressions_and_symbols(model.df) 
        model.set_component_keys()

        model.model_run_data = load_model_run_data(model.complete_dict)
        model.initial_values = load_initial_values(model.model_run_data)

        iv = model.initial_values[0]
        complete = check_initial_values_complete(iv, model.state_vector)
        self.assertTrue(complete)

        iv = model.initial_values[1]
        complete = check_initial_values_complete(iv, model.state_vector)
        self.assertFalse(complete)
            

    def test_load_run_times(self):
        # test normal case
        yaml_str = """\
            model:
            model_run_data:
                run_times:
                    - RT1:
                        start: 0
                        end: 10
                        step_size: 0.1
                    - RT2:
                        start: 10
                        end: 100
                        step_size: 1
        """
        complete_dict = yaml.load(yaml_str)
        model_run_data = load_model_run_data(complete_dict)
        run_times = load_run_times(model_run_data)

        ref = [{'name': 'RT1', 'start':  0, 'end':  10, 'step_size': 0.1},
               {'name': 'RT2', 'start': 10, 'end': 100, 'step_size': 1.0}]
        self.assertEqual(run_times, ref)

        # test missing start, end or step_size
        yaml_str = """\
            model:
            model_run_data:
                run_times:
                    - RT1:
                        start: 0
                        end: 10
                        step_size: 0.1
                    - RT2:
                        end: 100
                        step_size: 1
        """
        complete_dict = yaml.load(yaml_str)
        model_run_data = load_model_run_data(complete_dict)
        with self.assertRaises(YamlException) as cm:
            run_times = load_run_times(model_run_data)
        e = cm.exception
        self.assertEqual(e.__str__(), "'run_times' data set 'RT2' does not contain 'start'")

        # test start > end
        yaml_str = """\
            model:
            model_run_data:
                run_times:
                    - RT1:
                        start: 100
                        end: 10
                        step_size: 0.1
        """
        complete_dict = yaml.load(yaml_str)
        model_run_data = load_model_run_data(complete_dict)
        with self.assertRaises(YamlException) as cm:
            run_times = load_run_times(model_run_data)
        e = cm.exception
        self.assertEqual(e.__str__(), "'run_times' data set 'RT1' has 'start' > 'end'")


    def test_load_model_run_combinations(self):
        yaml_str = """\
            model:
                - state_variables: [C_0, C_1]
                - parameters: [k_01, k_10, k_0o, k_1o]
                - variables:
                    - t:
                        key: time_symbol
                    - K_0:
                        exprs: "K_0 = k_01*C_1**2+k_0o*C_0**2"
                    - K_1:
                        exprs: "K_1 = k_10*C_0+k_1o*C_1**2"
                - input_components: 
                    - u_0:
                        exprs: "u_0 = 2 + sin(t)" 
                    - u_1:
                        exprs: "u_1 = 2 + cos(t)"
                - components:
                    - C:
                        exprs: "C = Matrix([C_0, C_1])"
                        key: state_vector
                    - u:
                        exprs: "u = Matrix([u_0, u_1])"
                        key: input_vector
                    - T:
                        exprs: "T = Matrix([[-1, k_10*C_0/K_1],
                                           [k_01*C_1**2/K_0, -1]])"
                        key: trans_op
                    - N:
                        exprs: "N = diag(K_0, K_1)"
                        key: decomp_op_nonlin
                    - f_s:
                        exprs: "f_s = u + T * N * C"
                        key: state_vector_derivative                        
                    
            model_run_data:
                parameter_sets:
                    - Set1:
                        values:       
                            k_01: 0.01
                            k_10: 0.01
                            k_0o: 0.5
                            k_1o: 0.5
                    - Set2:
                        values:       
                            k_01: 0.02
                            k_10: 0.02
                            k_0o: 1.0
                            k_1o: 1.0

                initial_values:
                    - IV1:
                        values:
                            C_0: 1
                            C_1: 2
                    - IV2:
                        values:
                            C_0: 3
                
                run_times:
                    - RT1:
                        start: 0
                        end: 10
                        step_size: 0.1
                    - RT2:
                        start: 5
                        end: 12
                        step_size: 1

                possible_combinations:
                    - [Set1, IV1, RT1]
                    - [Set1, IV2, RT1]
                    - [Set2, IV1, RT2]
        """

        model = IncompleteModel(yaml_str)
        model.sections, model.section_titles, model.complete_dict = load_sections_and_titles(model.complete_dict)
        model.df = load_df(model.complete_dict, model.sections)
        model.syms_dict, model.exprs_dict, model.symbols_by_type = load_expressions_and_symbols(model.df) 
        model.set_component_keys()

        model.model_run_data = load_model_run_data(model.complete_dict)
        model.parameter_sets = load_parameter_sets(model.model_run_data)
        model.initial_values = load_initial_values(model.model_run_data)
        model.run_times = load_run_times(model.model_run_data)

        
        poss_combs, msg = load_model_run_combinations(model.model_run_data, model.parameter_sets, model.initial_values, 
                                                 model.run_times, model.state_vector, model.time_symbol, model.state_vector_derivative)

        self.assertEqual(len(poss_combs), 2)
        self.assertEqual(poss_combs[0]['par_set']['table_head'], 'Set1')
#        self.assertEqual(poss_combs[1]['IV']['table_head'], 'IV2')
        self.assertEqual(poss_combs[1]['run_time']['step_size'], 1)
        


    def test_load_model_run_data(self):
        yaml_str = """\
            model:
            model_run_data:
                parameter_sets:
                    - Set1:
                        values:       
                            k_01: 0.01
                            k_10: 0.01
                            k_0o: 0.5
                            k_1o: 0.5
                    - Set2:
                        values:       
                            k_01: 0.02
                            k_10: 0.02
                            k_0o: 1.0
                            k_1o: 1.0

                initial_values:
                    - IV1:
                        values:
                            C_0: 1
                            C_1: 2
                    - IV2:
                        values:
                            C_0: 3
                            C_1: 3

                run_times:
                    - RT1:
                        start: 0
                        end: 10
                        step_size: 0.1

                possible_combinations:
                    - [Set1, IV1, RT1]
                    - [Set1, IV2, RT1]
                    - [Set2, IV1, RT1]
        """
        ref_dict ={"parameter_sets":[
                    {"Set1":{
                            "values":{       
                                "k_01": 0.01,
                                "k_10": 0.01,
                                "k_0o": 0.5,
                                "k_1o": 0.5
                                }
                            }
                    },
                    {"Set2":{
                            "values":{       
                                "k_01": 0.02,
                                "k_10": 0.02,
                                "k_0o": 1.0,
                                "k_1o": 1.0
                                }
                            }
                    }],
                    "initial_values":[
                        {"IV1":{
                            'values': {
                                "C_0": 1,
                                "C_1": 2
                                }
                            }
                        },
                        {"IV2":{
                            'values': {
                                "C_0": 3,
                                "C_1": 3
                                }
                            }
                        }
                    ],
                    "run_times":[{
                        "RT1":{
                            "start": 0,
                            "end": 10,
                            "step_size": 0.1
                            }
                    }],
                    "possible_combinations":[
                        ["Set1", "IV1", "RT1"],
                        ["Set1", "IV2", "RT1"],
                        ["Set2", "IV1", "RT1"]
                     ]
                  }
        cd=yaml.load(yaml_str)
        res=load_model_run_data(cd)
        self.maxDiff=None
        self.assertEqual(ref_dict,res)


    # contains tests for load_parameter_sets and load_initial_values
    def test_load_parameter_sets_and_load_initial_values(self):
        # test good case
        yaml_str = """\
            model:
            model_run_data:
                parameter_sets:
                    - Set1:
                        values:       
                            k_01: 0.01
                            k_10: 0.01
                            k_0o: 0.5
                            k_1o: 0.5
                        desc: original data
                    - Set2:
                        values: {k_01: 0.02, k_10: 0.02, k_0o: 1.0, k_1o: 1.0}
                        desc: data from another paper
                        doi: 10.1038/ngeo846
                    - "Another set with a long name":
                        values:       
                            k_01: 0.02
                        desc: incomplete_set
                        bibtex: "@article{Li2014Biogeochemistry,
                                     author={Li, Jianwei and Wang, Gangsheng and Allison, Steven D and Mayes, Melanie A and Luo, Yiqi},
                                     title={Soil carbon sensitivity to temperature and carbon use efficiency compared across microbial-ecosystem models of varying complexity},
                                     journal={Biogeochemistry},
                                     volume={119},
                                     number={1-3},
                                     pages={67--84},
                                     year={2014},
                                     publisher={Springer}
                                    }"
                initial_values:
                    - "nice initial values":
                        values: {X: 10}
        """
        ps1 = {"table_head": "Set1",
               "values":{       
                                "k_01": 0.01,
                                "k_10": 0.01,
                                "k_0o": 0.5,
                                "k_1o": 0.5
                                },
               "desc": "original data",
               "bibtex_entry": None 
              }
        ps2 = {"table_head": "Set2",
               "values":{       
                                "k_01": 0.02,
                                "k_10": 0.02,
                                "k_0o": 1.0,
                                "k_1o": 1.0
                                },
               "desc": "data from another paper",
               "bibtex_entry": BibtexEntry.from_doi(doi="10.1038/ngeo846")
              }

        complete_dict = yaml.load(yaml_str)
        model_run_data = load_model_run_data(complete_dict)
        parameter_sets = load_parameter_sets(model_run_data)
        initial_values = load_initial_values(model_run_data)

        self.assertEqual(parameter_sets[0], ps1)
        self.assertEqual(parameter_sets[1], ps2)
        self.assertEqual(parameter_sets[2]['bibtex_entry'].key, "Li2014Biogeochemistry")
        self.assertEqual(initial_values[0]['table_head'], 'nice initial values')
        self.assertEqual(initial_values[0]['values']['X'], 10)

        # test missing space after colon
        yaml_str = """\
            model:
            model_run_data:
                parameter_sets:
                    - Set1:
                        values:       
                            k_01:0.01
        """
        complete_dict = yaml.load(yaml_str)
        model_run_data = load_model_run_data(complete_dict)
        with self.assertRaises(YamlException) as cm:
            parameter_sets = load_parameter_sets(model_run_data)
        e = cm.exception
        self.assertEqual(e.__str__(), "Could not load parameter sets.\nData set 'Set1' invalid, probably forgotten space after colon.")

        # test for not having 'values' in the dictionary
        yaml_str = """\
            model:
            model_run_data:
                parameter_sets:
                    - Set1:               
                        desc: missing values
        """
        complete_dict = yaml.load(yaml_str)
        model_run_data = load_model_run_data(complete_dict)
        with self.assertRaises(YamlException) as cm:
            parameter_sets = load_parameter_sets(model_run_data)
        e = cm.exception
        self.assertEqual(e.__str__(), "Could not load parameter sets.\nNo values given in data set 'Set1'.")


    #fixme: no state variables as parameters!
    def test_check_parameter_set_and_initial_value_set_valid(self):
        # test good case
        yaml_str = """\
        model:
            - state_variables:
                - X:
            - parameters:
                - k:
            - components:
                - A:
                    exprs: "A = X * k"
        model_run_data:
            parameter_sets:
                - Set1:
                    values:
                        k: 0.5
            initial_values:
                - Set1:
                    values:
                        X: 10
        """
        complete_dict = yaml.load(yaml_str)
        sections, titles, complete_dict = load_sections_and_titles(complete_dict)
        df = load_df(complete_dict, sections)
        sd, ed, syms_by_type = load_expressions_and_symbols(df)
        model_run_data = load_model_run_data(complete_dict)
        parameter_sets = load_parameter_sets(model_run_data)
        self.assertTrue(check_parameter_set_valid(parameter_sets[0], syms_by_type))

        initial_values = load_initial_values(model_run_data)
        self.assertTrue(check_initial_values_set_valid(initial_values[0], syms_by_type, ['X']))

        # test unknown parameter
        yaml_str = """\
        model:
            - state_variables:
                - X:
            - parameters:
                - k:
            - components:
                - A:
                    exprs: "A = X * k"
        model_run_data:
            parameter_sets:
                - Set1:
                    values:
                        a: 0.5
        """
        complete_dict = yaml.load(yaml_str)
        sections, titles, complete_dict = load_sections_and_titles(complete_dict)
        df = load_df(complete_dict, sections)
        sd, ed, syms_by_type = load_expressions_and_symbols(df)
        model_run_data = load_model_run_data(complete_dict)
        parameter_sets = load_parameter_sets(model_run_data)
        with self.assertRaises(YamlException) as cm:
            check_parameter_set_valid(parameter_sets[0], syms_by_type)
        e = cm.exception
        self.assertEqual(e.__str__(), "Invalid parameter set: Set1\nCould not substitute 'a'\nname 'a' is not defined")

        # test unknown state_variable in inital values
        yaml_str = """\
        model:
            - state_variables:
                - X:
            - parameters:
                - k:
            - components:
                - A:
                    exprs: "A = X * k"
        model_run_data:
            parameter_sets:
                - Set1:
                    values:
                        k: 0.5
            initial_values:
                - IV1:
                    values: {Y: 2}
        """
        complete_dict = yaml.load(yaml_str)
        sections, titles, complete_dict = load_sections_and_titles(complete_dict)
        df = load_df(complete_dict, sections)
        sd, ed, syms_by_type = load_expressions_and_symbols(df)
        model_run_data = load_model_run_data(complete_dict)
        initial_values = load_initial_values(model_run_data)
        with self.assertRaises(YamlException) as cm:
            check_initial_values_set_valid(initial_values[0], syms_by_type, ['X'])
        e = cm.exception
        self.assertEqual(e.__str__(), "Invalid initial values set: IV1\nCould not substitute 'Y'\nname 'Y' is not defined")


    def test_meta_data(self):
        yaml_str="""\
              version: 
              model-id: V0001
              entryAuthor: "Verónika Ceballos-Núñez"
              entryAuthorOrcid: 0000-0002-0046-1160
              entryCreationDate: _ecd_
              lastModification: _lm_
              modApproach: process based
              doi:
              bibtex: "@article{Hilbert1991Annals_of_Botany,
                          Author = {HILBERT, DAVID W. and REYNOLDS, JAMES F.},
                          Journal = {Annals of Botany},
                          Number = {5},
                          Pages = {417-425},
                          Title = {A Model Allocating Growth Among Leaf Proteins, Shoot Structure, and Root Biomass to Produce Balanced Activity},
                          Url = {http://aob.oxfordjournals.org/content/68/5/417.abstract},
                          Volume = {68},
                          Year = {1991}
                      }"
             """

        m=IncompleteModel(yaml_str)
        m.bibtex_entry = load_bibtex_entry(m.complete_dict)
        self.assertEqual(m.entryAuthor, "Verónika Ceballos-Núñez")
        self.assertEqual(m.version, "1")

        self.assertEqual(m.entry_creation_date, "_ecd_")
        self.assertEqual(m.last_modification_date, "_lm_")
        self.assertEqual(m.entryAuthor_orc_id, "0000-0002-0046-1160")
        self.assertEqual(m.approach, "process based")
      

    def test_add_data_columns_to_data_frame(self):
        yaml_str = """\
        model:
            - state_variables:
                - X:
            - parameters:
                - i:
                    desc: imaginary unit
                - k:
            - components:
                - x:
                    exprs: "x = Matrix(1,1,[X])"
                    key: "state_vector"
                - A:
                    exprs: "A = X * k"
        model_run_data:
            parameter_sets:
                - Set1:
                    values:
                        k: 0.5
            initial_values:
                - IV1:
                    values: {X: 23}
        """
        model = IncompleteModel(yaml_str)
        model.sections, model.section_titles, model.complete_dict = load_sections_and_titles(model.complete_dict)
        model.df = load_df(model.complete_dict, model.sections)

        df = model.section_vars('parameters')
        model.model_run_data = load_model_run_data(model.complete_dict)
        model.parameter_sets = load_parameter_sets(model.model_run_data)
        df = model.add_data_columns_to_data_frame(df, model.parameter_sets)
        self.assertEqual(df[1, 'Set1'], 0.5)
    
        model.initial_values = load_initial_values(model.model_run_data)
        df = model.section_vars('state_variables')
        df = model.add_data_columns_to_data_frame(df, model.initial_values)
        self.assertEqual(df[0, 'IV1'], 23)


    def test_set_component_keys(self):
        # test normal usage
        yaml_str = """\
        model:
            - state_variables: [C_1, C_2, C_3]
            - decomposition_parameters: [k_1, k_2, k_3]
            - transit_parameters: [t_12, t_13, t_21, t_23, t_31, t_32]
            - input_components: [u_1, u_2, u_3]
            - components:
                - C:
                    exprs: "C = Matrix(3,1, [C_1,C_2,C_3])"
                    key: state_vector
                - u:
                    exprs: u = Matrix(3,1, [u_1, u_2, u_3])
                    key: input_vector
                - xi:
                    key: env_eff_mult
                - T:
                    exprs: "T = Matrix([[  -1, t_12, t_13],
                                        [t_21,   -1, t_23],
                                        [t_31, t_32,   -1]])"
                    key: trans_op
                - N:
                    exprs: "N = diag(k_1, k_2, k_3)"
                    # key here not given
                - f_s:
                    exprs: "f_s = u + xi * T * N * C"
                    key: state_vector_derivative
        """
        model = IncompleteModel(yaml_str)
        model.sections, model.section_titles, model.complete_dict = load_sections_and_titles(model.complete_dict)
        model.df = load_df(model.complete_dict, model.sections)
        model.syms_dict, model.exprs_dict, model.symbols_by_type = load_expressions_and_symbols(model.df) 
        
        model.set_component_keys()
        C_1, C_2, C_3, k_1, k_2, k_3, t_12, t_13, t_21, t_23, t_31, t_32, u_1, u_2, u_3, xi, \
            = symbols('C_1 C_2 C_3 k_1 k_2 k_3 t_12 t_13 t_21 t_23 t_31 t_32 u_1 u_2 u_3 xi')

        self.assertEqual(model.input_vector['expr'], Matrix(3,1,[u_1, u_2, u_3]))
        self.assertEqual(model.state_vector_derivative['expr'], 
                         Matrix([[-C_1*xi*k_1 + C_2*xi*k_2*t_12 + C_3*xi*k_3*t_13 + u_1],
                                [ C_1*xi*k_1*t_21 - C_2*xi*k_2 + C_3*xi*k_3*t_23 + u_2],
                                [ C_1*xi*k_1*t_31 + C_2*xi*k_2*t_32 - C_3*xi*k_3 + u_3]]))

        self.assertFalse(hasattr(self, 'decomp_op_nonlin'))

        # test invalid key __init__
        yaml_str = """\
        model:
            - state_variables: [C_1, C_2, C_3]
            - decomposition_parameters: [k_1, k_2, k_3]
            - transit_parameters: [t_12, t_13, t_21, t_23, t_31, t_32]
            - input_components: [u_1, u_2, u_3]
            - components:
                - C:
                    exprs: "C = Matrix(3,1, [C_1,C_2,C_3])"
                    key: state_vector
                - u:
                    exprs: u = Matrix(3,1, [u_1, u_2, u_3])
                    key: input_vector
                - xi:
                    key: env_eff_mult
                - T:
                    exprs: "T = Matrix([[  -1, t_12, t_13],
                                        [t_21,   -1, t_23],
                                        [t_31, t_32,   -1]])"
                    key: trans_op
                - N:
                    exprs: "N = diag(k_1, k_2, k_3)"
                    # key here not given
                - f_s:
                    exprs: "f_s = u + xi * T * N * C"
                    key: __init__
        """
        model = IncompleteModel(yaml_str)
        model.sections, model.section_titles, model.complete_dict = load_sections_and_titles(model.complete_dict)
        model.df = load_df(model.complete_dict, model.sections)
        model.syms_dict, model.exprs_dict, model.symbols_by_type = load_expressions_and_symbols(model.df) 
        
        with self.assertRaises(YamlException) as cm:
            model.set_component_keys()
        e = cm.exception
        self.assertEqual(e.__str__(), "Invalid component key: '__init__'")


    def test_figure(self):
        yaml_str = """\
        model:
            - state_variables: [C_1, C_2, C_3]
            - environmental_paramters: [gamma]
            - decomposition_parameters: [k_1, k_2, k_3]
            - transit_parameters: [t_12, t_13, t_21, t_23, t_31, t_32]
            - input_components: [u_1, u_2, u_3]
            - components:
                - C:
                    exprs: "C = Matrix(3,1, [C_1, C_2, C_3])"
                    key: state_vector
                - u:
                    exprs: u = Matrix(3,1, [u_1, 0, u_3])
                    key: input_vector
                - xi:
                    exprs: "xi = gamma"
                    key: env_eff_mult
                - T:
                    exprs: "T = Matrix([[  -1,    0, t_13],
                                        [t_21,   -1, t_23],
                                        [t_31,    1,   -1]])"
                    key: trans_op
                - N:
                    exprs: "N = diag(k_1*C_1*C_3, k_2, k_3+5/C_3)"
                    key: decomp_op_nonlin
                - f_s:
                    exprs: "f_s = u + xi * T * N * C"
                    key: state_vector_derivative
        """
        model = IncompleteModel(yaml_str)
        model.sections, model.section_titles, model.complete_dict = load_sections_and_titles(model.complete_dict)
        model.df = load_df(model.complete_dict, model.sections)
        model.syms_dict, model.exprs_dict, model.symbols_by_type = load_expressions_and_symbols(model.df) 
        model.set_component_keys()
        
        pm = model.reservoir_model

        fig = pm.figure((7,7))
        fig.savefig("model_plot.pdf")


    def test_key_relations(self):
        yaml_str = """\
        model:
            - state_variables: 
                - C_1:
                    key: foliage 
                - C_2 
                - C_3

            - environmental_paramters: 
                - T:
                    key: Temperature

            - decomposition_parameters: [k_1, k_2, k_3]
            - components:
                - C:
                    exprs: "C = Matrix(3,1, [C_1, C_2, C_3])"
                    key: state_vector
                - b:
                    exprs: b = Matrix(3,1, [1, 0, 1])
                    key: input_vector
                - u:
                    exprs: u=T*C_1+T*C_2
                    key: scalar_func_phot
                - A:
                    exprs: "A = diag(-k_1, -k_2, -k_3)"
                    key: decomp_op_nonlin
                - f_s:
                    exprs: "f_s = u*b + A* C"
                    key: state_vector_derivative
        """
        model = IncompleteModel(yaml_str)
        model.outsideName="Test1"
        model.sections, model.section_titles, model.complete_dict = load_sections_and_titles(model.complete_dict)
        model.df = load_df(model.complete_dict, model.sections)
        model.syms_dict, model.exprs_dict, model.symbols_by_type = load_expressions_and_symbols(model.df) 
        model.set_component_keys()
        
        res=model.find_keys_used_in_key("scalar_func_phot")
        ref={"Temperature","foliage"}
        self.assertEqual(ref,res)
        
        res=model.find_keys_or_symbols_used_in_key("scalar_func_phot")
        # note that C_2 has no key attached 
        ref={"Temperature","foliage","C_2"}
        self.assertEqual(ref,res)

        #print(res)
        #ref={Symbol("C_2")}
        #self.assertEqual(ref,res)


    def test_dependencies(self):
        yaml_str = """\
        model:
            - environmental_paramters: 
                - a
                - Ti:
                    key: Temperature
                - f:
                    key: foliage

            - components:
                - b:
                    exprs: b = Matrix(3,1, [1, 0, 1])
                    key: input_vector
                - u:
                    exprs: u=Ti*f
                    key: scalar_func_phot
                - f_s:
                    exprs: "f_s = u*b"
                    key: state_vector_derivative
        """
        model_0 = IncompleteModel(yaml_str)
        model_0.outsideName="Test1"
        model_0.sections, model_0.section_titles, model_0.complete_dict = load_sections_and_titles(model_0.complete_dict)
        model_0.df = load_df(model_0.complete_dict, model_0.sections)
        model_0.syms_dict, model_0.exprs_dict, model_0.symbols_by_type = load_expressions_and_symbols(model_0.df) 
        
        ##assertions

        self.assertEqual(model_0.get_expr_str_rhs_or_None("b"),"Matrix(3,1, [1, 0, 1])")
        self.assertEqual(model_0.get_expr_str_rhs_or_None("Ti"),None)
        self.assertEqual(model_0.get_key_of_var_name_or_None("Ti"),"Temperature")
        self.assertEqual(model_0.get_key_of_var_name_or_None("a"),None)

        res=model_0.find_all_variables_in_dependency_tree_of_expr("f_s")
        ref=set(["u","b","Ti","f"])
        self.assertEqual(ref,res)
        
        res=model_0.find_keys_used_in_key("scalar_func_phot")
        print(res)
        res=model_0.find_keys_used_in_key("state_vector_derivative")
        print(res)

    def test_T_N_u_to_reservoir_model(self):
        yaml_str = """\
        model:
            - state_variables: [C_1, C_2]
            - decomposition_parameters: [k_1, k_2 ]
            - transit_parameters: [t_12, t_21 ]
            - input_components: [u_1, u_2]
            - components:
                - C:
                    exprs: "C = Matrix([C_1, C_2])"
                    key: state_vector
                - u:
                    exprs: u = Matrix([u_1, u_2])
                    key: input_vector
                - T:
                    exprs: "T = Matrix([[  -1, t_12],
                                        [t_21,   -1]])"
                    key: trans_op
                - N:
                    exprs: "N = diag(k_1, k_2)"
                    key: decomp_op_nonlin
                - f_s:
                    exprs: "f_s = u +  T * N * C"
                    key: state_vector_derivative
        """
        model = IncompleteModel(yaml_str)
        model.sections, model.section_titles, model.complete_dict = load_sections_and_titles(model.complete_dict)
        model.df = load_df(model.complete_dict, model.sections)
        model.syms_dict, model.exprs_dict, model.symbols_by_type = load_expressions_and_symbols(model.df) 
        model.set_component_keys()
        
        mod= model.reservoir_model
        

    def test_xi_T_N_u(self):
        # f = u + xi*T*N*
        yaml_str = """\
        model:
            - state_variables: [C_1, C_2, C_3]
            - environmental_paramters: [gamma]
            - decomposition_parameters: [k_1, k_2, k_3]
            - transit_parameters: [t_12, t_13, t_21, t_23, t_31, t_32]
            - input_components: [u_1, u_2, u_3]
            - components:
                - C:
                    exprs: "C = Matrix(3,1, [C_1, C_2, C_3])"
                    key: state_vector
                - u:
                    exprs: u = Matrix(3,1, [u_1, u_2, u_3])
                    key: input_vector
                - xi:
                    exprs: "xi = gamma"
                    key: env_eff_mult
                - T:
                    exprs: "T = Matrix([[  -1, t_12, t_13],
                                        [t_21,   -1, t_23],
                                        [t_31, t_32,   -1]])"
                    key: trans_op
                - N:
                    exprs: "N = diag(k_1, k_2, k_3)"
                    key: decomp_op_nonlin
                - f_s:
                    exprs: "f_s = u + xi * T * N * C"
                    key: state_vector_derivative
        """
        model = IncompleteModel(yaml_str)
        model.sections, model.section_titles, model.complete_dict = load_sections_and_titles(model.complete_dict)
        model.df = load_df(model.complete_dict, model.sections)
        model.syms_dict, model.exprs_dict, model.symbols_by_type = load_expressions_and_symbols(model.df) 
        model.set_component_keys()
        
        # test conversion to matrices l
        pm = model.reservoir_model
        xi2, T2, N2, C2, u2 = pm.xi_T_N_u_representation()
        self.assertTrue(Eq(u2+xi2*T2*N2*C2, model.fs))


    def test_A_u(self):
        # f = u + A*C
        yaml_str = """\
        model:
            - state_variables: [C_1, C_2, C_3]
            - decomposition_parameters: [k_1, k_2, k_3]
            - transit_parameters: [a_12, a_13, a_21, a_23, a_31, a_32]
            - input_components: [u_1, u_2, u_3]
            - components:
                - C:
                    exprs: "C = Matrix(3,1, [C_1, C_2, C_3])"
                    key: state_vector
                - u:
                    exprs: u = Matrix(3,1, [u_1, u_2, u_3])
                    key: input_vector
                - A:
                    exprs: "A = Matrix([[-k_1, a_12, a_13],
                                        [a_21, -k_2, a_23],
                                        [a_31, a_32, -k_3]])"
                    key: decomp_op_lin
                - f_s:
                    exprs: "f_s = u + A * C"
                    key: state_vector_derivative
        """
        model = IncompleteModel(yaml_str)
        model.sections, model.section_titles, model.complete_dict = load_sections_and_titles(model.complete_dict)
        model.df = load_df(model.complete_dict, model.sections)
        model.syms_dict, model.exprs_dict, model.symbols_by_type = load_expressions_and_symbols(model.df) 
        model.set_component_keys()
        
            
        # test backward conversion to matrices
        pm = model.reservoir_model
        xi2, T2, N2, C2, u2 = pm.xi_T_N_u_representation()
        self.assertTrue(Eq(u2+xi2*T2*N2*C2, model.fs))
        A = pm.compartmental_matrix


    def test_xi_A_u(self):
        # f = u + xi*A*C
        yaml_str = """\
        model:
            - state_variables: [C_1, C_2, C_3]
            - environmental_paramters: [gamma]
            - decomposition_parameters: [k_1, k_2, k_3]
            - transit_parameters: [a_12, a_13, a_21, a_23, a_31, a_32]
            - input_components: [u_1, u_2, u_3]
            - components:
                - C:
                    exprs: "C = Matrix(3,1, [C_1, C_2, C_3])"
                    key: state_vector
                - u:
                    exprs: u = Matrix(3,1, [u_1, u_2, u_3])
                    key: input_vector
                - xi:
                    exprs: "xi = gamma"
                    key: env_eff_mult
                - A:
                    exprs: "A = Matrix([[-k_1, a_12, a_13],
                                        [a_21, -k_2, a_23],
                                        [a_31, a_32, -k_3]])"
                    key: decomp_op_lin
                - f_s:
                    exprs: "f_s = u + xi * A * C"
                    key: state_vector_derivative
        """
        model = IncompleteModel(yaml_str)
        model.sections, model.section_titles, model.complete_dict = load_sections_and_titles(model.complete_dict)
        model.df = load_df(model.complete_dict, model.sections)
        model.syms_dict, model.exprs_dict, model.symbols_by_type = load_expressions_and_symbols(model.df) 
        model.set_component_keys()
        
            
        # test backward conversion to matrices
        pm = model.reservoir_model
        xi2, T2, N2, C2, u2 = pm.xi_T_N_u_representation()
        self.assertTrue(Eq(u2+xi2*T2*N2*C2, model.fs))


    def test_xi_T_N_u_nonlinear(self):
        # f = u + xi*T*N*
        yaml_str = """\
        model:
            - state_variables: [C_1, C_2, C_3]
            - environmental_paramters: [gamma]
            - decomposition_parameters: [k_1, k_2, k_3]
            - transit_parameters: [t_12, t_13, t_21, t_23, t_31, t_32]
            - input_components: [u_1, u_2, u_3]
            - components:
                - C:
                    exprs: "C = Matrix(3,1, [C_1, C_2, C_3])"
                    key: state_vector
                - u:
                    exprs: u = Matrix(3,1, [u_1, u_2, u_3])
                    key: input_vector
                - xi:
                    exprs: "xi = gamma*2"
                    key: env_eff_mult
                - T:
                    exprs: "T = Matrix([[  -1, t_12*C_2, t_13],
                                        [t_21,   -1, t_23],
                                        [t_31*k_1, t_32,   -1]])"
                    key: trans_op
                - N:
                    exprs: "N = diag(k_1*C_2, k_2/C_3, k_3)"
                    key: decomp_op_nonlin
                - f_s:
                    exprs: "f_s = u + xi * T * N * C"
                    key: state_vector_derivative
        """
        model = IncompleteModel(yaml_str)
        model.sections, model.section_titles, model.complete_dict = load_sections_and_titles(model.complete_dict)
        model.df = load_df(model.complete_dict, model.sections)
        model.syms_dict, model.exprs_dict, model.symbols_by_type = load_expressions_and_symbols(model.df) 
        model.set_component_keys()
        
        # test backward conversion to matrices
        pm = model.reservoir_model
        xi2, T2, N2, C2, u2 = pm.xi_T_N_u_representation()

        self.assertTrue(Eq(u2+xi2*T2*N2*C2, model.fs)
)


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

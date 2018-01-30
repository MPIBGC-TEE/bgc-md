# vim: set expandtab ts=4
import unittest 
#from run_tests import *
from bgc_md.tests.TestModel import TestModel
from bgc_md.tests.TestReportElements import TestReportElements
#from bgc_md.tests.TestDensityAlgorithm import TestDensityAlgorithm
#from bgc_md.tests.TestReportElements import TestReportElements, TestWriteReportElements

def suite():
    s=unittest.TestSuite()
    #s.addTest(Test(""))
    #s.addTest(TestWriteReportElements("test_write_html_with_bibliography"))
    #s.addTest(TestWriteReportElements("test_write_html_with_picture"))
    #s.addTest(TestReportElements("test_Report"))
    #s.addTest(TestReportElements("test_TableRow"))
    #s.addTest(TestReportElements("test_Text"))
    #s.addTest(TestReportElements("test_Math"))
    #s.addTest(TestReportElements("test_TableRow"))
    #s.addTest(TestReportElements("test_Report"))
    #s.addTest(TestReportElements("test_ReportElementList"))
    #s.addTest(TestReportElements("test_add"))
    #s.addTest(TestDensityAlgorithm("test_age_distribution"))
    #s.addTest(TestDensityAlgorithm("test_age_distribution_for_2_pools"))
    #s.addTest(TestModel("test_load_model_runs_dict"))
    #s.addTest(TestModel("test_jacobian"))
    #s.addTest(TestModel("test_set_component_keys"))
    #s.addTest(TestModel("test_reservoir_model"))
    #s.addTest(TestModel("test_matrix_to_fluxes_and_back"))
    #s.addTest(TestModel("test_matrix_to_flux_and_back_nonlinear"))
    #s.addTest(TestModel("test_load_model_run_combinations"))
    #s.addTest(TestModel("test_figure"))
    #s.addTest(TestModel("test_check_parameter_set_complete"))
    #s.addTest(TestModel("test_check_initial_values_complete"))
    #s.addTest(TestModel("test_check_initial_values_valid"))
    s.addTest(TestReportElements("test_Text"))
    return(s)
    
if  __name__ == '__main__':
    s=suite()
    unittest.TextTestRunner(verbosity=2).run(s)

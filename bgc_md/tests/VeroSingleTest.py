# vim: set expandtab ts=4
import unittest 
#from run_tests import *
from bgc_md.tests.TestModel import TestModel
#from bgc_md.tests.TestDensityAlgorithm import TestDensityAlgorithm
#from bgc_md.tests.TestReportElements import TestReportElements, TestWriteReportElements
#from bgc_md.tests.TestReportGeneration import TestReportGeneration

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
    #s.addTest(TestModel("test_key_relations"))
    #s.addTest(TestReportGeneration("test_histogram"))
    s.addTest(TestModel("test_plot_model_key_dependencies_scatter_plot"))
    s.addTest(TestModel("test_dependencies"))
    return(s)
    
if  __name__ == '__main__':
    s=suite()
    unittest.TextTestRunner(verbosity=2).run(s)

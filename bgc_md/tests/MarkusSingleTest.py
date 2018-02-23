#!/usr/bin/env python3 
# vim: set expandtab ts=4
import unittest
#from run_tests import *
from bgc_md.tests.TestCompleteModelList import TestCompleteModelList
#from bgc_md.tests.TestModel import TestModel
from bgc_md.tests.TestModelList import TestModelList
#from bgc_md.tests.TestStoichiometricModel import TestStoichiometricModel
#from bgc_md.tests.TestTsTpField import TestTsTpField
#from bgc_md.tests.TestTsTpMassFieldsPerPoolPerTimeStep import TestTsTpMassFieldsPerPoolPerTimeStep 
from bgc_md.tests.TestWriteReportElements import  TestWriteReportElements
from bgc_md.tests.TestReportGeneration import TestReportGeneration

def suite():
    s=unittest.TestSuite()
    s.addTest(TestCompleteModelList("test_scatter_plus_hist_nr_vars_vs_nr_ops"))
    #s.addTest(TestReportGeneration("test_commandline_generate_model_run_report"))
    #s.addTest(TestReportGeneration("test_commandline_gnerate_website"))
    #s.addTest(TestCompleteModelList("test_scatter_plus_hist_nr_vars_vs_nr_ops"))
    #s.addTest(TestModelList("test_create_overview_report"))
    #s.addTest(TestModelList("test_create_overview_table"))
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
    #s.addTest(TestTsTpMassFieldsPerPoolPerTimeStep("test_mean_age_distribution_for_BW"))
    #s.addTest(TestModel("test_load_model_runs_dict"))
    #s.addTest(TestModel("test_jacobian"))
    #s.addTest(TestModel("test_key_relations"))
    #s.addTest(TestReportGeneration("test_histogram"))
    #s.addTest(TestReportGeneration("test_commandline_tools"))
    #s.addTest(TestModel("test_plot_model_key_dependencies_scatter_plot"))
    #s.addTest(TestModel("test_meta_data"))
    #s.addTest(TestModel("test_reservoir_model"))
    #s.addTest(TestStoichiometricModel("test_rhs"))
    #s.addTest(TestSmoothReservoirModel("test_matrix_to_fluxes_and_back"))
    #s.addTest(TestModel("test_dependencies"))
    #s.addTest(TestTsTpField("test_plot"))
    #s.addTest(TestTsTpField("test_plot_bins"))
    #s.addTest(TestCompleteModelList("test_scatter_plus_hist_nr_vars_vs_nr_ops"))
    return(s)
    
if  __name__ == '__main__':
    s=suite()
    unittest.TextTestRunner(verbosity=2).run(s)

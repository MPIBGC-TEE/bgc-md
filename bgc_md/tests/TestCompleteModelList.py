# vim:set ff=unix expandtab ts=4 sw=4:
import unittest
from testinfrastructure.InDirTest import InDirTest
import yaml
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from pathlib import Path
from bgc_md.IncompleteModel import IncompleteModel
from bgc_md.Model import Model, load_bibtex_entry, load_abstract, load_further_references, load_reviews, load_sections_and_titles, load_df, load_expressions_and_symbols, section_subdict, load_model_run_data, load_parameter_sets, load_initial_values, check_parameter_set_valid, check_parameter_sets_valid, check_parameter_set_complete, check_initial_values_set_valid, check_initial_values_complete, load_run_times, load_model_run_combinations, YamlException
from bgc_md.ModelList import ModelList
from bgc_md.reports import defaults

class TestCompleteModelList(InDirTest):
    def setUp(self):
        this=Path(__file__).parents[1] #the package dir
        vegModelPath=defaults()['paths']['veg'] ### Fix me!!! Temporarily changed Vegetation for Test
        self.ml=ModelList.from_dir_path(vegModelPath)

    def test_plot_model_key_dependencies_scatter_plot(self):
        ml=self.ml #only veg
        target_key="scalar_func_phot"
        sublist=ModelList([el for el in ml if el.has_key(target_key)])
        fig = plt.figure()
        ax=fig.add_subplot(1,1,1)
        sublist.plot_model_key_dependencies_scatter_plot(target_key,ax)
        fig.savefig("plot.pdf")
        ax=fig.add_subplot(1,1,1)

# The following function no longer exists:    
#    def test_scatter_plus_hist_nr_vars_vs_nr_ops(self):
#        ml=self.ml
#        fig = plt.figure()
#        ax=fig.add_subplot(1,1,1)
#        ml.scatter_plus_hist_nr_vars_vs_nr_ops(ax)
#        plt.close(fig.number)
#        fig.savefig("plot.pdf")
#        plt.close(fig.number)

    def test_denpendency_plots_from_keys_in_compartments(self):
        fig = plt.figure(figsize=(30,30),tight_layout=True)
        self.ml.denpendency_plots_from_keys_in_compartments(fig)
        fig.savefig("plot.pdf")
        plt.close(fig.number)


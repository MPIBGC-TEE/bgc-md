
from unittest import skip
import sys
from multiprocessing import Pool
from subprocess import run,CalledProcessError
from pathlib import Path
import shutil 
from bgc_md.Model import Model
from testinfrastructure.InDirTest import InDirTest
from bgc_md.reports import produce_model_report_markdown, produce_model_report_markdown_directory, create_html_from_pandoc_md, create_html_from_pandoc_md_directory,generate_website,defaults,create_overview_report,render
from bgc_md.yaml_creator_mod import example_yaml_string_list2
from bgc_md.helpers import remove_indentation
from bgc_md.ModelList import ModelList
import bgc_md.gv as gv
class TestReportGeneration(InDirTest):
    def test_report_template_fluxes(self):
        
        d=defaults() 
        sp=d['paths']['tested_records'].joinpath('Fluxes.yaml')

        tp=d['paths']['report_templates'].joinpath('single_model','CompleteSingleModelReport.py')
        model=Model.from_path(sp)
        pe('model.get_component_keys()')
        #rel=render(tp,model)

        #target_dir_path=Path('.').joinpath('html')
        #target_dir_path.mkdir(parents=True,exist_ok=True)
        #targetFileName='Report.html'
        #rel.write_pandoc_html(target_dir_path.joinpath(targetFileName))



    def test_website_from_template(self):
        d=defaults() 
        sp=d['paths']['tested_records'].parent.joinpath('TestModels_1')
        model_list=ModelList.from_dir_path(sp)

        list_tp=d['paths']['report_templates'].joinpath('multiple_model','Website.py')
        #rel=render(list_tp,model_list=model_list)
        rel=render(list_tp,model_list)

        target_dir_path=Path('.')
        target_dir_path.mkdir(parents=True,exist_ok=True)
        targetFileName='overview.html'
        rel.write_pandoc_html(target_dir_path.joinpath(targetFileName))

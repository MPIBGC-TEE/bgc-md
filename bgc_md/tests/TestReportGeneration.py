#!/usr/bin/env python3
# vim:set ff=unix expandtab ts=4 sw=4:
from unittest import skip
import sys
from multiprocessing import Pool
from subprocess import run,CalledProcessError
from pathlib import Path
import shutil 
from bgc_md.Model import Model
from testinfrastructure.InDirTest import InDirTest
from bgc_md.reports import produce_model_report_markdown, produce_model_report_markdown_directory,  defaults,render
from bgc_md.yaml_creator_mod import example_yaml_string_list2
from bgc_md.helpers import remove_indentation
from bgc_md.ModelList import ModelList
import bgc_md.gv as gv


class TestReportGeneration(InDirTest):


    def test_flagstaff_templates_commandline(self):
        d=defaults() 
        sp=d['paths']['data'].joinpath('FlagstaffTemplates')
        tp=d['paths']['report_templates'].joinpath('single_model','FlagstaffVegetationTemplate.py')
        rec_list=[ rec  for rec in sp.glob('*.yaml')]#[0:2]
        for rec in rec_list:
            #print(rec)
            run(["render", str(tp.absolute()),"-y",str(rec.absolute()),"-t","."])
            #m=Model.from_path(rec)
            #rel=render(tp,model=m)
#
        

    def test_report_template_single_model(self):
        
        d=defaults() 
        sp=d['paths']['tested_records'].parent.joinpath('TestModels_1').joinpath('Williams2005GCB.yaml')

        #tp=d['paths']['report_templates'].joinpath('single_model','MinimalSingleReport.py')
        #tp=d['paths']['report_templates'].joinpath('single_model','TransientMeanAges.py')
        tp=d['paths']['report_templates'].joinpath('single_model','TransientSystemAgeDensity3d.py')
        model=Model.from_path(sp)
        rel=render(tp,model)
        targetFileName='Report.html'
        target_dir_names=['pandoc','pypandoc']
        target_dir_paths={n:Path('.').joinpath(n) for n in target_dir_names}
        for p in target_dir_paths.values():
            p.mkdir(parents=True,exist_ok=True)
        rel.write_pandoc_html(target_dir_paths['pandoc'].joinpath(targetFileName))
        rel.write_pypandoc_html(target_dir_paths['pypandoc'].joinpath(targetFileName))


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
        target_dir_names=['pandoc','pypandoc']
        target_dir_paths={n:Path('.').joinpath(n) for n in target_dir_names}
        for p in target_dir_paths.values():
            p.mkdir(parents=True,exist_ok=True)
        rel.write_pandoc_html(target_dir_paths['pandoc'].joinpath(targetFileName))
        rel.write_pypandoc_html(target_dir_paths['pypandoc'].joinpath(targetFileName))



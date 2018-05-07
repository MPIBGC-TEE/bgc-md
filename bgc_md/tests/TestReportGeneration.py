#!/usr/bin/env python3
# vim:set ff=unix expandtab ts=4 sw=4:
import unittest
import sys
from multiprocessing import Pool
from subprocess import run,CalledProcessError
from concurrencytest import ConcurrentTestSuite, fork_for_tests
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
    def test_report_template_single_model(self):
        d=defaults() 
        sp=d['paths']['tested_records'].parent.joinpath('TestModels_1').joinpath('Williams2005GCB.yaml')

        tp=d['paths']['report_templates'].joinpath('MinimalSingleReport.py')
        model=Model.from_path(sp)
        rel=render(tp,model)

        target_dir_path=Path('.').joinpath('html')
        target_dir_path.mkdir(parents=True,exist_ok=True)
        targetFileName='Report.html'
        rel.write_pandoc_html(target_dir_path.joinpath(targetFileName))


    def test_website_from_template(self):
        d=defaults() 
        sp=d['paths']['tested_records'].parent.joinpath('TestModels_1')
        model_list=ModelList.from_dir_path(sp)

        list_tp=d['paths']['report_templates'].joinpath('Website.py')
        #rel=render(list_tp,model_list=model_list)
        rel=render(list_tp,model_list)

        target_dir_path=Path('.')
        target_dir_path.mkdir(parents=True,exist_ok=True)
        targetFileName='overview.html'
        rel.write_pandoc_html(target_dir_path.joinpath(targetFileName))

#
    def test_create_overview_report(self):
        # fixme:
        # The tested method is deprecated and should be replaced by templates as soon as possible.
        # we create a target directory populated with only a few files and create a overview html from it
        d=defaults() 
        #sp=d['paths']['tested_records']
        sp=d['paths']['tested_records'].parent.joinpath('VerosTestModels')
        src_dir_name='localDataBase'
        src_dir_path=Path(src_dir_name)
        src_dir_path.mkdir()
        rec_list=[ rec  for rec in sp.glob('*.yaml')]#[0:2]
        
        for rec in rec_list:
            src=str(sp.joinpath(rec))
            target=(src_dir_name)

            shutil.copy(src,src_dir_name)
         
        ml=ModelList.from_dir_path(src_dir_path)

        target_dir_path=Path('.').joinpath('html')
        targetFileName='overview.html'
        create_overview_report(ml,target_dir_path,targetFileName)
        targetPath=target_dir_path.joinpath(targetFileName)
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

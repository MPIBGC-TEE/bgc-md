#!/usr/bin/env python3
# vim:set ff=unix expandtab ts=4 sw=4:
import unittest
import sys
from multiprocessing import Pool
from subprocess import run,CalledProcessError
from pathlib import Path
from string import Template
import shutil 
from bgc_md.Model import Model
from testinfrastructure.InDirTest import InDirTest
from bgc_md.reports import produce_model_report_markdown, produce_model_report_markdown_directory, create_html_from_pandoc_md, create_html_from_pandoc_md_directory,generate_website
from bgc_md.yaml_creator_mod import example_yaml_string_list2
from bgc_md.helpers import remove_indentation
from bgc_md.reports import defaults
import bgc_md.gv as gv


def f(l):
    tp,rec=l
    targetPath=Path('.')
    print("1 ###################")
    print(tp.stem)
    print(rec.stem)
    command_list=['render','-y']
    file_name=str(rec)
    command_list+=[file_name]
    command_list+=[str(tp.absolute())]
    res=run(command_list)
    result=dict()
    result['file']=rec.stem
    result['template']=tp.stem
    result['returnValue']=res.returncode
    html_dir_path=targetPath.joinpath(rec.stem)
    html_file_path=html_dir_path.joinpath(tp.stem+'.html')
    result['fileExists']=html_file_path.exists()
    return(result)



class SlowTestSingleYaml(InDirTest):
    def test_commandline_render_all_templates(self):
        # this is a matrix test that tests all templates in report_templates/single_model
        # against all records in data/tested_records
        d=defaults() 
        template_path=d['paths']['report_templates'].joinpath('single_model')
        tps=[tp for tp in template_path.glob('*.py')]
        # you can even 
        #tps=[template_path.joinpath('GeneralOverview.py')]
        sp=d['paths']['tested_records']

        # put the file you want to test in the rec_list
        #rec_list=[ rec  for rec in sp.glob('*.yaml')]
        #rec_list=[sp.joinpath("Ceballos2016.yaml")] 
        rec_list=[sp.joinpath("Wang2014BG3p.yaml")] 

        #test_list= rec_list
        test_list= [ [tp,rec] for rec in sorted(rec_list) for tp in  tps]

        pool=Pool(processes=16)
        result_list=pool.map(f,test_list)
       # 
        failure_list=[
            r  for r in result_list 
            if r['returnValue']!=0 or r['fileExists']==False
        ]
        def fail_line(d):
            t=Template( "${f}\t\t${t}\t\t${r}\t\t${fe}")
            return t.substitute(f=d['file'],t=d['template'],r=d['returnValue'],fe=d['fileExists'])

        failure_msg="\n".join(map(fail_line,failure_list))

        self.assertEqual(
            len(failure_list)
            ,0
            ,msg="The following files caused problems \n%s" % failure_msg
        )

#

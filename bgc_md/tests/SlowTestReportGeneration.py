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

def runProtected_old(rec,command_list,targetPath=Path('.')):
    file_name=str(rec)
    result=dict()
    res=run(command_list+[file_name])
    result['file']=file_name
    result['returnValue']=res.returncode
    html_dir_path=targetPath.joinpath(rec.stem)
    html_file_path=html_dir_path.joinpath('Report.html')
    result['fileExists']=html_file_path.exists()
    return(result)

def f_old(rec):
    command_list=['generate_model_run_report']
    d=defaults() 
    result=runProtected(rec,command_list)
    return result




def runProtected(rec,command_list,targetPath=Path('.')):
    file_name=str(rec)
    result=dict()
    res=run(command_list+[file_name])
    result['file']=file_name
    result['returnValue']=res.returncode
    html_dir_path=targetPath.joinpath(rec.stem)
    html_file_path=html_dir_path.joinpath('Report.html')
    result['fileExists']=html_file_path.exists()
    return(result)

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



class SlowTestReportGeneration(InDirTest):
    def test_commandline_render_single_model_templates(self):
        # this is a matrix test that tests all templates in report_templates/single_model
        # against all records in data/tested_records
        d=defaults() 
        template_path=d['paths']['report_templates'].joinpath('single_model')
        tps=[tp for tp in template_path.glob('*.py')]
        sp=d['paths']['tested_records']
        rec_list=[ rec  for rec in sp.glob('*.yaml')]
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

    def test_commandline_generate_model_run_report(self):
        d=defaults() 
        sp=d['paths']['tested_records']
        rec_list=[ rec  for rec in sp.glob('*.yaml')]
        test_list= rec_list
        #test_list= sorted(rec_list)[2:3]

        pool=Pool(processes=1)
        result_list=pool.map(f,test_list)
       # 
        failure_list=[
            r  for r in result_list 
            if r['returnValue']!=0 or r['fileExists']==False
        ]
        self.assertEqual(
            len(failure_list)
            ,0
            ,msg="The following files caused problems %s" % str(failure_list)
            )


    def test_commandline_generate_model_run_report_single_file(self):
        # This function is more of a tool to test a 
        # specific selectable yaml file 
        # than an active automatic test. 
        # Usually the specific file will be tested by one of the 
        # more comprehensive tests that iterate over all our model files.
        d=defaults() 
        sp=d['paths']['tested_records']
        here=Path('.')
        rec_list=[ rec  for rec in sp.glob('*.yaml')]
        test_list= rec_list
        #test_list=['Allison2010NatureGeoscience.yaml']
        targetDirName='output'
        targetPath=here.joinpath(targetDirName)
        targetPath.mkdir(parents=True,exist_ok=True)
        
        result_list=[ runProtected( rec ,['generate_model_run_report',"-t", targetDirName] ,targetPath) for rec in test_list
        ]
        failure_list=[r  for r in result_list if r['returnValue']!=0 or r['fileExists']==False]
        self.assertEqual(
            len(failure_list)
            ,0
            ,msg="The following files caused problems %s" % str(failure_list)
        )

    def test_commandline_generate_model_run_report_with_targetdir(self):
        # test the -t option for a smaller selection of yaml file
        d=defaults() 
        sp=d['paths']['tested_records']
        here=Path('.')
        rec_list=[ rec  for rec in sp.glob('*.yaml')]
        #test_list= rec_list
        test_list= sorted(rec_list)[2:3]
        targetDirName='output'
        targetPath=here.joinpath(targetDirName)
        targetPath.mkdir(parents=True,exist_ok=True)
        test_list= sorted(rec_list)[0:1]
        result_list=[ runProtected( rec ,['generate_model_run_report',"-t", targetDirName] ,targetPath) for rec in test_list
        ]
        failure_list=[r  for r in result_list if r['returnValue']!=0 or r['fileExists']==False]
        self.assertEqual(
            len(failure_list)
            ,0
            ,msg="The following files caused problems %s" % str(failure_list)
        )

    def test_commandline_gnerate_website(self):
        # we create a target directory populated with only a few files and create a website from it
        d=defaults() 
        sp=d['paths']['tested_records']
        src_dir_name='localDataBase'
        src_dir_path=Path(src_dir_name)
        src_dir_path.mkdir()
        rec_list=sorted([ rec  for rec in sp.glob('*.yaml')])[2:3]
        
        for rec in rec_list:
            print(rec)
            src=(sp.joinpath(rec)).as_posix()
            target=(src_dir_name)
            shutil.copy(src,src_dir_name)
        
        res=run(['generate_website','-s',src_dir_name],check=True )
    
#    @unittest.skip("function under test calls report_from_yaml_str which is commented out")
#    def test_report_html_presence(self):
#    # fixme
#    # to be deprecated
#
#        for index, yaml_str in enumerate(self.yaml_str_list):
#            trunk = "testfile" + str(index)
#            yaml_file_name = trunk + ".yaml"
#            markdown_file_name = trunk + ".md"
#            html_file_name = trunk + ".html"
#            csl_file_name = gv.resources_path.joinpath('apa.csl').as_posix()
#            css_file_name = gv.resources_path.joinpath('buttondown.css').as_posix()
#
#            # yaml -> md, bibtex -> html
#            produce_model_report_markdown(yaml_file_name, markdown_file_name)
#            create_html_from_pandoc_md(markdown_file_name, html_file_name,
#                                        csl_file_name=csl_file_name, css_file_name=css_file_name, slide_show=False)
#            #check if the result has been produced where we expected 
#            self.assertTrue(Path(html_file_name).exists())
#
#            # yaml -> md, bibtex -> html (slide show)
#            html_file_name = trunk + "_ss.html"
#            produce_model_report_markdown(yaml_file_name, markdown_file_name)
#            create_html_from_pandoc_md(markdown_file_name, html_file_name,
#                                        csl_file_name=csl_file_name, css_file_name=css_file_name, slide_show=True)
#            #check if the result has been produced where we expected 
#            self.assertTrue(Path(html_file_name).exists())
#
#    @unittest.skip("function under test calls report_from_yaml_str which is commented out")
#    def test_report_html_presence_directory(self):
#    # fixme
#    # to be deprecated
#        csl_file_name = gv.resources_path.joinpath('apa.csl').as_posix()
#        css_file_name = gv.resources_path.joinpath('buttondown.css').as_posix()
#        produce_model_report_markdown_directory("", "md")
#        create_html_from_pandoc_md_directory("md", "html", csl_file_name=csl_file_name, css_file_name=css_file_name)
#        
#

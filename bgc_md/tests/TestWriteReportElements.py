#!/usr/bin/env python3
# vim:set ff=unix expandtab ts=4 sw=4:

import unittest
import numpy as np
import sys
from sympy import var,sqrt,pi,sin, sympify
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from pathlib import Path

from bgc_md.ReportInfraStructure import Text, Math, Meta, ReportElementList, TableRow, Table, Header, Newline, Citation, MatplotlibFigure
from testinfrastructure.InDirTest import InDirTest
from bgc_md.helpers import remove_indentation
from bgc_md import gv
from bgc_md.bibtexc import  BibtexEntry, online_entry,entry_list_from_file



class TestWriteReportElements(InDirTest):
    def test_write_pandoc_markdown(self):
        var("x")
        expr=sqrt(2/x)
        rel=Text("name=:$n",n="Markus")+Math("a=$a",a=expr)
        rel.write_pandoc_markdown(Path("report.md"))
    
    def test_write_html_with_bibliography(self):
        csl_file_path = gv.resources_path.joinpath('apa.csl')
        css_file_path = gv.resources_path.joinpath('buttondown.css')
        rel=Text("Some Text")
        rel+=Newline()
        e=BibtexEntry.from_doi(doi="10.1139/x91-133")
        print("#################################################")
        print(e)
        print("#################################################")
        rel+=Citation(e,parentheses=True)
        rel+=Text("This is some text between the citations")
        rel+=Newline()
        rel+=Citation(BibtexEntry.from_doi(doi="10.1556/Select.2.2001.1-2.14"))
        rel+=Text("This is some text after the citation")
        rel+=Newline()
        rel+=Text("This is second citation of the first paper")
        #rel+=Citation(BibtexEntry.from_doi(doi="10.1139/x91-133"),parentheses=True)

        html_file_path=Path("text_with_citation.html")
        bibtex_file_name=Path("text_with_citation.bibtex")
        print('#######################################')
        rel.write_pypandoc_html(html_file_path,csl_file_path,css_file_path)
        
        self.assertTrue(Path(html_file_path).exists())
        # check that the bibtex file is there
        self.assertTrue(Path(bibtex_file_name).exists())
        # check deduplication
        # read the bibtexfile with bibtexparser and 
        # make sure that only two entries are present 
        # which presupposes that the parser does not deduplicate
        et=entry_list_from_file(bibtex_file_name)
        self.assertEqual(len(et),2)

    def test_write_html_with_picture(self):
        csl_file_path = gv.resources_path.joinpath('apa.csl')
        css_file_path = gv.resources_path.joinpath('buttondown.css')
        rel=Text("some text before the first picture")
        fig=plt.figure()
        x_values=[2*pi/100*i for i in range(0,100)]
        y_values=[sin(x) for x in x_values]
        fig.add_subplot(1,1,1).plot(x_values,y_values)
        
        fig2=plt.figure()
        n=1000
        x=np.array([i/(2*n) for i in range(-n,n)],dtype="float")
        y=np.exp(-x**2/2)
        ax0=fig2.add_subplot(1,1,1)
        number_of_bins=20
        ax0.hist(y, number_of_bins, normed=1, histtype='stepfilled', facecolor='g', alpha=0.75)
        rel+=MatplotlibFigure(fig,"Label","caption text2 ") 
        rel+=Newline()
        
        rel+=Text("some text before the second picture")
        rel+=MatplotlibFigure(fig2,"differentLabel","caption text 2") 
        # now refer to the figures from the text
        html_file_path=Path("text_with_figure.html")
        rel.write_pypandoc_html(html_file_path,csl_file_path,css_file_path)


        



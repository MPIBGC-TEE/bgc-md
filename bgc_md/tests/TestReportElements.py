# vim:set ff=unix expandtab ts=4 sw=4:

import unittest
import numpy as np
import sys
from sympy import var,sqrt,pi,sin, sympify
from concurrencytest import ConcurrentTestSuite, fork_for_tests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from pathlib import Path

from bgc_md.ReportInfraStructure import Text, Math, Meta, ReportElementList, TableRow, Table, Header, Newline, Citation, MatplotlibFigure
from testinfrastructure.InDirTest import InDirTest
from bgc_md.helpers import remove_indentation
from bgc_md import gv
from bgc_md import bibtexc


class TestReportElements(unittest.TestCase):
    def test_Header(self):
        #self.maxDiff = None
        self.assertEqual(
            Header("General Overview Chapter=$c",1,c=1).pandoc_markdown(),
            "\n# General Overview Chapter=1\n"
        )    
        
        self.assertEqual(
            Header("General Overview Chapter=$c",6,c=1).pandoc_markdown(),
            "\n###### General Overview Chapter=1\n"
        )    

    def test_Text(self):
        t=Text(remove_indentation("""\
                                     ---
                                     title: Model $title
                                     author: $entryAuthor
                                     ---
                                  """), title="Model title", entryAuthor="Veronika")
        target_string = remove_indentation("""\
                          ---
                          title: Model Model title
                          author: Veronika
                          ---
                          """)
        self.assertEqual(t.pandoc_markdown(), target_string)

        desc = "Reference to $F_NSC$, not to $F_{x}$"
        t = Text("$d", d=desc)
        target_string = "Reference to $F_{NSC}$, not to $F_{x}$"
        self.assertEqual(t.pandoc_markdown(), target_string)

        
    def test_Math(self):
        var("x")
        expr=sqrt(2/x)
        self.assertEqual(
            Math("a=$a",a=expr).pandoc_markdown(),
            r"$a=\sqrt{2}\cdot\sqrt{\frac{1}{x}}$"
        )

        m =  Math("$x=$p1", x=x, p1=sympify('alpha*r *   delta'))
        self.assertEqual(m.pandoc_markdown(), r"$x=\alpha\cdot\delta\cdot r$")

    def test_Meta(self):
        long_name = None
        name = "Hilbert 1991"
        version = "2"
        self.assertEqual(
            Meta(long_name, name, version).pandoc_markdown(),
            remove_indentation("""\
                ---
                title: "Report of the model: Hilbert 1991, version: 2"
                ---
            """
            # fixme:
            # extend to entryAuthor,
            )
        )

        long_name = "The beautiful Hilbert model"
        name="Hilbert 1991"
        version="2"
        self.assertEqual(
            Meta(long_name, name, version).pandoc_markdown(),
            remove_indentation("""\
                ---
                title: "Report of the model: The beautiful Hilbert model (Hilbert 1991), version: 2"
                ---
            """
            # fixme:
            # extend to entryAuthor,
            )
        )

    def test_Newline(self):
        self.assertEqual(Newline().pandoc_markdown(), " <br>")


    def test_ReportElementList(self):
        var("x")
        expr=sqrt(2/x)
        rel=ReportElementList([Text("name=:$n",n="Markus"),Math("a=$a",a=expr)])
        self.assertEqual(
            rel.pandoc_markdown(),
            r"name=:Markus$a=\sqrt{2}\cdot\sqrt{\frac{1}{x}}$"
        )
        
    def test_iadd(self):
        var("x")
        expr=sqrt(2/x)
        rel=Text("name=:$n",n="Markus")
        rel+=Math("a=$a",a=expr)
        self.assertEqual(
            rel.pandoc_markdown(),
            r"name=:Markus$a=\sqrt{2}\cdot\sqrt{\frac{1}{x}}$"
        )
        # add a case where lists are added to lists
        rel2=rel
        rel2+=rel
        self.assertEqual(
            rel2.pandoc_markdown(),
            r"name=:Markus$a=\sqrt{2}\cdot\sqrt{\frac{1}{x}}$name=:Markus$a=\sqrt{2}\cdot\sqrt{\frac{1}{x}}$"
        )

    def test_add(self):
        var("x")
        expr=sqrt(2/x)
        rel=Text("name=:$n",n="Markus")+Math("a=$a",a=expr)
        self.assertEqual(
            rel.pandoc_markdown(),
            r"name=:Markus$a=\sqrt{2}\cdot\sqrt{\frac{1}{x}}$"
        )
        # add a case where lists are added to lists
        rel2=rel+rel
        self.assertEqual(
            rel2.pandoc_markdown(),
            r"name=:Markus$a=\sqrt{2}\cdot\sqrt{\frac{1}{x}}$name=:Markus$a=\sqrt{2}\cdot\sqrt{\frac{1}{x}}$"
        )
        # add a case where a Report element is  added to a list
        rel3=rel+Text("Markus")
        self.assertEqual(
            rel3.pandoc_markdown(),
            r"name=:Markus$a=\sqrt{2}\cdot\sqrt{\frac{1}{x}}$Markus"
        )

    def test_mul(self):
        rel = Newline()*3
        self.assertEqual(rel.pandoc_markdown(), " <br> <br> <br>")


    def test_TableRow(self):
        var("x")
        expr=sqrt(2/x)
        tr=TableRow([Text("first col $name",name="test")+Math("a=$a",a=expr),Math("2*a=$a$a",a=expr)])
        self.assertEqual(
            tr.pandoc_markdown(),
            r"first col test$a=\sqrt{2}\cdot\sqrt{\frac{1}{x}}$|$2*a=\sqrt{2}\cdot\sqrt{\frac{1}{x}}\sqrt{2}\cdot\sqrt{\frac{1}{x}}$"
        )


    def test_Table(self):
        # we create a table by giving the firs row
        headers_row=TableRow([Text("name of first column"),Text("name of second column")])
        # and the formats as a list of strings
        formats=["c","l"]
        t=Table("first Table", headers_row,formats)
        var("x")
        expr=sqrt(2/x)
        t.add_row(TableRow([Math("a=$a",a=expr),Math("b=$b",b=2*expr)]))
        res=t.pandoc_markdown()
        self.maxDiff = None
        ref=r"""

        name of first column|name of second column
        :-----:|:-----
        $a=\sqrt{2}\cdot\sqrt{\frac{1}{x}}$|$b=2\cdot\sqrt{2}\cdot\sqrt{\frac{1}{x}}$

        Table: first Table
        """
        ref = remove_indentation(ref)
        self.assertEqual(res,ref)

  #  def test_matplotlib_plot(self):
  #      rel=MatplotlibFigure
    def test_Report(self):
        # we create a table by giving the firs row
        headers_row=TableRow([Text("name of first column"),Text("name of second column")])
        # and the formats as a list of strings
        formats=["c","l"]
        t=Table("first Table", headers_row,formats)
        var("x")
        expr=sqrt(2/x)
        t.add_row(TableRow([Math("a=$a",a=expr),Math("b=$b",b=2*expr)]))
        var("x")
        expr=sqrt(2/x)
        m=Math("a=$a",a=expr)
        tx=Text("###############")
        t+=tx+m
        res=t.pandoc_markdown()
        ref=r"""

        name of first column|name of second column
        :-----:|:-----
        $a=\sqrt{2}\cdot\sqrt{\frac{1}{x}}$|$b=2\cdot\sqrt{2}\cdot\sqrt{\frac{1}{x}}$

        Table: first Table
        ###############$a=\sqrt{2}\cdot\sqrt{\frac{1}{x}}$"""
        ref = remove_indentation(ref)
        #print(">>"+res+"<<")
        #print(">>"+ref+"<<")
        self.assertEqual(res,ref)

class TestWriteReportElements(InDirTest):
    def test_write_pandoc_markdown(self):
        var("x")
        expr=sqrt(2/x)
        rel=Text("name=:$n",n="Markus")+Math("a=$a",a=expr)
        rel.write_pandoc_markdown("report.md")
    
    def test_write_html_with_bibliography(self):
        csl_file_name = gv.resources_path.joinpath('apa.csl').as_posix()
        css_file_name = gv.resources_path.joinpath('buttondown.css').as_posix()
        rel=Text("This is some text")
        rel+=Newline()
        rel+=Citation(bibtexc.BibtexEntry(doi="10.1139/x91-133"),parentheses=True)
        rel+=Text("This is some text between the citations")
        rel+=Newline()
        rel+=Citation(bibtexc.BibtexEntry(doi="10.1556/Select.2.2001.1-2.14"))
        rel+=Text("This is some text after the citation")
        rel+=Newline()
        rel+=Text("This is second citation of the first paper")
        rel+=Citation(bibtexc.BibtexEntry(doi="10.1139/x91-133"),parentheses=True)

        html_file_name="text_with_citation.html"
        bibtex_file_name="text_with_citation.bibtex"

        rel.write_pandoc_html(html_file_name,csl_file_name,css_file_name)
        
        self.assertTrue(Path(html_file_name).exists())
        # check that the bibtex file is there
        self.assertTrue(Path(bibtex_file_name).exists())
        # check deduplication
        # read the bibtexfile with bibtexparser and 
        # make sure that only two entries are present 
        # which presupposes that the parser does not deduplicate
        et=bibtexc.entry_list_from_file(bibtex_file_name)
        self.assertEqual(len(et),2)

    def test_write_html_with_picture(self):
        csl_file_name = gv.resources_path.joinpath('apa.csl').as_posix()
        css_file_name = gv.resources_path.joinpath('buttondown.css').as_posix()
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
        html_file_name="text_with_figure.html"
        rel.write_pandoc_html(html_file_name,csl_file_name,css_file_name)


        


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

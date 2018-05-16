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
from collections import OrderedDict

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
        d=OrderedDict()
        d["name"]="Hilbert 1991"
        d["version"]="2"
        res=Meta(d).pandoc_markdown()
        ref=remove_indentation("""\
            ---
            name: Hilbert 1991 
            version: 2
            ---
            """
        )
        self.assertEqual(res,ref)

    def test_Newline(self):
        self.assertEqual(Newline().pandoc_markdown(), "  ")


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
        self.assertEqual(rel.pandoc_markdown(), "      ")


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
        # the (partly invisible)  spaces at the end of the lins are important since they
        # are interpreted by pandoc as newlines
        ref=r"""  
          
        name of first column|name of second column  
        :-----:|:-----  
        $a=\sqrt{2}\cdot\sqrt{\frac{1}{x}}$|$b=2\cdot\sqrt{2}\cdot\sqrt{\frac{1}{x}}$  
          Table: first Table  
        """
        ref=ref.replace("        ","") # do not use remove_indentation() since it will also remove the needed spaces
        self.assertEqual(res,ref)

  #  def test_matplotlib_plot(self):
  #      rel=MatplotlibFigure


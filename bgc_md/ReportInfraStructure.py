# vim:set ff=unix expandtab ts=4 sw=4:
from string import Template
from copy import copy,deepcopy 
from pathlib import Path
from sympy import sympify
from pytexit import py2tex
from .helpers import py2tex_silent

import shutil
import subprocess
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# imports from own package
from .helpers import remove_indentation
from .BGCmarkdown import MarkdownTemplate 
from . import bibtexc
from . import gv
# needs a test
def exprs_to_element(exprs, symbols_by_type):
    if not exprs:
        return Text("-")

    # two possibilities in yaml file:
    # 1)    exprs: "C = ..."
    # 2)    exprs:
    #           - "C = ..."
    #           - "C = ..."
    # so this table entry will be treated as a list of expressions
    subl = ReportElementList([])
    if type(exprs) == type(""):
        expr_list = [exprs]
    elif type(exprs) == type([]):
        expr_list = exprs
    else:
        raise(Exception(str(exprs) + " is no valid list of expressions."))

    for index2, expr_string in enumerate(expr_list):
        if expr_string:
            # new line if not first entry
            if index2 > 0:
                subl.append(Newline()) 
            parts = expr_string.split("=",1)
            parts[0] = parts[0].strip()
            parts[1] = parts[1].strip()
            p1 = sympify(parts[0], locals=symbols_by_type)
            p2 = sympify(parts[1], locals=symbols_by_type)
            
            # this is a hybrid version that keeps 'f_s = I + A*C' in shape, but if 'Matrix(...)' comes into play, rearranging by sympify within the matrix cannot be prevented
            # comment it out for a a clean version regarding use of ReportElementList, but with showing 
            # 'f_s = A * C + I' instead
            try:
                p2 = py2tex_silent(parts[1])
            except TypeError:
               pass
            
            subl.append(Math("$p1=$p2", p1=p1,p2=p2))
    return subl

class ReportElementList(list):
    def __init__(self,ListOfObjects=[]):
        #use the init method of list to initialize an empty ReportElementList
        super().__init__()
        for obj in ListOfObjects:
            # we accept only TextElements or ReportElementLists
            if isinstance(obj,TextElement) or isinstance(obj,__class__):
                self.append(obj)
            else:
                raise Exception()
            
    #@classmethod
    #def from_list(cls,list):
    #    return(cls(list))

    # is indeed needed!
    def __iadd__(self,rhs):
        res=self+rhs
        return(res)

    def __add__(self,other):
        #cp=deepcopy(self)
        cp=copy(self)
        #cp=self
        return(__class__([cp,other]))

    def __mul__(self,factor):
        res=self
        for i in range(1,factor):
            res+=self
        return res
            
    def pandoc_markdown(self):
        if 'pandoc_markdown_string' in dir(self):
            strs=self.pandoc_markdown_string()
        else:
            strs=""
            for sub_el in self:
                el_str=sub_el.pandoc_markdown()
                strs+=el_str
        return(strs)

    
    def bibtex_entries(self):
        #entries = []
        entries=set()
        if isinstance(self,AtomicReportElementList):
            el=self[0]
            if 'bibtex_entry' in dir(el):
                #entries=[el.bibtex_entry]
                entries|={el.bibtex_entry}
            return(entries)    
        else:
            for sub_el in self:
                #el_lst=sub_el.bibtex_entries()
                #entries+=el_lst
                el_set=sub_el.bibtex_entries()
                entries|=el_set            
            #e_dict={el.key:el for el in entries} 
            # deduplication of the list:
            # if there are two bibtex objects with the same key 
            # the later one overwrites the entry in the dict
            #entries=e_dict.values()
            # backsubstitution to a list
        return(entries)
    
    def sub_pages(self):
        if isinstance(self,AtomicReportElementList):
            if isinstance(self,LinkedSubPage):
                entries=[self[0]]
            else:
                entries = []
            return(entries)    
        else:
            entries = []
            for sub_el in self:
                el_lst=sub_el.sub_pages()
                entries+=el_lst
            
        return(entries)

    def matplotlib_figure_elements(self):
        if isinstance(self,AtomicReportElementList):
            if isinstance(self,MatplotlibFigure):
                entries=[self[0]]
            else:
                entries = []
            return(entries)    
        else:
            entries = []
            for sub_el in self:
                el_lst=sub_el.matplotlib_figure_elements()
                entries+=el_lst
            
        return(entries)

    def write_pandoc_html(self,html_file_path,csl_file_path=None , css_file_path= None, slide_show = False):
        csl_file_name=str(csl_file_path)
        css_file_name=str(css_file_path)
        html_file_name=str(html_file_path)
        html_file_path=Path(html_file_name)
        
        dir_path=html_file_path.parent
        if not dir_path.exists():
            dir_path.mkdir(parents=True)

        if csl_file_path is None:
            csl_file_path= gv.resources_path.joinpath('apa.csl')
        if css_file_path is None:
            css_file_path= gv.resources_path.joinpath('buttondown.css')
        trunk = html_file_path.stem

        md_file_path = html_file_path.parent.joinpath(html_file_path.stem+".md")
        bibtex_file_path= html_file_path.parent.joinpath(html_file_path.stem+".bibtex")

        #collect bibtexentries and remove None entries
        references=set([ el for el in self.bibtex_entries() if el is not None])
        if len(references)!=0:
            #bibtexc.entry_list_to_file(bibtex_file_path, references, format_str="BibTeX")
            bibtexc.entry_list_to_file(str(bibtex_file_path), references, format_str="plain")
    
        #collect matplotlib figures and plot them 
        figure_elements=self.matplotlib_figure_elements()
        for fig_el in figure_elements:
            #plt.show(fig_el.fig)
#            plt.rc('text', usetex=True)
            plt.rc('font', family='serif')
            file_path= html_file_path.parent.joinpath(fig_el.label+".svg")
            file_name=str(file_path)
            #file_name=os.path.join(os.path.dirname(html_file_name), fig_el.label+".svg")
            fig_el.fig.savefig(file_name, transparent=fig_el.transparent)
            plt.close(fig_el.fig)

        #collect sub_pages and write them 
        for sub_page in self.sub_pages():
            dir_path=html_file_path.parent
            sub_dir_path=dir_path.joinpath(sub_page.label)
            sub_dir_path.mkdir(exist_ok=True,parents=True)
            if sub_page.target_format=="html":
                outputFilePath=str(sub_dir_path.joinpath(LinkedSubPage.output_file_name()+".html"))
                sub_page.contentRel.write_pandoc_html(outputFilePath,csl_file_path,css_file_path)

        self.write_pandoc_markdown(md_file_path)   
        cmd = ["pandoc"]
        cmd += [str(md_file_path),"-s","--mathjax", "-o", html_file_name]        
        #cmd += ["--metadata=title:Test"]
        if len(references)!=0:
            cmd += ["--filter=pandoc-citeproc", "--bibliography="+str(bibtex_file_path)]
        if css_file_path is not None : 
            cmd += ["-c", str(css_file_path.absolute())]

        if csl_file_path is not None:
            cmd += ["--csl", str(csl_file_path)]
        if slide_show: cmd += ["-t", "slidy"]
            # "slidy" can be changed to: "s5", "slideous", "dzslides", or "revealjs". 
            # For generating a beamer, we'll need: (["pandoc","-t","beamer","--mathjax",md_file,"-o","pdf"]), 
            # where md_file should have TeX math embedded.

        try:
            subprocess.check_call(["rm","-rf", str(html_file_path)])
            #print(" ".join(cmd))
            
            subprocess.check_output(cmd)
    
            # copy css file

            copy_cmd = ["cp"]
            copy_cmd += [str(css_file_path)]
            dn = str(html_file_path.parent)
            copy_cmd += [dn]

            # comment in if copying buttondown.css is needed
            subprocess.check_call(copy_cmd)

        except subprocess.CalledProcessError as e:
           out=e.output
            #print(out)
        
        
   # def create_pandoc_dir(self,csl_file_path=None , css_file_path= None, slide_show = False):
   #     if csl_file_path is not None:
   #         csl_file_path= gv.resources_path.joinpath('apa.csl')
   #     if not css_file_name:
   #         css_file_name = gv.resources_path.joinpath('buttondown.css')

   #     dir_path=Path(dir_name) 
   #     if not dir_path.exists():
   #         dir_path.mkdir(parents=True)
   #     trunk = "Report" 
   #     html_path=dir_path.joinpath(trunk+".html")
   #     html_file_name=html_path.as_posix()
   #     md_file_name = os.path.join(os.path.dirname(html_file_name), trunk + ".md")
   #     bibtex_file_name = os.path.join(os.path.dirname(html_file_name), trunk + ".bibtex")

   #     #collect bibtexentries
   #     references=self.bibtex_entries()
#  #      bibtexc.entry_list_to_file(bibtex_file_name, references, format_str="BibTeX")
   #     bibtexc.entry_list_to_file(bibtex_file_name, references, format_str="plain")

   #     #collect matplotlib figures and plot them 
   #     figure_elements=self.matplotlib_figure_elements()
   #     for fig_el in figure_elements:
   #         plt.rc('text', usetex=True)
   #         plt.rc('font', family='serif')
   #         fig_el.fig.savefig(os.path.join(os.path.dirname(html_file_name), fig_el.label+".svg"), transparent=fig_el.transparent)
   #         plt.close(fig_el.fig)

   #     self.write_pandoc_markdown(md_file_name)   
   #     cmd = ["pandoc"]
   #     cmd += [md_file_name,"-s","--mathjax", "-o", html_file_name]        
   #     cmd += ["--filter=pandoc-citeproc", "--bibliography="+bibtex_file_name]
   #     if css_file_name: 
   #         rel_css_folder = relpath(dirname(css_file_name), dirname(html_file_name))
   #         rel_css_file_name = os.path.join(rel_css_folder, os.path.split(css_file_name)[1])

   #         # use css from this folder
   #         rel_css_file_name = 'buttondown.css'

   #         cmd += ["-c", rel_css_file_name]

   #     if csl_file_name: cmd += ["--csl", csl_file_name]
   #     if slide_show: cmd += ["-t", "slidy"]
   #         # "slidy" can be changed to: "s5", "slideous", "dzslides", or "revealjs". 
   #         # For generating a beamer, we'll need: (["pandoc","-t","beamer","--mathjax",md_file,"-o","pdf"]), 
   #         # where md_file should have TeX math embedded.

   #     try:
   #         subprocess.check_call(["rm","-rf", html_file_name])
   #         subprocess.check_output(cmd)
   #         #print(cmd)

   #         # copy css file
   #         copy_cmd = ["cp"]
   #         copy_cmd += [css_file_name]
   #         copy_cmd += [dir_path.as_posix()]
   #         # comment in if copying buttondown.css is needed
   #         subprocess.check_call(copy_cmd)

   #     except subprocess.CalledProcessError as e:
   #        out=e.output
   #         #print(out)
        
        
    def write_pandoc_markdown(self, output_md_path):
        # template_file="report_template_html.template"
        Text=self.pandoc_markdown()
        with output_md_path.open("w") as f:
            f.write(Text)

##########################################
class AtomicReportElementList(ReportElementList):
    def pandoc_markdown_string(self):
        return(self[0].pandoc_markdown_string()) 


##########################################
class Text(AtomicReportElementList):        
    def __init__(self,template_string,**kws):
        atom=TextElement(template_string,**kws)
        super().__init__([atom])

class TextElement():
    def __init__(self,template_string,**kws):
        self.template_string=template_string
        self.kws=kws
    
    def pandoc_markdown_string(self):
        # in the template creation we do not allow 
        # positional arguments although Markdown template
        # admits (exactly) one position argument

        # !!! check if there is anything to print ???
#        if self.template_string:
        t=MarkdownTemplate(self.template_string).substitute(**self.kws)
#        else:
#            t = ""

        return(t)

##########################################
class Header(AtomicReportElementList):        
    def __init__(self,template_string,level,**kws):
        atom=HeaderElement(template_string,level,**kws)
        super().__init__([atom])

class HeaderElement(TextElement):        

    def __init__(self,template_string,level,**kws):
        super().__init__(template_string,**kws)
        self.level=level

    def pandoc_markdown_string(self):
        if self.level>6:
            raise(Exception("In pandoc markdown only 6 levels for headers are allowed"))
        return("\n"+"#"*self.level+" "+super().pandoc_markdown_string()+"\n")




##########################################

class Meta(AtomicReportElementList):
    #def __init__(self, long_name, name, version):
    def __init__(self, key_dict):
        self.key_dict=key_dict
        

        dict_string="\n".join([
            str(key) + ": " + str(val) for key, val in key_dict.items()
        ])
        t=TextElement(remove_indentation("""\
                 --- 
                 ${dict_string} 
                 ---
                 """
        ),dict_string=dict_string)


        super().__init__([t])

##########################################
class EmptyLine(AtomicReportElementList):
    def __init__(self):
        atom=EmptyLineElement()
        super().__init__([atom])

class EmptyLineElement(TextElement):
    def __init__(self):
        pass
        
    def pandoc_markdown_string(self):
        return "\n" 
##########################################
class Newline(AtomicReportElementList):
    def __init__(self):
        atom=NewlineElement()
        super().__init__([atom])

class NewlineElement(TextElement):
    def __init__(self):
        pass
        
    def pandoc_markdown_string(self):
        return "  " #pandoc breaks a line after two or more spaces
##########################################
class MatplotlibFigure(AtomicReportElementList):
    def __init__(self, fig, label,caption_text = '', show_label = True, transparent = False):
        atom=MatplotlibFigureElement(fig,label, caption_text=caption_text, show_label=show_label, transparent=transparent)
        super().__init__([atom])

class MatplotlibFigureElement(TextElement):
    def __init__(self, fig, label, caption_text = '', show_label = True, transparent = False):
        self.fig=fig
        self.label=label
        self.caption_text=caption_text
        self.show_label = show_label
        self.transparent = transparent
    
    def pandoc_markdown_string(self):
        if self.show_label:
            # fixme mm 15.05.2018 looks like html which we do not want to see in
            # the markdown string
            t=Template(remove_indentation("""\n<br>
            <center>
            ![$l]($l.svg)<br>**$l:** *$c*<br>
            </center>
            """))
            return(t.substitute(c=self.caption_text,l=self.label))
        else:
            t=Template(remove_indentation("""\n<br>
            <center>
            ![$l]($l.svg)
            </center>
            """))
            return(t.substitute(l=self.label))

##########################################
class LinkedSubPage(AtomicReportElementList):
    @classmethod
    def output_file_name(cls):
        return "Report"

    def __init__(self, contentRel, label, link_text,target_format):
        atom=LinkedSubPageElement(contentRel,label,link_text,target_format)
        super().__init__([atom])

class LinkedSubPageElement(TextElement):
    def __init__(self, contentRel, label, link_text,target_format):
        self.contentRel=contentRel
        self.label=label
        self.link_text=link_text
        self.target_format=target_format
    
    def pandoc_markdown_string(self):
        t=Template("[${text}](${path_str})")
        return t.substitute(
                text=self.link_text,
                path_str=str(Path(self.label).joinpath(LinkedSubPage.output_file_name()+"."+self.target_format)))


##########################################
class Link(AtomicReportElementList):
    def __init__(self, text, target):
        atom=LinkElement(text,target)
        super().__init__([atom])

class LinkElement(TextElement):
    def __init__(self, text, target):
        self.text = text
        self.target = target
    
    def pandoc_markdown_string(self):
        return "[" + self.text +"](" + self.target +")"

##########################################
class Citation(AtomicReportElementList):
    def __init__(self, bibtex_entry, parentheses=True):
        atom=CitationElement(bibtex_entry,parentheses)
        super().__init__([atom])

class CitationElement(TextElement):
    def __init__(self, bibtex_entry, parentheses=True):
        self.bibtex_entry = bibtex_entry
        self.parentheses = parentheses
    
    def pandoc_markdown_string(self):
        if self.bibtex_entry:
            if self.parentheses:
                return "[@" + self.bibtex_entry.key + "]"
            else:
                return "@" + self.bibtex_entry.key
        else:
            return ""

##########################################
class Math(AtomicReportElementList):        
    def __init__(self,template_string,**kws):
        atom=MathElement(template_string,**kws)
        super().__init__([atom])

class MathElement(TextElement):        
    def pandoc_markdown_string(self):
        pmds = super().pandoc_markdown_string().replace("\\leq", "{\leq}")
        pmds = pmds.replace("\\geq", "{\geq}")
#        return("$"+super().pandoc_markdown_string()+"$")
        return("$"+pmds+"$")
        
        
##########################################
class TableRow(ReportElementList):
    def __init__(self,ListOfObjects):
        # we check if the list we got contains only ReportElements
        for obj in ListOfObjects:
            if not(isinstance(obj,TextElement) or isinstance(obj,ReportElementList) ):
                raise Exception("obj :"+str(obj)+" must be either of type TextElement or ReportElementList but was of type: "+str(type(obj)))
        super().__init__(ListOfObjects)
            
        self.ListOfObjects= ListOfObjects
    
    def pandoc_markdown_string(self):
        substituted_templates=[ob.pandoc_markdown()  for ob in self]
        if self.ncol()==1:
            return "|"+substituted_templates[0]+"|"
        else:
            return("|".join(substituted_templates))

    def ncol(self):
        return(len(self))
    
        
##########################################
class Table(ReportElementList):
    def __init__(self,name,headers_row,column_formats=None):
        super().__init__([])
        self.column_formats=column_formats
        self.name=name
        self.append(headers_row)
    def add_row(self,row):
        self.append(row)
        

    def pandoc_markdown_string(self):
        # translate the alingnment from (r)ight (l)eft (d)efault (c)center to the pipe_tables format used by pandoc
        d={"r":"-----:","l":":-----","d":"------","c":":-----:"}
        pandoc_format_strings=[d[fs] for fs in self.column_formats]
        if len(pandoc_format_strings)==1:
            format_row="|"+pandoc_format_strings[0]+'|'
        else:
            format_row="|".join(pandoc_format_strings)
        
        # adding the header format and footer of the table in the right order    
        last_row="  Table: "+str(self.name)+"  \n"
        row_strings=[tr.pandoc_markdown_string() for tr in self]
        complete=["  \n"]+[row_strings[0]]+[format_row]+row_strings[1:]+[last_row]
        return("  \n".join(complete))

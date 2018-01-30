# vim:set ff=unix expandtab ts=4 sw=4:

import re as regexp 
import os
from pathlib import Path
import subprocess
from sympy import latex
from string import Template
from sympy.printing.mathml import mathml

def ml(ex):
    # insert multiplication symbol
    st = latex(ex, mul_symbol="dot")

    # delete whitespaces
    st = regexp.sub("\s+"," ", st)
    st = regexp.sub("\s*\\\\", "\\\\", st)
    return(st) 


class MarkdownTemplate(Template):
     def substitute(self, *args, **kws):
         if len(args) > 1:
             raise TypeError('Too many positional arguments')
         if not args:
              mapping = kws
         elif kws:
              mapping = _multimap(kws, args[0])
         else:
              mapping = args[0]
         # Helper function for .sub()
         def convert(mo):
             # Check the most common path first.
             named = mo.group('named') or mo.group('braced')
             if named is not None:
                 if issubclass(type(mapping[named]),str):
                    val=mapping[named]

                    # replace $x_yz$ by $x_{yz}$
                    # do not replace $x_{y}$
                    pattern = r"\$(?P<var>(.*?))_(?!{)(?P<subsc>(.*?))\$"
                    val = regexp.sub(pattern, "$\g<var>_{\g<subsc>}$", val)

                 else:
                    val = ml(mapping[named])
                 # We use this idiom instead of str() because the latter will
                 # fail if val is a Unicode containing non-ASCII characters.
                 return '%s' % (val,)
             if mo.group('escaped') is not None:
                return self.delimiter
             if mo.group('invalid') is not None:
                 self._invalid(mo)
             raise ValueError('Unrecognized named group in pattern', self.pattern)
         return self.pattern.sub(convert, self.template)

class BGCmarkdown:
    def __init__(self,dir,filenameTrunk):
        self.dir=dir
        self.md=filenameTrunk+".md"
        self.html=filenameTrunk+".html"
        self.pdf=filenameTrunk+".pdf"
        self.textParts=[]
        self.yaml=filenameTrunk+"Head.yaml"
        self.YamlHead=[]
        self.ptemplate="template"
        self.customTemplate=[]

    @classmethod 
    def text(self,tString,*args,**kws):
        t=MarkdownTemplate(tString).substitute(*args,**kws)+" "
        return(t)

    def addText(self,tString,*args,**kws):
        t=BGCmarkdown.text(tString,*args,**kws)
        self.textParts.append(t)

    def printParts(self):
        return("".join(self.textParts))

    def dmath(self,mathString,*args,**kws):
        t=MarkdownTemplate(mathString).substitute(*args,**kws)
        return("\n"+t+"\n")

    def add_dmath(self,mathString,*args,**kws):
        self.textParts.append(self.dmath(mathString,*args,**kws))

    def addTable(self,name,head1,head2,Row):
        t="\n"+head1+"|"+head2+"\n:-----:|:-----\n"+Row+"\n Table: "+name+"\n"
        self.textParts.append(t)
    
    def addPandocTemplate(self,tString):
        self.customTemplate.append(tString)

    def returnPandocTemplate(self):
        return("".join(self.customTemplate))

    def addYamlHead(self,tString,*args,**kws):
        t=BGCmarkdown.text(tString,*args,**kws)
        self.YamlHead.append(t)

    def returnYamlHead(self):
        return("".join(self.YamlHead))

    def write(self):
        orgdir=os.getcwd()
        dp=Path(self.dir)
        Text=self.printParts()
        Head=self.returnYamlHead()
        PandocTemplate=self.returnPandocTemplate()
        if not(dp.exists()):
            dp.mkdir()
        os.chdir(self.dir)
        try:
            f1=open(self.md,"w")
            f1.write(Text)
            f1.close()
            
            f2=open(self.yaml,"w")
            f2.write(Head)
            f2.close()

            f3=open(self.ptemplate,"w")
            f3.write(PandocTemplate)
            f3.close()

            subprocess.check_call(["rm","-rf", self.html])
            #out=subprocess.check_output(["pandoc","-s","--mathjax","--toc|--table-of-contents","-html5",self.md,"-o",self.html])
            out=subprocess.check_output(["pandoc","-s","--mathjax",self.md,"-o",self.html]),#"--template"
#pandoc file1.md -s --mathjax -o file.html
#        except subprocess.CalledProcessError as e:
#            out=e.output
#            print(out)
#            raise(LatexException(e))

            subprocess.check_call(["rm","-rf",self.pdf])
            out=subprocess.check_output(["pandoc","-s",self.md,"-o",self.pdf])
        except subprocess.CalledProcessError as e:
            out=e.output
            print(out)
#            raise(LatexException(e))


        finally: 
            os.chdir(orgdir)


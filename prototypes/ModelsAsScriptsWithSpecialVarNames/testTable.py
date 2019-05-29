from sympy import var,sqrt,pi,sin, sympify
from pathlib import Path
from bgc_md.ReportInfraStructure import Text, Math, Meta, ReportElementList, TableRow, Table, Header, Newline, Citation, MatplotlibFigure
from bgc_md.DescribedQuantity import DescribedQuantity
from sympy.physics.units import mass,time
from sympy.physics.units import Quantity 
from sympy.physics.units import year,day,second,minute
from sympy.physics.units import meter, kilogram
from sympy.physics.units.dimensions import dimsys_SI
from sympy.physics.units import convert_to

s=DescribedQuantity("s")
s.set_dimension(mass,"SI")
s=DescribedQuantity("s")
s.set_dimension(mass,"SI")
s.set_description("Soil carbon ")

l=DescribedQuantity("l")
l.set_dimension(mass,"SI")
l.set_description("Leaf carbon ")

k_s=DescribedQuantity("k_s")
k_s.set_dimension(mass/time,"SI")
k_s.set_description("Soil respiration rate")

k_l=DescribedQuantity("k_l")
k_l.set_dimension(mass/time,"SI")
k_l.set_description("Leaf respiration rate")

documented_identifiers=[k_s,k_l,l,s]

headers_row=TableRow([Text("abbreviation"),Text("name of second column")])
# and the formats as a list of strings
formats=["c","l"]
t=Table("first Table", headers_row,formats)
var("x")
expr=sqrt(2/x)
for di in documented_identifiers:
    #t.add_row(TableRow([Math("a=$a",a=expr),Math("b=$b",b=2*expr)]))
    t.add_row(TableRow([Math("a=$a",a=di.abbrev),Math("b=$b",b=2*expr)]))

res=t.pandoc_markdown()
target_dir_path=Path('.').joinpath('html')
target_dir_path.mkdir(parents=True,exist_ok=True)
targetFileName='Report.html'
t.write_pypandoc_html(target_dir_path.joinpath(targetFileName))

from pathlib import Path
from bgc_md.ReportInfraStructure import ReportElementList, Header, Math, Meta, Text, Citation, Table, TableRow, Newline, MatplotlibFigure
fn="template.py"
p=Path(fn)

with p.open() as f:
    code=f.read()
data=5
exec(code)    
# call the function
rel= template(data)
print(rel.pandoc_markdown())

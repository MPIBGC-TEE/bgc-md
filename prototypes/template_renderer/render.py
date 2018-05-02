from pathlib import Path
from bgc_md.ReportInfraStructure import ReportElementList, Header, Math, Meta, Text, Citation, Table, TableRow, Newline, MatplotlibFigure


def render(p,data):
    with p.open() as f:
        code=f.read()
    exec(code,globals(),locals())    
    # call the function
    func=locals()['template']
    rel= func.__call__(data)
    return rel

print(render(Path("template.py"),5).pandoc_markdown())
print(render(Path("nestedTemplate.py"),6).pandoc_markdown())

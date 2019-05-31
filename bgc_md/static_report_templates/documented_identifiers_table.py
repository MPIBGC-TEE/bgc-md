from typing import List
def template(documented_identifiers:List):
    from collections import OrderedDict
    from bgc_md.ReportInfraStructure import Text, Math, ReportElementList, TableRow, Table, Header, Newline
    rel=ReportElementList()

        
    headers_row=TableRow([Text("abbreviation"),Text("Dimension"),Text('Description')])
    # and the formats as a list of strings
    formats=["c","l","l"]
    t=Table("first Table", headers_row,formats)
    #var("x")
    #expr=sqrt(2/x)
    for di in documented_identifiers:
        #t.add_row(TableRow([Math("a=$a",a=expr),Math("b=$b",b=2*expr)]))
        t.add_row(TableRow([Math("a=$a",a=di.abbrev),Text("$b",b=di.dimension.args),Text("$b",b=di.description)]))
    rel+=t
    return rel

# the function name and signature:
# template(model_list) is a convention. It will be called in a 
# predefined environment by a higher order function.
# If you want to include another template call you can do so with a line
# rel+=render(Path("path/to/the/template.py"))

def template(model_list):
    rel=ReportElementList()
    header_row = TableRow([Text(""), Text("Model"),  Text("Source")])
    table_format = list("lcl")
    T = Table("Summary of the models in the database of Carbon Allocation in Vegetation models", header_row, table_format)
    for index, model in enumerate(model_list):
        l = [Text(model.name),Text("blub")]         
        l.append(Citation(model.bibtex_entry, parentheses=False))
        row = TableRow(l)
        T.add_row(row)
    
    rel+=T
    return(rel)


# the function name and signature:
# template(model_list) is a convention. It will be called in a 
# predefined environment by a higher order function.
# If you want to include another template call you can do so with a line
# rel+=render(Path("path/to/the/template.py"))

def template(paths,model_list):
    rel=ReportElementList()
    rel+= Meta({"title":"Overview"})
    #fixme:
    # get rid of "." by repairing the report element list 
    header_row = TableRow([ Text("Model"),  Text("Source")])
    table_format = list("ll")
    T = Table("Summary of the models in the database of Carbon Allocation in Vegetation models", header_row, table_format)
    for i,model in enumerate(model_list):
        target=model.name
        l = [
            Link(model.name,str(paths[i]))
        ]         
        l.append(Citation(model.bibtex_entry, parentheses=False))
        row = TableRow(l)
        T.add_row(row)
    
    rel+=T
    return(rel)


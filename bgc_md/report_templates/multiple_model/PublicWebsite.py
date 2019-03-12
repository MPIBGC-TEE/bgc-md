# the function name and signature:
# template(model_list) is a convention. It will be called in a 
# predefined environment by a higher order function.
# If you want to include another template call you can do so with a line
# rel+=render(Path("path/to/the/template.py"))

def template(model_list):
    rel=ReportElementList()
    rel+= Meta({"title":"Overview of Models in BGC-MD"})
    #fixme:
    # get rid of "." by repairing the report element list 
    header_row = TableRow([ Text("Model"),  Text("Source")])
    table_format = list("ll")
    T = Table("Summary of the models in the database", header_row, table_format)
    single_tp=defaults()['paths']['report_templates'].joinpath('single_model','index.py')
    for i,model in enumerate(model_list):

        modelRel=render(single_tp,model=model)
        l = [
            LinkedSubPage(modelRel,model.yaml_file_path.stem,model.name,"html")
        ]         
        l.append(Citation(model.bibtex_entry, parentheses=False))
        row = TableRow(l)
        T.add_row(row)
    
    rel+=T
    rel+=Header("References", 1)
    return(rel)


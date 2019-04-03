# the function name and signature:
# template(model_list) is a convention. It will be called in a 
# predefined environment by a higher order function.
# If you want to include another template call you can do so with a line
# rel+=render(Path("path/to/the/template.py"))
def template(model_list):
    from multiprocessing import Pool

    rel=ReportElementList()
    rel+= Meta({"title":"Overview"})
    #fixme:
    # get rid of "." by repairing the report element list 
    header_row = TableRow([ 
        Text("Model"), 
        Text("# Variables"), 
        Text("# Constants"), 
        Text("Structure"), 
        #Text("Right hand side of ODE"), 
        Text("Source")])
    #table_format = list("lccccc")
    table_format = list("lcccc")
    T = Table("Summary of the models in the database of Carbon Allocation in Vegetation models", header_row, table_format)
    #single_tp=defaults()['paths']['report_templates'].joinpath('single_model','MinimalSingleReport.py')
    single_tp=defaults()['paths']['report_templates'].joinpath('single_model','CompleteSingleModelReport.py')

    def func(model):
        modelRel=render(single_tp,model=model)
        l = [
            LinkedSubPage(modelRel,model.yaml_file_path.stem,model.name,"html")
        ]         
        l.append(Math("${v}",v=model.nr_variables, parentheses=False))
        l.append(Math("${v}",v=model.nr_parameters, parentheses=False))
        
        fv_fs_entry = Text(" ")
        for row_dic in model.df.rows_as_dictionary:
            if row_dic['name'] in ('f_v', 'f_s'):
                if 'exprs' in row_dic.keys() and row_dic['exprs']:
                    fv_fs_entry = exprs_to_element(row_dic['exprs'], model.symbols_by_type)
        l.append(fv_fs_entry)

        #l.append(Math("${eq}",eq=model.rhs, parentheses=False))
        if hasattr(model,'bibtex_entry'):
            l.append(Citation(model.bibtex_entry, parentheses=False))
        row = TableRow(l)
        return row

    #fixme mm 30.06 2018 
    # parallelize with pool.map
    # pool=Pool(processes=16)
    # rows=pool.map(func,model_list)
    # for row in rows:
    #    T.add_row(row)
    # does not work :Can't pickle local object 'template.<locals>.func'
    
    for i,model in enumerate(model_list):
        row=func(model)
        T.add_row(row)
    
    rel+=T
    # add the scatter plots and histograms from a different template
    rel+=Newline()
    rel+=render(
        defaults()["paths"]["report_templates"].joinpath('multiple_model',"ModelListPlots.py")
        ,model_list)

    return(rel)


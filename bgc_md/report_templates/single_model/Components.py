def template(model):
    sdp= defaults()["paths"]["report_templates"].joinpath("single_model")
    
    rel = render(sdp.joinpath("SectionVariablesTable.py"),model,section="components")
    return rel
#def template(model):
#    ps=model.parameter_sets
#    df=model.section_pandas_df("components")
#    # replace missing entries in description column with '-'
#    df["desc"].fillna(value='-',inplace=True) 
#    
#    header_row = TableRow(
#        [Text("Name")
#         ,Text("Description")
#         ,Text("Expressions")
#        ]
#    )
#    table_format = list("lll")
#    T = Table("Components", header_row, table_format)
#    for i in range(len(df)):
#        df_line=df.loc[i]
#        expr_string=df_line["exprs"]
#        if expr_string:
#            # fixme: with parsing first, we could use the evaluate=False option, probably. Would keep the order of the expressions.
#            #fixme: as long as we allow printing of the expression only by coming from a python mathematical expression, we cannot prevent sympy from rearranging terms (except for matrix multiplication)
#            # otherwise we would have to use something like py2tex to convert a python expression like 'f_s = I + A*C' to a latex string
#            # py2tex cannot deal with 'Matrix([[1,2], [3,4]])'
#            parts = expr_string.split("=",1)           
#            parts[0] = parts[0].strip()
#            parts[1] = parts[1].strip()
#            p1 = sympify(parts[0], locals=model.symbols_by_type)
#            p2 = sympify(parts[1], locals=model.symbols_by_type)
#
#            # this is a hybrid version that keeps 'f_s = I + A*C' in shape, but if 'Matrix(...)' comes into play, rearranging by sympify within the matrix cannot be prevented
#            # comment it out for a a clean version regarding use of ReportElementList, but with showing 
#            # 'f_s = A * C + I' instead
#            #try:    
#            #    p2 = py2tex_silent(parts[1]) 
#            #except TypeError:
#            #   pass
# 
#            subrel=(Math("$p1=$p2", p1=p1,p2=p2))
#        else:
#            subrel=Text("")
#        T.add_row(TableRow([
#            Math("$v",v=sympify(df_line["name"],locals=model.symbols_by_type))
#            ,Text(df_line["desc"])
#            ,subrel
#        ]))
#
#    rel=T
#    return rel

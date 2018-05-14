def template(model):
    ps=model.parameter_sets
    df=model.section_pandas_df("additional_variables")
    # replace missing entries  column with '-'
    df["unit"].fillna(value='-',inplace=True) 

    header_row = TableRow(
        [Text("Name")
         ,Text("Description")
         ,Text("Expressions")
         ,Text("Unit")
        ]
    )
    table_format = list("llcl")
    T = Table("Parameters", header_row, table_format)
    for i in range(len(df)):
        df_line=df.loc[i]
        expr_string=df_line["exprs"]
        if expr_string:
            parts = expr_string.split("=",1)
            parts[0] = parts[0].strip()
            parts[1] = parts[1].strip()
            p1 = sympify(parts[0], locals=model.symbols_by_type)
            p2 = sympify(parts[1], locals=model.symbols_by_type)
            subrel=Math("$p1,$p2",p1=p1,p2=p2)
        else:
            subrel=Text("")
        T.add_row(TableRow([
            Math(py2tex_silent(df_line["name"]))
            ,Text(df_line["desc"])
            ,subrel
            ,Math(df_line["unit"])
        ]))

    rel=T
    return rel

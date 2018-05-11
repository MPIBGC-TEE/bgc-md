def template(model):
    ps=model.parameter_sets
    df=model.section_pandas_df("parameters")

    header_row = TableRow(
        [Text("Name")
         ,Text("Description")
         ,Text("Unit")
        ]
    )
    table_format = list("lll")
    T = Table("Parameters", header_row, table_format)
    for i in range(len(df)):
        df_line=df.loc[i]
        if df_line["unit"]:
            u=Math((df_line["unit"]))
        else:
            u=Text("-")
        T.add_row(TableRow([
           Math(py2tex_silent(df_line["name"]))
            ,
            Text(df_line["desc"])
            ,
            u
        ]))

    rel=T
    return rel

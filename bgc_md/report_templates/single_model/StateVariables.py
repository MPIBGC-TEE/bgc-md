def template(model):
    df=model.section_pandas_df("state_variables")

    header_row = TableRow(
        [Text("Model")
         ,Text("Description")
         ,Text("Unit")
        ]
    )
    table_format = list("lllcl")
    T = Table("State Variables", header_row, table_format)
    for i in range(df.ndim):
        df_line=df.loc[i]
        T.add_row(TableRow([
             Text(df_line["name"])
            ,Text(df_line["desc"])
            ,Math(df_line["unit"])
        ]))
    rel=T
    return rel

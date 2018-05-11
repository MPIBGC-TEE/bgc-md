def template(model):
    df=model.section_pandas_df("state_variables")

    header_row = TableRow(
        [ Text("Name")
         ,Text("Description")
         ,Text("Unit")
        ]
    )
    table_format = list("lll")
    T = Table("State Variables", header_row, table_format)
    for i in range(len(df)):
        df_line=df.loc[i]
        T.add_row(TableRow([
             Math(df_line["name"])
            ,Text(df_line["desc"])
            ,Math(df_line["unit"])
        ]))
    rel=T
    return rel

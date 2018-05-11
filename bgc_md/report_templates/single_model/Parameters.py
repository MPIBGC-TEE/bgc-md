def template(model):
    ps=model.parameter_sets
    df=model.section_pandas_df("parameters")
    # replace missing entries in units column with '-'
    df["unit"].fillna(value='-',inplace=True) 
    
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
        T.add_row(TableRow([
           Math(py2tex_silent(df_line["name"]))
            ,Text(df_line["desc"])
            ,Math(df_line["unit"])
        ]))

    rel=T
    return rel

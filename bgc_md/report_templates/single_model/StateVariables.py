def template(model):
    df=model.section_pandas_df("state_variables")
    # replace missing entries  column with '-'
    if "unit" in list(df.columns):
        df["unit"].fillna(value='-',inplace=True) 

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
        if "unit" in list(df.columns):
            u=Math(df_line["unit"])
        else:
            u=Text("")
        T.add_row(TableRow([
             Math(df_line["name"])
            ,Text(df_line["desc"])
            ,u
        ]))
    rel=T
    return rel

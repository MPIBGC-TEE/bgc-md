def template(model):
    #ps=model.parameter_sets
    df=model.section_pandas_df("allocation_coefficients")
    # replace missing entries in units column with '-'
    #df["unit"].fillna(value='-',inplace=True) 
    rel=ReportElementList() 

    header_row = TableRow(
        [Text("Name")
         ,Text("Description")
         ,Text("Expressions")
        ]
    )
    table_format = list("lll")
    T = Table("Allocation Coefficients", header_row, table_format)
    for i in range(len(df)):
        df_line=df.loc[i]
        T.add_row(TableRow([
            Math("$v", v=sympify(df_line["name"], locals=model.symbols_by_type)),
           Text(df_line["desc"])
       ]))

    rel+=T
    return rel

from typing import List

def template(documented_identifiers:List,section=None):
    rel=ReportElementList()
    from collections import OrderedDict

    dic={'name':'Name','desc':'Description', 'exprs':'Expression', 'unit':'Unit' }   
    inv_dic={v:k for k,v in dic.items()}
    
    #ps=model.parameter_sets
    #if not(model.has_model_subsection(section)):
    #    return Text("The model section in the yaml file has no subsection: ${s}.",s=section )
    #df=model.section_pandas_df(section)
    #yaml_colnames=list(df.columns)
    ## replace missing entries  column with '-'
    ##df["unit"].fillna(value='-',inplace=True) 
    #target_cols=OrderedDict()
    #target_cols["Name"]="l"
    #target_cols["Description"]="l"
    #target_cols["Expression"]="c"
    #target_cols["Unit"]="l"
    #text_colnames= [k for k in target_cols.keys() if inv_dic[k] in yaml_colnames ]
    #used_yaml_colnames=[inv_dic[tc] for tc in text_colnames]
    #table_format = [target_cols[k] for k in text_colnames]
    #header_row=TableRow([Text(s) for s in text_colnames])
    #T = Table(section, header_row, table_format)
    #for i in range(len(df)):
    #    df_line=df.loc[i]
    #    d=dict()
    #    for cn in used_yaml_colnames: 
    #        string=df_line[cn]
    #        if cn=="name":
    #            d[cn]=Math("$v",v=sympify(string, locals=model.symbols_by_type))
    #        elif cn=="exprs":
    #            if string is not None:
    #                parts = string.split("=",1)
    #                parts[0] = parts[0].strip()
    #                parts[1] = parts[1].strip()
    #                p1 = sympify(parts[0], locals=model.symbols_by_type)
    #                p2 = sympify(parts[1], locals=model.symbols_by_type)
    #                d[cn]=Math("$p1=$p2",p1=p1,p2=p2)
    #            else:
    #                d[cn]=Text("-")
    #        elif cn=="unit":
    #            if string is not None:
    #                string = string.replace("*", "\cdot ")
    #                string = string.replace("^-1", "^{-1}")
    #                string = string.replace("^-2", "^{-2}")
    #                string = string.replace("^-3", "^{-3}")
    #                d[cn]=Math("$u",u=string)
    #            else:
    #                d[cn]=Text("-")
    #        elif cn=="desc":
    #            d[cn]=Text("$d",d=string)
    #        else:
    #            d[cn]=Text('-')
    #    row_list=[d[inv_dic[tn]] for tn in text_colnames]
    #    T.add_row(TableRow(row_list))
    #    
    #rel=T
    return rel

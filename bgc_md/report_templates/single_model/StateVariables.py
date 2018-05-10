def template(model):
    df=model.section_pandas_df("state_variables")
    rel=ReportElementList()


        #elif section_name == 'additional_variables':
        #    rel += Header(model.section_titles[section_name], 1)
        #    rel += Text("The following table contains the available information regarding this section:")
        #    rel += model.additional_variables_Table()
        #elif section_name == 'allocation_coefficients':
        #    rel += Header(model.section_titles[section_name], 1)
        #    rel += Text("The following table contains the available information regarding this section:")
        #    rel += model.allocation_coefficients_Table()
        #elif section_name == 'components':
        #    rel += Header(model.section_titles[section_name], 1)
        #    rel += Text("The following table contains the available information regarding this section:")
        #    rel += model.components_Table()
        #elif section_name == 'parameter_sets':
        #    # parameter_sets are treated completely differently
        #    pass
        #else:
        #    # custom section to be included in the report
        #    rel += Header(model.section_titles[section_name], 1)
        #    rel += Text("The following table contains the available information regarding this section:")
        #    rel += model.variables_Table_from_section(section_name, parameter_values = True)
    
    return rel
    
#def get_all_colnames(complete_dict, variables_sections):
#    colnames = set()
#    for sec in variables_sections:
#        section_dic = section_subdict(complete_dict, sec) # {'state_variables': [...]}
#        return get_all_colnames_of_section_dict(section_dic)
#        for sec_name, var_list in section_dic.items():
#            for var_dic in var_list:
#                # var_dic = {'C': {'exprs': 'C=...', 'desc': '...'}}
#                # or var_dic = 'C'
#                if type(var_dic) == builtins.dict:
#                    for var, props in var_dic.items():
#                        if props: # maybe var_dic = {'C': }
#                            for colname, value in props.items(): # ('desc', '...')
#                                colnames |= {colname}
#    return sorted(list(colnames))

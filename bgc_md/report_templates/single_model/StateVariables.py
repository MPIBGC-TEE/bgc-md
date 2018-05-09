def template(model):
    rel=ReportElementList()
    for section_name in model.sections:
        if section_name == 'state_variables':
            rel += Header(model.section_titles[section_name], 1)
            rel += Text("The following table contains the available information regarding this section:")
            rel += model.state_variables_Table()
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

def template(model):
    sdp= defaults()["paths"]["report_templates"].joinpath("single_model")
    
    rel = render(sdp.joinpath("SectionVariablesTable.py"),model,section="additional_variables")
    return rel

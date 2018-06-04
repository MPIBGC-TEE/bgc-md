def template(model):
    sdp= defaults()["paths"]["report_templates"].joinpath("single_model")
    rel = render(sdp.joinpath("SectionVariablesTable.py"),model,section="state_variables")
    return rel

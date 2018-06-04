def template(model):
    #fixme mm 15.05.2018:
    # this seems to work for soil models only since the Vegetation models 
    # do not have a parameter section but other sections instead

    sdp= defaults()["paths"]["report_templates"].joinpath("single_model")
    rel = render(sdp.joinpath("SectionVariablesTable.py"),model,section="parameters")
    return rel

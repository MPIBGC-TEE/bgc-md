
def template(model):
    sdp= defaults()["paths"]["report_templates"].joinpath("single_model")
    rel=render(sdp.joinpath("GeneralOverview.py"),model)
    rel+=render(sdp.joinpath("StateVariables.py"),model)
    

    return(rel)


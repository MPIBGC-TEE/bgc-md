
def template(model):
    sdp= defaults()["paths"]["report_templates"].joinpath("single_model")
    rel=ReportElementList()
   # rel+=render(sdp.joinpath("GeneralOverview.py"),model)
    rel+=render(sdp.joinpath("StateVariables.py"),model)
    if model.model_type=="soil_model":
        rel+=render(sdp.joinpath("SoilModelParameters.py"),model)

    #rel+=render(sdp.joinpath("AdditionalVariables.py"),model)
    rel+=render(sdp.joinpath("Components.py"),model)
    rel+=render(sdp.joinpath("ReservoirModel.py"),model)
    #rel+=render(sdp.joinpath("SteadyStates.py"),model)
    #rel+=render(sdp.joinpath("Simulations.py"),model)
    rel+=render(sdp.joinpath("RightHandSideOfODE.py"),model)
    

    return(rel)


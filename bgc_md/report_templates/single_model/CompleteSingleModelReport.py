
def template(model):
    sdp= defaults()["paths"]["report_templates"].joinpath("single_model")
    rel=ReportElementList()
    rel+=render(sdp.joinpath("GeneralOverview.py"),model)
    rel+=render(sdp.joinpath("StateVariables.py"),model)
    if model.model_type=="soil_model":
        rel+=render(sdp.joinpath("SoilModelParameters.py"),model)

    rel+=render(sdp.joinpath("AdditionalVariables.py"),model)
    rel+=render(sdp.joinpath("Components.py"),model)
    rel+=render(sdp.joinpath("ReservoirModel.py"),model)
    rel+=render(sdp.joinpath("Simulations.py"),model)
    rel+=render(sdp.joinpath("SteadyStateFormulas.py"),model)
    rel+=render(sdp.joinpath("SteadyStateValues.py"), model)
    rel+=render(sdp.joinpath("TransientMeanAges.py"), model)
#    rel+=render(sdp.joinpath("TransientSystemAgeDensity3d.py"), model)
    
    rel+=Header("References", 2)

    return(rel)


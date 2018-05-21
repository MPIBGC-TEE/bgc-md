def template(model):
    sdp= defaults()["paths"]["report_templates"].joinpath("single_model")
    rel=ReportElementList()
    rel+=render(sdp.joinpath("StatevariablesAsFunctionsOfTime.py"),model)
    rel+=render(sdp.joinpath("PhasePlanePlots.py"),model)
    rel+=render(sdp.joinpath("Fluxes.py"),model)
######################################################################
    return rel

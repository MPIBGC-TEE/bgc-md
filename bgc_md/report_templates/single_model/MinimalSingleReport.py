
def template(model):
    rel=ReportElementList()
    sdp= defaults()["paths"]["report_templates"].joinpath("single_model")
    
    if model.long_name:
        t=Template("\'Report of the model: $long_name ($name), version: $version\'").substitute(
            long_name=model.long_name
            ,name=model.name 
            ,version=model.version)
    else:
        t=Template("\'Report of the model: $name, version: $version\'").substitute( name=model.name ,version=model.version)
    #rel=ReportElementList()
    rel+= Meta({"title":t})
    #fixme mm 01.07
    ###link broken
    ###rel+= Link("yaml_file",str(model.yaml_file_path))
    rel+=Newline()
    rel+=Newline()
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
    rel+=render(sdp.joinpath("TransientSystemAgeDensity3d.py"), model)
    
    rel+=Header("References", 2)

    return(rel)



def template(model):
    rel=ReportElementList()
    sdp= defaults()["paths"]["report_templates"].joinpath("single_model")
    
    if model.long_name:
        t=Template("\' $long_name ($name), version: $version\'").substitute(
            long_name=model.long_name
            ,name=model.name 
            ,version=model.version)
    else:
        t=Template("\' $name, version: $version\'").substitute( name=model.name ,version=model.version)
    #rel=ReportElementList()
    rel+= Meta({"title":t})
    #fixme mm 01.07
    ###link broken
    ###rel+= Link("yaml_file",str(model.yaml_file_path))
    rel+=Newline()
    rel+=Newline()
    rel+=render(sdp.joinpath("PublicOverview.py"),model)
    rel+=Header("Model description",1)
    rel+=Header("State variables", 2)
    rel+=render(sdp.joinpath("StateVariables.py"),model)
    #rel+=Header("Additional variables", 2)
    #rel+=render(sdp.joinpath("AdditionalVariables.py"),model)
    rel+=Header("Components of the compartmental system",2)
    rel+=render(sdp.joinpath("Components.py"),model)
    rel+=render(sdp.joinpath("ReservoirModel.py"),model)
    #rel+=render(sdp.joinpath("Simulations.py"),model)
    rel+=render(sdp.joinpath("SteadyStateFormulas.py"),model)
    #rel+=render(sdp.joinpath("SteadyStateValues.py"), model)
    
    rel+=Header("References", 1)

    return(rel)


from bgc_md.ReportInfraStructure import ReportElementList, Header, Math, Meta, Text, Citation, Table, TableRow, Newline,EmptyLine,MatplotlibFigure, Link, LinkedSubPage, exprs_to_element, PlotlyFigure
from bgc_md.reports import defaults,render_if_possible

def template(name_space):
    rel=ReportElementList()
    sdp= defaults()["paths"]["static_report_templates"].joinpath("single_model")
    rel+=render_if_possible(sdp.joinpath("GeneralOverview.py"),name_space)
    #rel+=render(sdp.joinpath("StateVariables.py"),name_space)
    #if name_space.name_space_type=="soil_name_space":
    #    rel+=render(sdp.joinpath("SoilModelParameters.py"),name_space)

    #rel+=render(sdp.joinpath("AdditionalVariables.py"),name_space)
    #rel+=render(sdp.joinpath("Components.py"),name_space)
    #rel+=render(sdp.joinpath("ReservoirModel.py"),name_space)
    #rel+=render(sdp.joinpath("Simulations.py"),name_space)
    #rel+=render(sdp.joinpath("SteadyStateFormulas.py"),name_space)
    #rel+=render(sdp.joinpath("SteadyStateValues.py"), name_space)
    #rel+=render(sdp.joinpath("TransientMeanAges.py"), name_space)
    #rel+=render(sdp.joinpath("TransientSystemAgeDensity3d.py"), name_space)
    #
    #rel+=Header("References", 2)

    return(rel)


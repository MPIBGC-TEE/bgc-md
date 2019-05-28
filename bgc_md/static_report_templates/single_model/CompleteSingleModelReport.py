from bgc_md.ReportInfraStructure import ReportElementList, Header, Math, Meta, Text, Citation, Table, TableRow, Newline,EmptyLine,MatplotlibFigure, Link, LinkedSubPage, exprs_to_element, PlotlyFigure
from bgc_md.reports import defaults,render2

from bgc_md.resolve.helpers import  get_bgc,is_computable_bgc

def template(model_id):
    rel=ReportElementList()
    sdp= defaults()["paths"]["static_report_templates"].joinpath("single_model")
    rel+=render2(sdp.joinpath("GeneralOverview.py"),model_id)
    #rel+=render(sdp.joinpath("StateVariables.py"),model_id)
    #if model.model_id_type=="soil_model_id":
    #    rel+=render(sdp.joinpath("SoilModelParameters.py"),model_id)

    #rel+=render(sdp.joinpath("AdditionalVariables.py"),model_id)
    if is_computable_bgc('documented_identifiers_table',model_id):
        rel+= get_bgc("documented_identifiers_table",model_id)
    #rel+=render(sdp.joinpath("Components.py"),model_id)
    #rel+=render(sdp.joinpath("ReservoirModel.py"),model_id)
    #rel+=render(sdp.joinpath("Simulations.py"),model_id)
    #rel+=render(sdp.joinpath("SteadyStateFormulas.py"),model_id)
    #rel+=render(sdp.joinpath("SteadyStateValues.py"), model_id)
    #rel+=render(sdp.joinpath("TransientMeanAges.py"), model_id)
    #rel+=render(sdp.joinpath("TransientSystemAgeDensity3d.py"), model_id)
    #
    #rel+=Header("References", 2)

    return(rel)


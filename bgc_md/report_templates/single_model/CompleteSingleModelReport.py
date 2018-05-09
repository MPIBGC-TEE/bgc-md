
def template(model):
    
    sub_template_path=defaults()["paths"]["report_templates"].joinpath("single_model","GeneralOverview.py")
    rel=render(sub_template_path,model)
    sub_template_path=defaults()["paths"]["report_templates"].joinpath("single_model","StateVariables.py")
    rel+=render(sub_template_path,model)

    return(rel)


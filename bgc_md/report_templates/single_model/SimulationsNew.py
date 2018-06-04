def template(model):
    sdp= defaults()["paths"]["report_templates"].joinpath("model_run")
    # include model simulations
    rel = EmptyLine()
    rel += Header("Model simulations", 2)
    #if reservoir_model and model.model_runs:

    fontsize = 20

    model_runs = model.model_runs
    for i, mr in enumerate(model_runs):
        n = mr.nr_pools

        comb = model.model_run_combinations[i]
        if comb['par_set'] is not None:
            par_set_names = comb['par_set']['values']
            par_set = {model.symbols_by_type[name]: value for name, value in par_set_names.items()}
        else:
            par_set=dict()

        run_data_str_basis = "Initial values: " + comb['IV']['table_head']
        
        if comb['par_set'] is not None:
            run_data_str_basis += ", Parameter set: " + comb['par_set']['table_head']

        rel+=render(sdp.joinpath("StatevariablesAsFunctionsOfTime.py"),mr)
######################################################################
    return rel

def template(model):
    # include model simulations
    rel = EmptyLine()
    rel += Header("Phaseplane plots", 2)
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
            # if we do not have free variables we do not need a parameter se
            par_set=dict()

        run_data_str_basis = "Initial values: " + comb['IV']['table_head']
        
        if comb['par_set'] is not None:
            run_data_str_basis += ", Parameter set: " + comb['par_set']['table_head']

        
        ######################################################################3 
        # plot phase planes
        fig = plt.figure(figsize=(3*n,3*n), tight_layout=True)
#        mr.plot_phase_planes(fig, units)
        mr.plot_phase_planes(fig, fontsize=fontsize)

        label = "Model run " + str(i+1) + " - phase planes"
        run_data_str = run_data_str_basis + ", Start: " + str(comb['run_time']['start'])
        run_data_str += ", End: " + str(comb['run_time']['end'])
        run_data_str += ", Time step: " + str(comb['run_time']['step_size'])
        rel += MatplotlibFigure(fig, label, run_data_str)

    return rel

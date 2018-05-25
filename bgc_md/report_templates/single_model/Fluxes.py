def template(model):
    # include model simulations
    rel = EmptyLine()
    rel += Header("Fluxes", 2)
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

        # plot solutions

       # plot external input 
        fs=mr.nr_pools*3
        fig1 = plt.figure(figsize=(7,fs), tight_layout=True)
        label = "Model run " + str(i+1) + " - external input"
        mr.plot_external_input_fluxes(fig1)
        rel += MatplotlibFigure(fig1, label, run_data_str_basis)
       
       # plot external output fluxes
        fig2 = plt.figure(figsize=(7,fs), tight_layout=True)
        label = "Model run " + str(i+1) + " - external output"
        mr.plot_external_output_fluxes(fig2)
        rel += MatplotlibFigure(fig2, label, run_data_str_basis)

       # plot internal fluxes
        fig3 = plt.figure(figsize=(7,fs), tight_layout=True)
        label = "Model run " + str(i+1) + " - internal fluxes"
        mr.plot_internal_fluxes(fig3)
        rel += MatplotlibFigure(fig3, label, run_data_str_basis)
    return rel

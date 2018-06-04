def template(model):
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

        # plot solutions
        fig = plt.figure(figsize=(7,3*len(model.state_vector["expr"])), tight_layout=True)          
        #time_unit = model.df.get_by_cond('unit', 'name', model.time_symbol['name'])
        #units = [model.df.get_by_cond('unit', 'name', sv.name) for sv in model.state_vector['expr']]
        #mr.plot_sols(fig, time_unit, units)
        mr.plot_solutions(fig, fontsize=fontsize)
# fimm-30.01.2018            mr.plot_sols(fig)

        label = "Model run " + str(i+1) + " - solutions"
        run_data_str = run_data_str_basis + ", Time step: " + str(comb['run_time']['step_size'])
        rel += MatplotlibFigure(fig, label, run_data_str)
        
    return rel

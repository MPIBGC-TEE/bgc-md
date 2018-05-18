def template(model):
    # include model simulations
    rel = EmptyLine()
    rel += Header("Model simulations", 2)
    #if reservoir_model and model.model_runs:

    fontsize = 20

    model_runs = model.model_runs
    for i, mr in enumerate(model_runs):
        n = mr.nr_pools
        lmr = mr.linearize()

        comb = model.model_run_combinations[i]
        par_set = comb['par_set']['values']

        run_data_str_basis = "Initial values: " + comb['IV']['table_head']
        run_data_str_basis += ", Parameter set: " + comb['par_set']['table_head']

        start_age_moments = lmr.compute_start_age_moments(1)
        first_moment = lmr.system_age_moment(1, start_age_moments)

        fig = plt.figure(figsize=(7,3*(n+1)), tight_layout=True)
        lmr.plot_mean_ages(fig, start_age_moments)
        label = "Model run " + str(i+1) + " - mean ages"
        run_data_str = run_data_str_basis + ", Time step: " + str(comb['run_time']['step_size'])
        rel += MatplotlibFigure(fig, label, run_data_str)
        
    return rel


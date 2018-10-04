def template(model):
    from CompartmentalSystems.start_distributions import start_age_moments_from_zero_initial_content
    # include mean ages
    fontsize = 20
    rel = EmptyLine()
    rel += Header("Mean ages", 2)

    rel +=Text("To compute the moments we need a start_age distribution.  This distribution can be chosen arbitrarily by the user or contributor of the yaml file and should in this case be defined in the model run data.  If the model run data do not contain age distributions, we can compute some distributions for special situations")
    rel +=Header("Zero age for the whole initial mass",3) 
    rel +=Text("We assume that the contents of all pools (as described by the start values of a model run combination are zero")  

    model_runs = model.model_runs
    for i, mr in enumerate(model_runs):
        n = mr.nr_pools
        lmr = mr.linearize()

        comb = model.model_run_combinations[i]
        par_set = comb['par_set']['values']

        run_data_str_basis = "Initial values: " + comb['IV']['table_head']
        run_data_str_basis += ", Parameter set: " + comb['par_set']['table_head']

        start_age_moments = start_age_moments_from_zero_initial_content(model.reservoir_model,1)

        first_moment = lmr.system_age_moment(1, start_age_moments)

        fig = plt.figure(figsize=(7,3*(n+1)), tight_layout=True)
        lmr.plot_mean_ages(fig, start_age_moments)
        label = "Model run " + str(i+1) + " - mean ages"
        run_data_str = run_data_str_basis + ", Time step: " + str(comb['run_time']['step_size'])
        rel += MatplotlibFigure(fig, label, run_data_str)

    rel +=Header("Steady state start age distribution ",3) 
    rel +=Text("In the general non autonomous case The model can be frozen at a time t_0. The resulting model is in general autonomous but nonlinear and might have fixed points. If fixedpoints can be found we can compute the age distribution that would have developed if the system had stayed in this equilibrium for infinite time. Note that any startvalues given in the model run data section will not influence this start distribution since it will use the equilibrium values if such can be found.")
    # fixme 08-21-2018
    # We have to implement the functionality to integrate python functions in the yaml file (or maybe later the directory of a model
    # since we have to substitute the functions before we can evalueate the Matrix B and vector u at time t0
    raise Exception("func_sets are not implemented yet") 
        
    return rel


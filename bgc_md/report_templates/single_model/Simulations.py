def template(model):
    # include model simulations
    rel = EmptyLine()
    rel += Header("Model simulations", 2)
    #if reservoir_model and model.model_runs:


    model_runs = model.model_runs
    for i, mr in enumerate(model_runs):
        comb = model.model_run_combinations[i]
        par_set = comb['par_set']['values']

        run_data_str_basis = "Initial values: " + comb['IV']['table_head']
        run_data_str_basis += ", Parameter set: " + comb['par_set']['table_head']

        # plot solutions
        fig = plt.figure(figsize=(7,3*len(model.state_vector["expr"])), tight_layout=True)          
        time_unit = model.df.get_by_cond('unit', 'name', model.time_symbol['name'])
        units = [model.df.get_by_cond('unit', 'name', sv.name) for sv in model.state_vector['expr']]
        #mr.plot_sols(fig, time_unit, units)
        mr.plot_solutions(fig )
# fimm-30.01.2018            mr.plot_sols(fig)

        label = "Model run " + str(i+1) + " - solutions"
        run_data_str = run_data_str_basis + ", Time step: " + str(comb['run_time']['step_size'])
        rel += MatplotlibFigure(fig, label, run_data_str)
        
        # plot phase planes
        fig = plt.figure(figsize=(3*len(model.state_vector["expr"]),7), tight_layout=True)
#        mr.plot_phase_planes(fig, units)
        mr.plot_phase_planes(fig)

        label = "Model run " + str(i+1) + " - phase planes"
        run_data_str = run_data_str_basis + ", Start: " + str(comb['run_time']['start'])
        run_data_str += ", End: " + str(comb['run_time']['end'])
        run_data_str += ", Time step: " + str(comb['run_time']['step_size'])
        rel += MatplotlibFigure(fig, label, run_data_str)

        # plot external input 
#        fig = plt.figure(figsize=(7,3), tight_layout=True)
#        label = "Model run " + str(i+1) + " - external input"
#        mr.plot_external_input_fluxes(fig)
#        rel += MatplotlibFigure(fig, label, run_data_str)

        # plot system-age distributions
        fig = plt.figure(figsize=(10,15), tight_layout=True)
#        fig = plt.figure(figsize=(6,6), tight_layout=True)
#        tsi=TimeStepIterator.from_ode_reservoir_model_run(mr)
        
#        age_dist_hist=TsTpMassFieldsPerPoolPerTimeStep.from_time_step_iterator(tsi)
#        print("Calculation done, creating plot.")
#        age_dist_hist.matrix_plot3d("plot_system_age_distributions_with_bins", fig, title="System age distribution", mr=mr)
#        print("Plot created.")
#        
#        label = "Model run " + str(i+1) + " - system-age-distributions"
#        
#        rel += MatplotlibFigure(fig, label, run_data_str_basis)
        #fig.show()
        #input()

    # include references
    rel += Text("\n")
    rel += Header("References", 1)
    return(rel)
    
######################################################################
    return rel

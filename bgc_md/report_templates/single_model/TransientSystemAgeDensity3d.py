def template(model):
    from LAPM.linear_autonomous_pool_model import LinearAutonomousPoolModel
    from CompartmentalSystems.start_distributions import start_age_distributions_from_zero_age_initial_content

    rel = EmptyLine()
    rel += Header("Age Density Evolution", 2)
    rel +=Text("""
    To compute the moments we need a start_age distribution.  
    This distribution can be chosen arbitrarily by the user.
    At the moment the yaml files do not contain startdistributions.
    The package CompartmentalSystems has a module "start_age_densities"  which contains functions to compute some distributions for special situations.
    In this template we use only the simplest ones.""")
    rel +=Header("Zero age for the whole initial mass",3) 
    rel +=Text("We assume that the contents of all pools (as described by the start values of a model run combination are zero")  
    srm=model.reservoir_model
    model_runs = model.model_runs
    for i, mr in enumerate(model_runs):
        n = mr.nr_pools
        lmr = mr.linearize()
        
        start_age_densities=start_age_distributions_from_zero_age_initial_content(srm,mr.start_values)
        lmr.times = np.linspace(0,5,101)
        nr_age_steps = 20
        age_stride = 1
        #time_stride = 10
        time_stride = 1

        #ages = np.linspace(lmr.times[0], lmr.times[-1], nr_age_steps)
        ages = lmr.times
        ages=np.linspace(0,0.1,101)
        p = lmr.pool_age_densities_func(start_age_densities)
        pool_age_densities = p(ages)
        system_age_density = lmr.system_age_density(pool_age_densities)

        title = 'System age density evolution'
        fig = lmr.plot_3d_density_plotly(
                    title,
                    #system_age_density,
                    pool_age_densities[1],
                    ages,
                    age_stride=age_stride,
                    time_stride=time_stride
                )

        label = "Model run " + str(i+1) + " - age density evolution"
        rel += PlotlyFigure(fig, label)

    return rel


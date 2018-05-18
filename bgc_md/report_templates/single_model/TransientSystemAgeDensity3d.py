def template(model):
    from LAPM.linear_autonomous_pool_model import LinearAutonomousPoolModel

    rel = EmptyLine()
    rel += Header("Age Density Evolution", 2)

    model_runs = model.model_runs
    for i, mr in enumerate(model_runs):
        n = mr.nr_pools
        lmr = mr.linearize()

        comb = model.model_run_combinations[i]
        par_set = comb['par_set']['values']

        run_data_str_basis = "Initial values: " + comb['IV']['table_head']
        run_data_str_basis += ", Parameter set: " + comb['par_set']['table_head']
        ##### load linear autonomous pool model in steady state #####

        B0 = Matrix(lmr.B(lmr.times[0]))
        u0 = Matrix(lmr.external_input_vector_func(cut_off=False)(0))
        print(B0)
        print(u0)
        # force purely numerical treatment of the LAPM
        # symbolic treatment would be too slow here
        LM = LinearAutonomousPoolModel(u0, B0, force_numerical=True)

        ## load equilibrium age densities ##

        # the start age densities are given as a function of age that returns
        # a vector of mass with that age
        def start_age_densities(a):
            # we need to convert from sympy data types to numpy data types
            res =  np.array(LM.a_density(a)).astype(np.float64).reshape((3,)) * start_values
            return res

    return rel


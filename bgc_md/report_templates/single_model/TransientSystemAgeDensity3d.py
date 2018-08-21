def template(model):
    from LAPM.linear_autonomous_pool_model import LinearAutonomousPoolModel

    rel = EmptyLine()
    rel += Header("Age Density Evolution", 2)
    rel +=Text("To compute the moments we need a start_age distribution.  This distribution can be chosen arbitrarily by the user or contributor of the yaml file and should in this case be defined in the model run data.  If the model run data do not contain age distributions, we can compute some distributions for special situations")
    rel +=Header("Zero age for the whole initial mass",3) 
    rel +=Text("We assume that the contents of all pools (as described by the start values of a model run combination are zero")  

    # fixme 08-21-2018
    # Fixed points known to the user should be added to the model description either symbolikcally to the model section of the yam file or )
    rel +=Header("Steady state start age distribution ",3) 
    rel +=Text("In the general non autonomous case The model can be frozen at a time t_0. The resulting model is in general autonomous but nonlinear and might have fixed points. If fixedpoints can be found we can compute the age distribution that would have developed if the system had stayed in this equilibrium for infinite time. Note that any startvalues given in the model run data section will not influence this start distribution since it will use the equilibrium values if such can be found.")
    # fixme 08-21-2018
    # We have to implement the functionality to integrate python functions in the yaml file (or maybe later the directory of a model
    # since we have to substitute the functions before we can evalueate the Matrix B and vector u at time t0
    raise Exception("func_sets are not implemented yet") 
    srm=model.reservoir_model
    u_sym=srm.external_inputs
    print(u_sym)
    B_sym=srm.compartmental_matrix
    print(B_sym)
    # we want B and u as python functions 
    #str_func_set = {str(key): val for key, val in func_set.items()}
    #cut_func_set = {key[:key.index('(')]: val 
    #    for key, val in str_func_set.items()}
    #
    #tup = tuple(X) + (t,)
    #u_par=u_sym.subs(parameter_set)
    #print(u_par)
    #u_func = lambdify(tup, u_par, modules=[cut_func_set, 'numpy'])
    tup = tuple(X) + (t,)
    tup = (t,) # for the linear case 
    u_func=numerical_function_from_expression(u_sym,tup,parameter_set,func_set)
    u_func(0)
    B_func=numerical_function_from_expression(B_sym,tup,parameter_set,func_set)
    B0=B_func(0)
    u0=u_func(0)
    if srm.has_fixed_points:
        # at the moment we raise an ex
    model_runs = model.model_runs
    for i, mr in enumerate(model_runs):
        n = mr.nr_pools
        lmr = mr.linearize()
        
#        # load or compute and save the state transition operator
#        # to save time

        # problem: where to save it? the template doesn't know about
        # the output folder
#        size = 1001        
#        try:
#            print('Loading state transition operator')
#            smr.load_state_transition_operator_cache(folder + '_sto.cache')
#        except FileNotFoundError:
#            print('Building state transition operator cache')
#            smr.build_state_transition_operator_cache(size = cache_size)
#            print('Saving state transition operator cache')
#            smr.save_state_transition_operator_cache(folder + '_sto.cache')
#        print('done')

        ##### load linear autonomous pool model in steady state #####
        # rhs = xi*T*N*C + u
        xi, T, N, C, u = lmr.model.xi_T_N_u_representation()

        # B = xi*T*N, plug in the steady-state initial contents
        B0 = (xi*T*N).subs(lmr.parameter_set)
        #B0 = B0.subs(sv_dict)
        u0 = u.subs(lmr.parameter_set)
#        B0 = Matrix(lmr.B(lmr.times[0]))
#        u_func = lmr.external_input_vector_func(cut_off=False)
#        Bs = [lmr.B(t) for t in lmr.times]
#        for B in Bs:
#            print(B,'\n')
#        u0 = Matrix(u_func(lmr.times[0]))
        
        # force purely numerical treatment of the LAPM
        # symbolic treatment would be too slow here
        LM = LinearAutonomousPoolModel(u0, B0, force_numerical=True)

        #print(lmr.solve()[0:2].sum(1))

        ## load equilibrium age densities ##

        # the start age densities are given as a function of age that returns
        # a vector of mass with that age
        start_values = lmr.start_values
        def start_age_densities(a):
            # we need to convert from sympy data types to numpy data types
            res = 0 * np.array(LM.a_density(a)).astype(np.float64).reshape((n,)) * start_values
            return res

        #lmr.times = np.linspace(0,2,3)
        nr_age_steps = 20
        age_stride = 1
        time_stride = 10

        ages = np.linspace(lmr.times[0], lmr.times[-1], nr_age_steps)
        #ages = lmr.times
        p = lmr.pool_age_densities_func(start_age_densities)
        pool_age_densities = p(ages)
        system_age_density = lmr.system_age_density(pool_age_densities)

        title = 'System age density evolution'
        fig = lmr.plot_3d_density_plotly(
                    title,
                    system_age_density,
                    #pool_age_densities[1],
                    ages,
                    age_stride=age_stride,
                    time_stride=time_stride
                )

        label = "Model run " + str(i+1) + " - age density evolution"
        rel += PlotlyFigure(fig, label)

    return rel


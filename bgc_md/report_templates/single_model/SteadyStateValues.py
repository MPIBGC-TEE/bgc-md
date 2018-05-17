def template(model):
    sdp= defaults()["paths"]["report_templates"].joinpath("single_model")
    
    srm = model.reservoir_model
    if srm is None:
        return ReportElementList()

    time_symbol = srm.time_symbol

    complete_parameter_sets = [par_set for par_set in model.parameter_sets if check_parameter_set_complete(par_set, model.state_vector, model.time_symbol, model.state_vector_derivative)]

#    complete_parameter_sets = model.parameter_sets
    if complete_parameter_sets:
        rel = Header("Steady states (potentially incomplete), according jacobian eigenvalues, damping ratio", 2)

    for par_set_big in complete_parameter_sets:
        par_set = par_set_big['values']
        header_str = "Parameter set: " + par_set_big['table_head']
        rel += Header(header_str, 3)

        steady_states = srm.steady_states(par_set)

        if steady_states:
            for ss_dict in steady_states:
                for sv in srm.state_variables:
                    if sv in ss_dict.keys():
                        rel += Math("$name = $value", name=sv, value=ss_dict[sv])
                        rel += EmptyLine()*2

                    rel += EmptyLine()
    
                    dic = par_set.copy()
    
                jacobian = model.jacobian().subs(dic)
                if jacobian.free_symbols == set():
                    evs = [complex(v) for v in jacobian.eigenvals().keys()]
                else:
                    evs = [v for v in jacobian.eigenvals().keys()]

                for i in range(len(evs)):
                    ev = evs[i]
                    
                    if jacobian.free_symbols == set():
                        if ev.imag == 0:
                            ev = ev.real
    
                        lamda_i = Symbol('lamda_'+ str(i+1))
                        rel += Math("$s: $v", s = lamda_i, v = "{:.5f}".format(ev)) + Newline()
        
                        if ev.imag != 0:                        
                            rho = -ev.real/np.sqrt(ev.real**2+ev.imag**2)
                            rel += Math("$s: $v", s = Symbol("rho_"+ str(i+1)), v = "{:-5f}".format(rho)) + Newline()
                    else:
                        lamda_i = Symbol('lamda_'+ str(i+1))
                        rel += Math("$s: $v", s = lamda_i, v = ev.evalf(4)) + Newline()
        
                    rel += EmptyLine()

                rel+=render(sdp.joinpath("SteadyStateTransitTimeDensityPlot.py"), srm, ss_dict, par_set) 

    return(rel)                        
    


def template(model):
    rel=ReportElementList()
    #fixme: suggested steady states  
    # check suggested steady states in the yaml file

    # try to calculate the steady states for ten seconds
    # after ten seconds stop it
    q = multiprocessing.Queue()
    def calc_steady_states(q):

        ss = solve(model.rhs, model.state_vector['expr'], dict=True)
        q.put(ss)

    p = multiprocessing.Process(target=calc_steady_states, args=(q,))
    p.start()
    p.join(10)
    if p.is_alive():
        p.terminate()
        p.join()
        steady_states = []
    else:
        steady_states = q.get()


    formal_steady_states = steady_states
    if formal_steady_states:
        rel += Header("Steady state formulas", 2)
        for ss in formal_steady_states:
            for sv_symbol in model.state_vector['expr']:
                if sv_symbol in ss.keys():
                    ss[sv_symbol] = simplify(ss[sv_symbol])
                else:
                    ss[sv_symbol] = sv_symbol

                rel += Math("$name = $value", name=sv_symbol, value=ss[sv_symbol]) + Newline()
            rel += Newline()
    # include parameter set information: steady states, eigenvalues, damping ratios
#    complete_parameter_sets = [par_set for par_set in model.parameter_sets if check_parameter_set_complete(par_set, model.state_vector, model.time_symbol, model.state_vector_derivative)]
    
    if model.time_symbol:
        time_symbol = model.time_symbol['symbol']
    else:
        time_symbol = None

    complete_parameter_sets = model.parameter_sets
    if formal_steady_states and complete_parameter_sets:
        rel += Text("\n")
        rel += Header("Steady states (potentially incomplete), according jacobian eigenvalues, damping ratio", 2)
        for par_set in complete_parameter_sets:
            header_str = "Parameter set: " + par_set['table_head']
            rel += Header(header_str, 3)

            rhs = model.rhs
            steady_states = solve(rhs.subs(par_set['values']), model.state_vector['expr'], dict=True)
            #steady_states = solve(rhs, model.state_vector['expr'], dict=True)
            for ss in steady_states:
                # check if steady state calculation could solve for all state variables
#                if len(ss) == len(model.state_vector['expr']):
                    ss_list = []
                    for sv_symbol in model.state_vector['expr']:
                        if sv_symbol in ss.keys():
                            ss_expr = ss[sv_symbol]
                        else:
                            ss_expr = sv_symbol

                        if time_symbol in ss_expr.free_symbols:
                            # take limit of time to infinity if steady state still depends on time
                            ss_expr = limit(ss_expr, time_symbol, oo)
                            rel += Text("\nTaken limit ") + Math("$sv($t)", sv=sv_symbol, t=time_symbol)
                            rel += Text(" for ") + Math("$t", t=time_symbol)
                            rel += Text(" to infinity.\n\n")
    
                        sv_name = key_from_dict_by_value(model.symbols_by_type, sv_symbol)
    
                        ss_list.append({'name': sv_name, 'symbol': sv_symbol, 'value': ss_expr})
                        
                    for i in range(len(ss_list)):
                        if ss_list[i]['value'].free_symbols == set():
                            if ss_list[i]['value'] < 0:
                                rel += Text('<font color="FF0000">')
                                rel += Math(ss_list[i]['name'] + ": $v", v = round(ss_list[i]['value'], 3))
                                rel += Text('</font>')
                            else:
                                rel += Math(ss_list[i]['name'] + ": $v", v = round(ss_list[i]['value'], 3))
                        else:
                                rel += Math(ss_list[i]['name'] + ": $v", v = ss_list[i]['value'])
    
                        if i< len(ss_list)-1:
                            rel += Text(", ")
    
                    rel += Newline()*2
    
                    dic = par_set['values']
                    for i in range(len(ss_list)):
                        dic[ss_list[i]['name']] = ss_list[i]['value']
    
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
                            rel += Math("$s: $v", s = lamda_i, v = "{:.3f}".format(ev)) + Newline()
        
                            if ev.imag != 0:                        
                                rho = -ev.real/np.sqrt(ev.real**2+ev.imag**2)
                                rel += Math("$s: $v", s = Symbol("rho_"+ str(i+1)), v = "{:-3f}".format(rho)) + Newline()
                        else:
                            lamda_i = Symbol('lamda_'+ str(i+1))
                            rel += Math("$s: $v", s = lamda_i, v = ev.evalf(4)) + Newline()
        
                            #if ev.imag != 0:                        
                            #    rho = -ev.real/np.sqrt(ev.real**2+ev.imag**2)
                            #    rel += Math("$s: $v", s = Symbol("rho_"+ str(i+1)), v = "{:-3f}".format(rho)) + Newline()
    
        
                    rel += EmptyLine()*2
                        

    #fixme
#    steady_states=solve(model.rhs, model.state_vector['expr'], dict=True)

    
    return rel

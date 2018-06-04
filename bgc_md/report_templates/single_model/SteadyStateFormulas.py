def template(model):
    rel=ReportElementList()

    srm = model.reservoir_model
    if srm is None:
        return ReportElementList()

    formal_steady_states = srm.steady_states()
    time_symbol = srm.time_symbol
    
    if formal_steady_states:
        rel = Header("Steady state formulas", 2)
        for ss_dict in formal_steady_states:
            for sv in srm.state_variables:
                if sv in ss_dict.keys():
                    rel += Math("$name = $value", name=sv, value=ss_dict[sv])
                    rel += EmptyLine()*2

    return rel

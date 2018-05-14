def template(model):
    rel = Header("Pool model representation", 2)
    reservoir_model = model.reservoir_model
    inputs = reservoir_model.input_fluxes
    outputs = reservoir_model.output_fluxes
    internal_fluxes = reservoir_model.internal_fluxes
    
    fig = reservoir_model.figure(figure_size=(7,7))
    fig_rel = MatplotlibFigure(fig, "Figure 1", "Pool model representation")
    rel+=fig_rel
    legend = ReportElementList()
    # input fluxes
    if len(inputs) > 0:
        legend += Header("Input fluxes", 4)
        for pool, flux in inputs.items():
            legend += Math("$v: $f", v=py2tex_silent(model.state_variables[pool]), f=flux)
            legend += Newline()
    
    # output fluxes
    if len(outputs) > 0:
        legend += Text("\n")
        legend += Header("Output fluxes", 4)
        for pool, flux in outputs.items():
            legend += Math("$v: $f", v=py2tex_silent(model.state_variables[pool]), f=flux)
            legend += Newline()
    
    # internal fluxes
    if len(internal_fluxes) > 0:
        legend += Text("\n")
        legend += Header("Internal fluxes", 4)
        if_sorted = [((i,j), f) for (i,j), f in internal_fluxes.items()]
        if_sorted = sorted(if_sorted, key=lambda el: (el[0][0],el[0][1]))
        for (pfrom, pto), flux in if_sorted:
            legend += Math("$pf \\rightarrow $pt: $f", pf=py2tex_silent(model.state_variables[pfrom]), pt=py2tex_silent(model.state_variables[pto]), f=flux)
            legend += Newline()

    rel+=legend
    return rel

def template(srm, ss_dict, par_set):
    from LAPM.linear_autonomous_pool_model import LinearAutonomousPoolModel

    u = srm.external_inputs.subs(ss_dict).subs(par_set)
    B = srm.compartmental_matrix.subs(ss_dict).subs(par_set)

    lapm = LinearAutonomousPoolModel(u, B, force_numerical=True)

    rel = Header('Transit time density plot in steady state', 3)
    times=np.linspace(0,2500,100)
    vals=[lapm.T_density(t) for t in times]
    
    fig = plt.figure(figsize=(10,10))
    ax=fig.add_subplot(1,1,1)
    ax.plot(times,vals)
    ax.xaxis.label.set_size(20)
    rel+=MatplotlibFigure(fig, 'Transit time density',' ')
    
    return(rel)


def template(srm, ss_dict, par_set):
    # transit time plot, including mean, for a model in steady state

    from LAPM.linear_autonomous_pool_model import LinearAutonomousPoolModel
    
    u = srm.external_inputs.subs(ss_dict).subs(par_set)
    B = srm.compartmental_matrix.subs(ss_dict).subs(par_set)

    lapm = LinearAutonomousPoolModel(u, B, force_numerical=True)
    T_mean = np.float(lapm.T_expected_value)

    rel = Header('Transit time density plot in steady state', 3)
    times=np.linspace(0, 15000, 50)
    vals=[lapm.T_density(t) for t in times]
    
    fig = plt.figure(figsize=(10,10))
    ax=fig.add_subplot(1,1,1)
    ax.plot(times,vals, label='transit time density', lw=3)
    ax.axvline(x=T_mean, c='red', lw=3, label='mean', ls="--")
    ax.xaxis.label.set_size(20)
    ax.set_xlim([times[0], times[-1]])
    ax.set_ylim([0, ax.get_ylim()[1]])
    ax.legend(fontsize=20)

    rel+=MatplotlibFigure(fig, 'Transit time density',' ')
    
    return(rel)


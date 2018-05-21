def template(model_run):
    rel=ReportElementList()
    n = model_run.nr_pools
    model=model_run.model
    print(model.state_vector)
    # plot solutions
    fontsize = 20
    fig = plt.figure(figsize=(7,7), tight_layout=True)
    model_run.plot_solutions(fig, fontsize=fontsize)
    label = "Model run - solutions"
    run_data_str = "We should interview the model run object here"
    rel += MatplotlibFigure(fig, label, run_data_str)
    return rel

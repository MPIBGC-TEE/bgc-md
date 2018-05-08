# the function name and signature:
# template(model_list) is a convention. It will be called in a 
# predefined environment by a higher order function.
# If you want to include another template call you can do so with a line
# rel+=render(Path("path/to/the/template.py"))

def template(model_list):
    # get  mapping from the modelnames to the symbols to keep them consistent in all the plots
    symbol_list=gv.symbol_list
    if len(model_list) < len(symbol_list):
        mapping={(model_list[ind]).name:symbol_list[ind] for ind in range(len(model_list))}
    else:
        raise(Exception("The number of unique plot symbols is smaller than the number of models in the list. Change the way the symbol list is created."))

    rel=ReportElementList()
    
    fig = plt.figure(figsize=(15,10), tight_layout=True)

    # Attention: The help of figure.add_subplot is wrong!
    nr_col = 3
    nr_row = 2
    ax = fig.add_subplot(nr_row, nr_col, 1)
    ax = model_list.create_histogram(ax,x='nr_state_v',x_label='No. state variables',y_label='No. models')
    
    # parameters and models
    ax = fig.add_subplot(nr_row, nr_col, 2)
    ax = model_list.create_histogram(ax,x='nr_parameters',x_label='No. parameters',y_label='No. models')
    
    # variables and models
    ax = fig.add_subplot(nr_row, nr_col, 3)
    ax = model_list.create_histogram(ax,x='nr_variables',x_label='No. variables',y_label='No. models')
    rel += MatplotlibFigure(fig,'Figure 1',"Histograms,  variables") 



######################################################################
    # scatter plots
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(1,1,1)
    ax= model_list.create_scatter_plot(
        ax
        ,x='nr_variables'
        ,y='nr_parameters'
        ,x_label='No. variables'
        ,y_label='No. parameters'
        ,model_symbol_mapping=mapping
    )
        
    rel += MatplotlibFigure(fig,"Figure 2","No. variables & parameters" )

######################################################################
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(1,1,1)
    ax = model_list.create_scatter_plot(
        ax
        ,x='nr_variables'
        ,y='nr_ops'
        ,x_label='No. variables'
        ,y_label='No. operations to calculate rhs'
        ,model_symbol_mapping=mapping
    )
        
    rel += MatplotlibFigure(fig,"Figure 3","No. variables & operations" )
    
######################################################################
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(1,1,1)
    ax = model_list.create_scatter_plot(
        ax
        ,x='nr_variables'
        ,y='max_depth'
        ,x_label='No. variables'
        ,y_label='Cascading depth of operations\n to calculate the rhs'
        ,model_symbol_mapping=mapping
    )
        
    rel += MatplotlibFigure(fig,"Figure 4","No. variables & cascading depth of operations" )
    
######################################################################
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(1,1,1)
    ax = model_list.create_scatter_plot(
        ax
        ,x='nr_ops'
        ,y='max_depth'
        ,x_label='No. operations to calculate the rhs'
        ,y_label='Cascading depth of operations\n to calculate the rhs'
        ,model_symbol_mapping=mapping
    )
        
    rel += MatplotlibFigure(fig,"Figure 5","No. variables & cascading depth of operations" )

#####################################################################
    model_list = ModelList(
        m for m in model_list 
        if m.partitioning_scheme
    )
    fig = plt.figure(figsize=(6,len(model_list)*0.53))
    fig.subplots_adjust(bottom=0.2, top=0.8, left=0.2)
    ax = fig.add_subplot(1,1,1)
    ax.set_xlim(0,3)
    ax = model_list.create_scatter_plot_plus_rand(
        ax
        ,x='partitioning_scheme_nr'
        ,y='nr_ops'
        ,x_label='Partitioning scheme'
        ,y_label='No. operations to calculate the rhs'
        ,model_symbol_mapping=mapping
    )
    ax.set_xticks([1,2])
    ax.set_xticklabels(['fixed','dynamic'], fontsize = "14")
    
    rel += MatplotlibFigure(fig,"Figure 6","Type of carbon partitioning scheme among pools and No.  operations" )

#####################################################################
    model_list = ModelList(
        m for m in model_list 
        if m.partitioning_scheme and m.yaml_file_provides("claimedDynamicPart")
    )
    #fig = plt.figure()
    fig = plt.figure(figsize=(7,len(model_list)*0.53))
    fig.subplots_adjust(bottom=0.2, top=0.8, left=0.2)
    ax = fig.add_subplot(1,1,1)
    ax.set_xlim(0,3)
    ax = model_list.create_scatter_plot_plus_rand(
        ax
        ,x='partitioning_scheme_nr'
        ,y='claimed_dyn_part_nr'
        ,x_label='Partitioning scheme'
        ,y_label='Claimed to have a \n dynamic partitioning scheme?'
        ,model_symbol_mapping=mapping
    )
    ax.set_xticks([1,2])
    ax.set_xticklabels(['fixed','dynamic'])
    ax.set_yticks([1,2])
    ax.set_yticklabels(['No','Yes'])
    
    rel += MatplotlibFigure(fig,"Figure 7","Type of carbon partitioning scheme among pools and claim to have a dynamic partitionings" )

#####################################################################
    # fixme:
    # the models in the model_list should be selected by whether they have a cycling matrix or not (Vegetation Models)
    model_list= ModelList(
        m for m in model_list 
        if hasattr(m,"cyc_matrix")
    )
    fig = plt.figure(figsize=(7,len(model_list)*0.53))
    fig.subplots_adjust(bottom=0.2, top=0.8, left=0.2)
    ax = fig.add_subplot(1,1,1)
    ax = model_list.create_scatter_plot_plus_rand(
        ax
        ,x='nr_state_v'
        ,y='cyc_matrix_diagonal_nr'
        ,x_label='No. state variables'
        ,y_label='Diagonal matrix?'
        ,model_symbol_mapping=mapping
    )
    ax.set_yticks([1,2])
    ax.set_yticklabels(['No','Yes'])
    
    rel += MatplotlibFigure(fig,"Figure 8","Number of state variables and C cycling among compartments" )

######################################################################

    target_key="state_vector"
    # first check wich models actually provide the target_key we are looking for
    models_with_target_key = ModelList(
       m for m in model_list
       if m.has_key(target_key)
    )

    fig = plt.figure(figsize=(30,15), tight_layout=True)
    # note that the second argument 1 in figsize is required by matplotlib 
    # but ignored by the following method because the 
    # height will be adapted inside the method
    nr_row = 2
    ax = fig.add_subplot(nr_row,1,1)
    models_with_target_key.plot_dependencies(target_key,ax)
    ax = fig.add_subplot(nr_row,1,2)
    models_with_target_key.plot_model_key_dependencies_scatter_plot(target_key,ax)

    rel += MatplotlibFigure(fig,"Figure 6","Dependency plots of compartment variables" )
######################################################################
    

    rel += Header("Bibliography", 1)
    return(rel)

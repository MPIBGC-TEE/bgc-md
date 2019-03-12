def template(model):
    if model.long_name:
        t=Template("\'Report of the model: $long_name ($name), version: $version\'").substitute(
            long_name=model.long_name
            ,name=model.name 
            ,version=model.version)
    else:
        t=Template("\'Report of the model: $name, version: $version\'").substitute( name=model.name ,version=model.version)
    #rel=ReportElementList()
    rel= Meta({"title":t})

    #fixme mm 31.05 2018
    # link is not relative
    #rel+= Link(str(model.yaml_file_path),str(model.yaml_file_path.absolute()))
    #rel+=EmptyLine()
    rel+= Header("General Overview", 1)
    reservoir_model = model.reservoir_model
    if reservoir_model:
        #fixme mm 31.06 
        
    #    plt.rc('text', usetex=True)
    #    plt.rc('font', family='serif')
        rel += MatplotlibFigure(reservoir_model.figure(logo=True), "Logo", show_label=False, transparent=True)
    
    rel+= Text(r"This report presents a general overview of the model $name , which is part of the Biogeochemistry Model Database BGC-MD.  The underlying yaml file entry that contains all the information of the model was created by $curator (Orcid ID: $Oid) on $entryDate. The entry was processed by the python package bgc-md to produce symbolic output.",
        curator=model.entryAuthor,
        entryDate=model.entry_creation_date,
        modDate=model.last_modification_date,
        Oid=model.entryAuthor_orc_id,
        name=model.name
    )
    rel+=EmptyLine()

    #rel += Header("About the model", 2)
    rel += Text(r"The model was originally described by ") 
    rel += Citation(model.bibtex_entry, parentheses=False) + Text(".")+EmptyLine()
    # include the abstract
    if hasattr(model,"abstract"):
        rel += Header("Abstract", 3)
        rel += Text("$abstract", abstract=model.abstract+"\n")

    # include spaceScale:
    if model.spaceScale:
        rel += Header("Space Scale", 3)
    
        space_scale = model.spaceScale
        if type(space_scale) == type(""):
            space_scale = [space_scale]
        rel += Text("$k\n", k = (", ").join(space_scale))


    return rel

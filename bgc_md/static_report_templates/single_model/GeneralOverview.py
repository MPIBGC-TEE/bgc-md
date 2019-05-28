from bgc_md.ReportInfraStructure import ReportElementList, Header, Math, Meta, Text, Citation, Table, TableRow, Newline,EmptyLine,MatplotlibFigure, Link, LinkedSubPage, exprs_to_element, PlotlyFigure
from string import Template
def template(model_id):
#    if model.long_name:
#        t=Template("\'Report of the model: $long_name ($name), version: $version\'").substitute(
#            long_name=model.long_name
#            ,name=model.name 
#            ,version=model.version)
#    else:
#        t=Template("\'Report of the model: $name, version: $version\'").substitute( name=model.name ,version=model.version)
    name="fake"
    version='99999'
    t=Template("\'Report of the model: $name, version: $version\'").substitute( name=name ,version=version)
    rel= Meta({"title":t})
#
#    #fixme mm 31.05 2018
#    # link is not relative
#    rel+= Link(str(model.yaml_file_path),str(model.yaml_file_path.absolute()))
#    rel+=EmptyLine()
#    rel+= Header("General Overview", 1)
#    reservoir_model = model.reservoir_model
#    if reservoir_model:
#        #fixme mm 31.06 
#        
#    #    plt.rc('text', usetex=True)
#    #    plt.rc('font', family='serif')
#        rel += MatplotlibFigure(reservoir_model.figure(logo=True), "Logo", show_label=False, transparent=True)
#    
#    rel+= Text(r"This report is the result of the use of the python package bgc_md, as means to translate published models to a common language.  The underlying yaml file was created by $curator (Orcid ID: $Oid) on $entryDate.",
#        curator=model.entryAuthor,
#        entryDate=model.entry_creation_date,
#        modDate=model.last_modification_date,
#        Oid=model.entryAuthor_orc_id,
#    )
#    rel+=EmptyLine()
#    if model.model_type == "vegetation_model": modType = "carbon allocation"
#    if model.model_type == "soil_model": modType = "soil organic matter decomposition"
#
#    if model.approach:
#        article = "a"
#        if model.approach[0] in "aeiou":
#            article = "an"
#        modApproach = " with " + article + " " + model.approach + " approach."
#    else:
#        modApproach = "."
#
#    rel += Header("About the model", 2)
#    rel += Text(r"The model depicted in this document considers $modType$modApproach It was originally described by ", 
#        modType=modType, modApproach=modApproach)
#    if hasattr(model,'bibtex_entry'):
#        rel += Citation(model.bibtex_entry, parentheses=False) + Text(".")+EmptyLine()
#    # include the abstract
#    if hasattr(model,"abstract"):
#        rel += Header("Abstract", 3)
#        rel += Text("$abstract", abstract=model.abstract+"\n")
#    # include keywords
#    if model.keywords:
#        rel += Header("Keywords", 3)
#        rel += Text("$k\n", k = (", ").join(model.keywords))
#
#    # include principles
#    if model.principles:
#        rel += Header("Principles", 3)
#        rel += Text("$k\n", k = (", ").join(model.principles))
#
#    # include spaceScale:
#    if model.spaceScale:
#        rel += Header("Space Scale", 3)
#    
#        space_scale = model.spaceScale
#        if type(space_scale) == type(""):
#            space_scale = [space_scale]
#        rel += Text("$k\n", k = (", ").join(space_scale))
#
#    # include information on available parameter sets
#    if model.parameter_sets:
#        desc_exists = False
#        colname_list = [Text("Abbreviation")]
#        format_list = ["l"]
#        for par_set in model.parameter_sets:
#            sources_exist = False
#            desc_exists = False
#            if 'bibtex_entry' in par_set.keys() and par_set['bibtex_entry']: sources_exist = True
#            if 'desc' in par_set.keys() and par_set['desc']: desc_exists = True
#
#        if desc_exists:
#            colname_list.append(Text("Description"))
#            format_list.append("l")
#        if sources_exist:
#            colname_list.append(Text("Source"))
#            format_list.append("l")
#    
#        # show this section only if additional information to the parameter sets is given
#        if len(colname_list)>1:
#            rel += Header("Available parameter values", 3)
#            headers_row = TableRow(colname_list)
#            T = Table(" Information on given parameter sets", headers_row, format_list)
#            for par_set in model.parameter_sets:
#                l = [Text(par_set['table_head'])]
#                if desc_exists: 
#                    if par_set['desc']:
#                        l.append(Text(par_set['desc']))
#                    else:
#                        l.append(Text(" "))
#
#                if sources_exist: 
#                    if par_set['bibtex_entry']:
#                        l.append(Citation(par_set['bibtex_entry'], parentheses=False))
#                    else:
#                        l.append(Text(" "))
#
#                tr = TableRow(l)
#                T.add_row(tr)    
#            rel += T
#
#    # include information on available initial values sets
#    if model.initial_values:
#        desc_exists = False
#        colname_list = [Text("Abbreviation")]
#        format_list = ["l"]
#        for par_set in model.initial_values:
#            if 'bibtex_entry' in par_set.keys() and par_set['bibtex_entry']: sources_exist = True
#            if 'desc' in par_set.keys() and par_set['desc']: desc_exists = True
#
#        if desc_exists:
#            colname_list.append(Text("Description"))
#            format_list.append("l")
#        if sources_exist:
#            colname_list.append(Text("Source"))
#            format_list.append("l")
#    
#        # show this section only if additional information to the initial values sets is given
#        if len(colname_list)>1:
#            rel += Header("Available initial values", 3)
#            headers_row = TableRow(colname_list)
#            T = Table(" Information on given sets of initial values", headers_row, format_list)
#            for par_set in model.initial_values:
#                l = [Text(par_set['table_head'])]
#                if desc_exists: 
#                    if par_set['desc']:
#                        l.append(Text(par_set['desc']))
#                    else:
#                        l.append(Text(" "))
#
#                if sources_exist: 
#                    if par_set['bibtex_entry']:
#                        l.append(Citation(par_set['bibtex_entry'], parentheses=False))
#                    else:
#                        l.append(Text(" "))
#
#                tr = TableRow(l)
#                T.add_row(tr)    
#            rel += T

    return rel

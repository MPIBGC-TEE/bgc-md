
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

    rel+= Link("yaml_file",str(model.yaml_file_path))
    rel+=Newline()
    rel+=Newline()
    rel+= Header("General Overview", 1)

    return(rel)


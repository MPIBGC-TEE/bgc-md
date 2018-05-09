def template(model):
    # include the abstract
    if model.abstract:
        rel = Header("Abstract", 3)
        rel += Text("$abstract", abstract=model.abstract+"\n")
    return rel

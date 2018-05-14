def template(model):
    
    rel = Header("The right hand side of the ODE", 2)
    rel += Math("$eq", eq=model.rhs)
    rel += EmptyLine()
    rel += Header("The Jacobian (derivative of the ODE w.r.t. state variables)", 2)
    rel += Math("$J", J=model.jacobian())
    rel += EmptyLine()
    return rel

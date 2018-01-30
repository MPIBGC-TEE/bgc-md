from sympy import var,Matrix
import numpy as np
from scipy.integrate import odeint
# first example handcrafted righthandside
#def righthandside(X,t):
#	return(5*X)
#
#times=np.arange(10)
#X0=np.ones(2)#Startvalues, some array
#Xsol=odeint(righthandside,X0,times) #solutions for t in times
#print(Xsol)

# second example  righthandside created from expression
# two dimensional handcrafted
def funcmaker(expr,statevector,time_sym):
    def f(X,t):
        #create the dictionary for substitute
        edict={sv:X[i] for i,sv in enumerate(statevector)}
        edict.update({time_sym:t})
        #substitute 
        eval_expr=expr.subs(edict)
        #transform the resulting matrix to a list
        return(list(eval_expr))
	
    return(f)
  
var("t x1 x2")
fv=Matrix([x1**2,x2**2])
sv=Matrix([x1,x2])
auto_rhs=funcmaker(fv,sv,t)
times=np.arange(10)
X0=np.ones(2)#Startvalues, some array
Xsol=odeint(auto_rhs,X0,times) #solutions for t in times
print(Xsol)

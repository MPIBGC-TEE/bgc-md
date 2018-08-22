from scipy.optimize import root,fsolve
from sympy import symbols,Matrix,sin,cos,zeros,lambdify
from CompartmentalSystems.helpers_reservoir import jacobian
import numpy as np


# first example form tutorial
def fun(x):
    return [x[0]  + 0.5 * (x[0] - x[1])**3 - 1.0,
            0.5 * (x[1] - x[0])**3 + x[1]]

def jac(x):
    return np.array([[1 + 1.5 * (x[0] - x[1])**2,
                      -1.5 * (x[0] - x[1])**2],
                     [-1.5 * (x[1] - x[0])**2,
                      1 + 1.5 * (x[1] - x[0])**2]])

x0=np.zeros([2,1])
res = root(fun=fun,jac=jac,x0=x0)
#print(res.x)

# we see that we have to wrap the functions returned by lambdify
# since root expects a single vector like argument
phi,theta =symbols("phi,theta")
expr=Matrix([cos(phi),cos(theta)])
tup=(phi,theta)
stateVec=Matrix([x for x in tup])
ex_lamb=lambdify(tup,expr,modules='numpy')
jac_lamb=lambdify(tup,jacobian(expr,stateVec))

def ex_func(x):
    tup=tuple(x)
    return ex_lamb(*tup).reshape(x.shape)
def jac_func(x):
    tup=tuple(x)
    return jac_lamb(*tup)

ex_func(np.array([0,0]))
jac_func(np.array([0,0]))
#x0=1e-1*np.ones(stateVec.shape)
#x0=np.ones(stateVec.shape)
x0=np.zeros(stateVec.shape)

res = root(fun=ex_func,jac=jac_func,x0=x0,tol=1e-12)
print(res.x)
print(ex_func(res.x))
print(jac_func(res.x))

# in general our models will contain func_sets (external function u1(x,y,t),u2(t) ...)
# in this case the jacobian would contain expressions of the form du1/dx du1/dy and so on, which might not be available
# in this situation we have to call the root function with jac=False 
x0=1e-1*np.ones(stateVec.shape)
res = root(fun=ex_func,jac=False,x0=x0)
print(res.x)
print(ex_func(res.x))
print(jac_func(res.x))
# or a method that does not use the jacobian
res = root(fun=ex_func,method='krylov',x0=x0)
print(res.x)
print(ex_func(res.x))
print(jac_func(res.x))

# we can also try fsove
res = fsolve(func=ex_func,x0=x0,xtol=1e-12)
print(res)
print(ex_func(res))
print(jac_func(res))
# all methods depend very much non the startvalues


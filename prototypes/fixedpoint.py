from scipy.optimize import root 
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

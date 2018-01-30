#!/usr/bin/python3 env

import matplotlib.pyplot as plt

import numpy as np
from scipy.integrate import odeint
from sympy import Piecewise

def A(t):
	return(np.matrix([
		[-2,   0],
		[0	, -1]]))

def I(t):
    print(t)
    r = np.matrix([[Piecewise((np.sin(t)+1, t<=6), (0, True))], [0]])
    if t == 5.01:
        r += 20

    return r

X0=np.array([1,2])
n=X0.shape[0]

def rhs(X,t):
	Xdot=A(t)*np.matrix(X).transpose()+I(t)
	return(np.array(Xdot, dtype='float64').reshape((n,)))

times=np.linspace(0,10,101)
times = times.tolist() + [5.01]
times = np.array(times)
times.sort()
print(times)

soln=odeint(rhs,X0,times)

print('making plots')
plt.plot(times, soln)
plt.xlabel('time (s)')
plt.ylabel('content')
plt.title('solution')
plt.grid(True)
plt.savefig("test.svg")
plt.show()

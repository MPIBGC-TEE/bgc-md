# Check the behaviour of Piecewise expression containing an undefined function when the piecewise
# expression is lambdified
from sympy import Function,Piecewise,lambdify,Symbol,pprint,Not,Eq
t=Symbol('t')
u=Function('u')

#p_sym=Piecewise((-u(t),u(t)<0),(u(t),u(t)>=0))
p_sym=Piecewise((1,Eq(u(t),0)) ,(0 ,Not(Eq(u(t),0))) )
pprint(p_sym)
# now we implement a python Version for u
u_num=lambda x:x

p_num=lambdify(t,p_sym,{"u":u_num})
print( [p_num(i) for i in [-2,-1,0,1]])


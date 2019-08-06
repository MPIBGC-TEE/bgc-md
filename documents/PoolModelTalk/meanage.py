from sympy import *
import compiler as cp
def lp(str):
   print(str)
def displaymath(expr):
   return("\\["+latex(expr)+"\\]")

def anasol(C0,In,t0,t):
    tau=Symbol("tau")
    sol=C0*exp(A(t-t0))+integrate(exp(A(t-tau))*In(tau),(tau,t0,t))
    return(sol.powsimp())

# now we build the solution operator
def S(C0,ta,t):
    # it uses the analytical solution for zero inputrate
    def zero(something):
        return(0)
    sol=anasol(C0,zero,ta,t)
    return(sol)
dic={}
def add_displaymath(string):
    dic[string]=displaymath(latex(eval(string)))

t,t0,ta,a=symbols("t,t0,ta,a")
C0,A,I=symbols("C0,A,I")
sol_abstract=anasol(C0,I,t0,t)
add_displaymath("sol_abstract")   
k=Symbol("k")
def A(t):
    return(-k*t)

I0=Symbol("I0")
def I(t):
    return(I0)
sol_constant=anasol(C0,I,t0,t)
add_displaymath("sol_constant")   


#print(S(I(t-ta),ta,t))
## we now construct the formula for the Expected Value of the age (mean age)
E=integrate(S(I(t-a),t-a,t)/anasol(C0,I,0,t),(a,0,t))
#print(simplify(E))
E3=E.subs(k,3)

#print(limit(E3,t,oo))

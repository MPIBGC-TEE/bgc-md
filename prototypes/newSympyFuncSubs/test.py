from sympy import Function,var,lambdify
import numpy

var("x y")
u1_sym=Function("u1_sym")

def u1_func(x_v,y_v):
    return x_v+y_v

expr=1+u1_sym(x,y)
func_set={u1_sym:u1_func}
# the indices in funset are exressions of the form u_1(x,..)
# Firstly we convert them to strings 'u_1(x,...)'
str_func_set = {str(key): val for key, val in func_set.items()}

## Secondly we remove the parenthesis and there content
## since lambdify wants the dictionary indexed by
## the function name only
## after this step we have the key 'u_1'
#cut_func_set = {key[:key.index('(')]: val 
#    for key, val in str_func_set.items()}
tup=(x,y)
#expr_func=lambdify(expr,tup,modules=[cut_func_set,"numpy"])
expr_func=lambdify(tup,expr,modules=[str_func_set,"numpy"])
expr_func(1,2)
#numerical_function_from_expression


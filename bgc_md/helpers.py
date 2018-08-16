# vim:set ff=unix expandtab ts=4 sw=4:

import copy
import sys
import numpy as np 

from sympy import sympify, Symbol, MatrixSymbol 
from sympy.abc import _clash
from sympy.parsing import sympy_parser
from pytexit import py2tex


def pp(strng,env,comment=""):
    pe(strng,env,comment)

def pe(strng,env,comment=""):
    pass
    #print("\n####################################\n")
    #print(comment+"\n"+strng+"=:")
    #print(eval(strng,env))
    #print("\n####################################\n")


def remove_indentation(entry_str):
    lst = entry_str.splitlines()
    new_lst = []
    for line in lst:
        new_lst.append(line.strip())
    
    result = "\n".join(new_lst)
    return result


def create_symbols_func(symbols, g={}, l={}):
    gn = copy.copy(g)
    ln = copy.copy(l)
    exec("from sympy import *", gn, ln)
    for sym in symbols:
        expr = sym + "=Symbol('"+sym+"')"
        exec(expr, gn, ln)
    return(gn, ln)


def eval_expressions(expression_list, g, l):
    for expr in expression_list:
        #pe('expr',locals())
        not_expr = []
        if expr not in not_expr:
            try:
                exec(expr, g, l)
            except BaseException as e:
               raise Exception("The expression that could not be evaluated was: " + str(expr) + "\n" + str(e))

        
def retrieve_or_default(complete_dict,key):
#    default="a value for the key:\""+str(key)+"\" is not available"
    default = None
    if key in complete_dict.keys():
        if complete_dict[key]: #check for the case that key is present but the corresponding value is None
            val=complete_dict[key]
        else:
            val=default
    else:
        val=default
    return(val)


def retrieve_this_or_that(key,Option2,Dict):
    if key in Dict.keys():
        if Dict[key]==None: 
            del Dict[key]
            This=Dict.get(key,Option2) #If there is no 'key', another string <Option2> is returned
        else: 
            This=Dict[key]
    else:
        This=Option2
    return(This)


#fixme: to be tested
def key_from_dict_by_value(dic, target_value):
    for key, value in dic.items():
        if value == target_value:
            return key

    return None


def non_commutative_sympify(expr_string, expr_set):
    parsed_expr = sympy_parser.parse_expr(expr_string, evaluate = False, local_dict = _clash)

    symbols_string = [sym.name for sym in parsed_expr.atoms(Symbol)]
    symbols_list = [expr_set[name] for name in symbols_string]

    new_locals = dict()
    for index, sym in enumerate(symbols_list):
        name = symbols_string[index]
        if hasattr(sym, 'is_Matrix') and sym.is_Matrix == True:
            new_locals[name] = MatrixSymbol(name, sym.rows, sym.cols)
        else:
            new_locals[name] = Symbol(name)


#    new_locals = {sym.name:Symbol(sym.name, commutative=False) for sym in parsed_expr.atoms(Symbol)}
    z = _clash.copy()
    z.update(new_locals)
#    print(expr_string)
    return sympify(expr_string, locals=z)


def py2tex_silent(python_expression):
    expr_str = str(python_expression)
    result = (py2tex(expr_str, print_latex=False, print_formula=False,).replace("$$", ""))

    # matrices (also diagonal ones) are handled by sympify only
    # they are not implemented in py2tex, even though
    # diag does not raise an error
    if r'\operatorname{diag}\left(' in result: raise(TypeError)
    return result


def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size



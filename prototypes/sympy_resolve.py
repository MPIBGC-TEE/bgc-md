from sympy import sympify,symbols,Symbol

def resolve(targetSym,sl,ed):
    if targetSym in sl:
        return targetSym 
    else:
        e=ed[targetSym]
        print(e.free_symbols)
        return e.subs({s:resolve(s,sl,ed) for s in e.free_symbols}) 

syms=['k','r','s']
sl=[Symbol(s) for s in syms]
expressions={"y":"x**2+k","x":"u*2","u":"r+s"}
#expressions={"u":"r+s"}
ed={Symbol(k):sympify(v) for k,v in expressions.items()}

resolve(Symbol('y'),sl,ed)

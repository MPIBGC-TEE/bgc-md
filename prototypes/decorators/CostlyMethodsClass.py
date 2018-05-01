#example for expensive computation
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1 
    else:
        return fib(n-1) + fib(n-2)


def cache(method):
    def decorated(*args,**kw):
        print(method.__name__)
        self=(args[0])
        cache_attr="_"+method.__name__

        if  not hasattr(self,cache_attr):
            result=method(args)
            setattr(self,cache_attr,result)
        return getattr(self,cache_attr)
    return decorated

class Model:

    @cache
    def a(self):
        #if  not hasattr(self,"_a"):
        #    self._a=fib(34)
        #return self._a
        return fib(33)

    @cache
    def b(self):
        #if  not hasattr(self,"_b"):
        #    self._b=fib(34)
        #return self._b
        return fib(34)
    
    def c(self):
        return (self.a()+self.b())

m=Model()
print(m.c())
print(m.c())
print(m._a)
print(m._b)


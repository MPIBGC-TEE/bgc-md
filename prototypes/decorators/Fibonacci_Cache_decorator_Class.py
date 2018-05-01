class Memoize:
    def __init__(self,fn):
        self.fn=fn
        self.memo={}
    
    def __call__(self,*args):
            if args not in self.memo:
                self.memo[args] = self.fn(*args)
            return self.memo[args]

@Memoize
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1 
    else:
        return fib(n-1) + fib(n-2)

print(fib(36))

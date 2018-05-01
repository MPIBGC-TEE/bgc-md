def memoize(f):
    memo={}
    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]
    return helper

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1 
    else:
        return fib(n-1) + fib(n-2)
@memoize
def fib2(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1 
    else:
        return fib(n-1) + fib(n-2)

# direct call with exponential runtime
print(fib(36))

# create caching version explicitly 
fib_c=memoize(fib)
print(fib_c(36))
# or use decorated 
print(fib2(36))

def greeting(expr):
    def greeting_decorator(func):
        def function_wrapper(x):
            print(expr + ", " +func.__name__ + " returns:")
            return func(x)
        return function_wrapper
    return greeting_decorator

@greeting("καλημερα")
def foo(x):
    print(42)
    

foo("whatever")



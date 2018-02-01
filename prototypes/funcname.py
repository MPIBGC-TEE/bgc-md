from inspect import stack
def me():
    # the function returns the name of the function it was called by
    return(stack()[1][3])

def func():
    print(me())

func()

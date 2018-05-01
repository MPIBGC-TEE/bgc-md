# demonstrate __call__
class A:
    def __init__(self):
        print("An instance of A was initialized")

    def __call__(self,*args,**kwargs):
        print("Arguments are:", args,kwargs)

x=A()
print("now calling the instance:")
x(3,4,x=11,y=10)

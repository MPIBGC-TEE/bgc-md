class Singelton(type):
    _instances = {}
    def __call__(cls,*args,**kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singelton,cls).__call__(*args,**kwargs)
        return cls._instances[cls]


class SingeltonClass(metaclass=Singelton):
    pass
class RegularClass():
    pass

x=SingeltonClass()
y=SingeltonClass()
print(x==y)

x=RegularClass()
y=RegularClass()
print(x==y)


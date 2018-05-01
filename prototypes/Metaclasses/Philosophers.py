# main part
x = input("Do you need the answer? (y/n): ")

if x.lower() == "y":
    required = True
else:
    required = False
# prepare the common method
def the_answer(self,*args):
    return 42
# define a metaclass than conditionally adds this mehtod to several classes
class EssentialAnswer(type): 
    def __init__(cls, clsname, superclasses, attributedict):
        if required:
            cls.the_answer = the_answer
            

class Philosopher1(metaclass=EssentialAnswer):
    pass

class Philosopher2(metaclass=EssentialAnswer):
    pass
class Philosopher3(metaclass=EssentialAnswer):
    pass

plato = Philosopher1()
print(plato.the_answer())

kant = Philosopher2()
print(kant.the_answer())


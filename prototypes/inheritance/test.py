# baue das Vererbungsshema nach...
class ILAMBVariable:
    def __init__(self,val):
        self.value=val


class MyVariable(ILAMBVariable):
    def __init__(self,val):
        super().__init__(val)


class FluxVariable(MyVariable):

    def accumulateInTime(self):
        return self.value**2 


class StockVariable(MyVariable):
    pass 

############################
# 1. Test sollte klappen 
fv=FluxVariable(2)
fv.accumulateInTime()

# 2. Test sollte in der zweiten Zeile scheitern 
sv=StockVariable(2)
sv.accumulateInTime()



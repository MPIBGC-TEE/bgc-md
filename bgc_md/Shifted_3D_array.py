# vim: set ff=unix expandtab ts=4 sw=4:

import numpy as np

class Shifted_3D_array(np.ndarray):
    def __new__(cls, input_array, t_shift=0,Ts_shift=0,Tp_shift=0):
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(input_array).view(cls)
        # add the new attribute to the created instance
        obj.t_shift=t_shift
        obj.Ts_shift=Ts_shift
        obj.Tp_shift=Tp_shift
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        # ``self`` is a new object resulting from
        # ndarray.__new__(Shifted_3D_array, ...), therefore it only has
        # attributes that the ndarray.__new__ constructor gave it -
        # i.e. those of a standard ndarray.
        #
        # We could have got to the ndarray.__new__ call in 3 ways:
        # From an explicit constructor - e.g. Shifted_3D_array():
        #    obj is None
        #    (we're in the middle of the Shifted_3D_array.__new__
        #    constructor, and self.t_shift, self.Ts_shift, self.Tp_shift 
        #    will be set when we return to
        #    Shifted_3D_array.__new__)
        if obj is None: return
        # From view casting - e.g arr.view(Shifted_3D_array):
        #    obj is arr
        #    (type(obj) can be Shifted_3D_array)
        # From new-from-template - e.g infoarr[:3]
        #    type(obj) is Shifted_3D_array
        #
        # Note that it is here, rather than in the __new__ method,
        # that we set the default values for t_shift,Ts_shift and Tp_shift, because this
        # method sees all creation of default objects - with the
        # Shifted_3D_array.__new__ constructor, but also with
        # arr.view(Shifted_3D_array).
        self.t_shift= getattr(obj, 't_shift', None)
        self.Ts_shift= getattr(obj, 'Ts_shift', None)
        self.Tp_shift= getattr(obj, 'Tp_shift', None)
        # We do not need to return anything


    def set_t_shift(self, ts):
        self.t_shift = ts
            # fixme: make this a property set function 
        

    def t_shift(self):
        return self.t_shift


    def __getitem__(self, index_tuple):
#        print("index_tuple",index_tuple)
        xindex_new = index_tuple[0] + self.t_shift
        new_tuple = (xindex_new, index_tuple[1],index_tuple[2])
        return(super().__getitem__(new_tuple))




from typing import List
from sympy import eye, trigsimp, ImmutableMatrix as Matrix, Symbol, sin, cos,\
    sqrt, diff, Tuple, acos, atan2, simplify,Add ,symbols, MatrixBase, ImmutableDenseMatrix
from sympy.core import S, Pow, sympify , Dummy, Lambda
from sympy.core.assumptions import StdFactKB
from sympy.core.basic import Basic
from sympy.core.cache import cacheit
from sympy.core.compatibility import range, default_sort_key, string_types, range, Callable
from sympy.core.expr import AtomicExpr, Expr
from sympy.solvers import solve

from .basisdependent import (BasisDependent, BasisDependentAdd, BasisDependentMul, BasisDependentZero)
from .dyadic import BaseDyadic, Dyadic, DyadicAdd


from .scalar import BaseScalar

from .orienters import (Orienter, AxisOrienter, BodyOrienter,
                                    SpaceOrienter, QuaternionOrienter)
class Vector(BasisDependent):
    """
    Super class for all Vector classes.
    Ideally, neither this class nor any of its subclasses should be
    instantiated by the user.
    """

    is_Vector = True
    _op_priority = 12.0

    @property
    def components(self):
        """
        Returns the components of this vector in the form of a
        Python dictionary mapping BaseVector instances to the
        corresponding measure numbers.

        Examples
        ========

        >>> from sympy.vector import CoordSys3D
        >>> C = CoordSys3D('C')
        >>> v = 3*C.i + 4*C.j + 5*C.k
        >>> v.components
        {C.i: 3, C.j: 4, C.k: 5}

        """
        # The '_components' attribute is defined according to the
        # subclass of Vector the instance belongs to.
        return self._components

    def dot(self, other):
        """
        Returns the dot product of this Vector, either with another
        Vector, or a Dyadic, or a Del operator.
        If 'other' is a Vector, returns the dot product scalar (Sympy
        expression).
        If 'other' is a Dyadic, the dot product is returned as a Vector.
        If 'other' is an instance of Del, returns the directional
        derivative operator as a Python function. If this function is
        applied to a scalar expression, it returns the directional
        derivative of the scalar field wrt this Vector.

        Parameters
        ==========

        other: Vector/Dyadic/Del
            The Vector or Dyadic we are dotting with, or a Del operator .

        Examples
        ========

        >>> from sympy.vector import CoordSys3D, Del
        >>> C = CoordSys3D('C')
        >>> delop = Del()
        >>> C.i.dot(C.j)
        0
        >>> C.i & C.i
        1
        >>> v = 3*C.i + 4*C.j + 5*C.k
        >>> v.dot(C.k)
        5
        >>> (C.i & delop)(C.x*C.y*C.z)
        C.y*C.z
        >>> d = C.i.outer(C.i)
        >>> C.i.dot(d)
        C.i

        """

        # Check special cases
        if isinstance(other, Dyadic):
            if isinstance(self, VectorZero):
                return Vector.zero
            outvec = Vector.zero
            for k, v in other.components.items():
                vect_dot = k.args[0].dot(self)
                outvec += vect_dot * v * k.args[1]
            return outvec
        from sympy.vector.deloperator import Del
        if not isinstance(other, Vector) and not isinstance(other, Del):
            raise TypeError(str(other) + " is not a vector, dyadic or " +
                            "del operator")

        # Check if the other is a del operator
        if isinstance(other, Del):
            def directional_derivative(field):
                from sympy.vector.functions import directional_derivative
                return directional_derivative(field, self)
            return directional_derivative

        return dot(self, other)

    def __and__(self, other):
        return self.dot(other)

    __and__.__doc__ = dot.__doc__



    def outer(self, other):
        """
        Returns the outer product of this vector with another, in the
        form of a Dyadic instance.

        Parameters
        ==========

        other : Vector
            The Vector with respect to which the outer product is to
            be computed.

        Examples
        ========

        >>> from sympy.vector import CoordSys3D
        >>> N = CoordSys3D('N')
        >>> N.i.outer(N.j)
        (N.i|N.j)

        """

        # Handle the special cases
        if not isinstance(other, Vector):
            raise TypeError("Invalid operand for outer product")
        elif (isinstance(self, VectorZero) or
                isinstance(other, VectorZero)):
            return Dyadic.zero

        # Iterate over components of both the vectors to generate
        # the required Dyadic instance
        args = []
        for k1, v1 in self.components.items():
            for k2, v2 in other.components.items():
                args.append((v1 * v2) * BaseDyadic(k1, k2))

        return DyadicAdd(*args)

    #def projection(self, other, scalar=False):
    #    """
    #    Returns the vector or scalar projection of the 'other' on 'self'.

    #    Examples
    #    ========

    #    >>> from sympy.vector.coordsysrect import CoordSys3D
    #    >>> from sympy.vector.vector import Vector, BaseVector
    #    >>> C = CoordSys3D('C')
    #    >>> i, j, k = C.base_vectors()
    #    >>> v1 = i + j + k
    #    >>> v2 = 3*i + 4*j
    #    >>> v1.projection(v2)
    #    7/3*C.i + 7/3*C.j + 7/3*C.k
    #    >>> v1.projection(v2, scalar=True)
    #    7/3

    #    """
    #    if self.equals(Vector.zero):
    #        return S.zero if scalar else Vector.zero

    #    if scalar:
    #        return self.dot(other) / self.dot(self)
    #    else:
    #        return self.dot(other) / self.dot(self) * self

    @property
    def _projections(self):
        """
        Returns the components of this vector but the output includes
        also zero values components.

        Examples
        ========

        >>> from sympy.vector import CoordSys3D, Vector
        >>> C = CoordSys3D('C')
        >>> v1 = 3*C.i + 4*C.j + 5*C.k
        >>> v1._projections
        (3, 4, 5)
        >>> v2 = C.x*C.y*C.z*C.i
        >>> v2._projections
        (C.x*C.y*C.z, 0, 0)
        >>> v3 = Vector.zero
        >>> v3._projections
        (0, 0, 0)
        """

        from sympy.vector.operators import _get_coord_sys_from_expr
        if isinstance(self, VectorZero):
            return (S(0), S(0), S(0))
        base_vec = next(iter(_get_coord_sys_from_expr(self))).base_vectors()
        return tuple([self.dot(i) for i in base_vec])

    def __or__(self, other):
        return self.outer(other)

    __or__.__doc__ = outer.__doc__

    def to_matrix(self, system):
        """
        Returns the matrix form of this vector with respect to the
        specified coordinate system.

        Parameters
        ==========

        system : CoordSysND
            The system wrt which the matrix form is to be computed

        Examples
        ========

        >>> from sympy.vector import CoordSysND
        >>> C = CoordSys3D('C')
        >>> from sympy.abc import a, b, c
        >>> v = a*C.i + b*C.j + c*C.k
        >>> v.to_matrix(C)
        Matrix([
        [a],
        [b],
        [c]])

        """

        return Matrix([self.dot(unit_vec) for unit_vec in
                       system.base_vectors])

    def separate(self):
        """
        The constituents of this vector in different coordinate systems,
        as per its definition.

        Returns a dict mapping each CoordSys3D to the corresponding
        constituent Vector.

        Examples
        ========

        >>> from sympy.vector import CoordSys3D
        >>> R1 = CoordSys3D('R1')
        >>> R2 = CoordSys3D('R2')
        >>> v = R1.i + R2.i
        >>> v.separate() == {R1: R1.i, R2: R2.i}
        True

        """

        parts = {}
        for vect, measure in self.components.items():
            parts[vect.system] = (parts.get(vect.system, Vector.zero) +
                                  vect * measure)
        return parts


class BaseVector(Vector, AtomicExpr):
    """
    Class to denote a base vector.

    Unicode pretty forms in Python 2 should use the prefix ``u``.

    """

    def __new__(cls, index, system, pretty_str=None, latex_str=None):
        if pretty_str is None:
            pretty_str = "x{0}".format(index)
        if latex_str is None:
            latex_str = "x_{0}".format(index)
        pretty_str = str(pretty_str)
        latex_str = str(latex_str)
        # Verify arguments
        if not isinstance(system, CoordSysND):
            raise TypeError("system should be a CoordSysND")
        if index not in range(system.rank):
            raise ValueError("index must be 0, 1 or 2")
        name = system._vector_names[index]
        # Initialize an object
        obj = super(BaseVector, cls).__new__(cls, S(index), system)
        # Assign important attributes
        obj._base_instance = obj
        obj._components = {obj: S(1)}
        obj._measure_number = S(1)
        obj._name = system._name + '.' + name
        obj._pretty_form = u'' + pretty_str
        obj._latex_form = latex_str
        obj._system = system

        assumptions = {'commutative': True}
        obj._assumptions = StdFactKB(assumptions)

        # This attr is used for re-expression to one of the systems
        # involved in the definition of the Vector. Applies to
        # VectorMul and VectorAdd too.
        obj._sys = system

        return obj

    @property
    def system(self):
        return self._system

    def __str__(self, printer=None):
        return self._name

    @property
    def free_symbols(self):
        return {self}

    __repr__ = __str__
    _sympystr = __str__


class VectorAdd(BasisDependentAdd, Vector):
    """
    Class to denote sum of Vector instances.
    """

    def __new__(cls, *args, **options):
        obj = BasisDependentAdd.__new__(cls, *args, **options)
        return obj

    def __str__(self, printer=None):
        ret_str = ''
        items = list(self.separate().items())
        items.sort(key=lambda x: x[0].__str__())
        for system, vect in items:
            base_vects = system.base_vectors()
            for x in base_vects:
                if x in vect.components:
                    temp_vect = self.components[x] * x
                    ret_str += temp_vect.__str__(printer) + " + "
        return ret_str[:-3]

    __repr__ = __str__
    _sympystr = __str__


class VectorMul(BasisDependentMul, Vector):
    """
    Class to denote products of scalars and BaseVectors.
    """

    def __new__(cls, *args, **options):
        obj = BasisDependentMul.__new__(cls, *args, **options)
        return obj

    @property
    def base_vector(self):
        """ The BaseVector involved in the product. """
        return self._base_instance

    @property
    def measure_number(self):
        """ The scalar expression involved in the definition of
        this VectorMul.
        """
        return self._measure_number


class VectorZero(BasisDependentZero, Vector):
    """
    Class to denote a zero vector
    """

    _op_priority = 12.1
    _pretty_form = u'0'
    _latex_form = r'\mathbf{\hat{0}}'

    def __new__(cls):
        obj = BasisDependentZero.__new__(cls)
        return obj




class Dot(Expr):
    """
    Represents unevaluated Dot product.

    Examples
    ========

    >>> from sympy.vector import CoordSys3D, Dot
    >>> from sympy import symbols
    >>> R = CoordSys3D('R')
    >>> a, b, c = symbols('a b c')
    >>> v1 = R.i + R.j + R.k
    >>> v2 = a * R.i + b * R.j + c * R.k
    >>> Dot(v1, v2)
    Dot(R.i + R.j + R.k, a*R.i + b*R.j + c*R.k)
    >>> Dot(v1, v2).doit()
    a + b + c

    """

    def __new__(cls, expr1, expr2):
        expr1 = sympify(expr1)
        expr2 = sympify(expr2)
        expr1, expr2 = sorted([expr1, expr2], key=default_sort_key)
        obj = Expr.__new__(cls, expr1, expr2)
        obj._expr1 = expr1
        obj._expr2 = expr2
        return obj

    def doit(self, **kwargs):
        return dot(self._expr1, self._expr2)



def dot(vect1, vect2):
    """
    Returns dot product of two vectors.

    Examples
    ========

    >>> from sympy.vector import CoordSys3D
    >>> from sympy.vector.vector import dot
    >>> R = CoordSys3D('R')
    >>> v1 = R.i + R.j + R.k
    >>> v2 = R.x * R.i + R.y * R.j + R.z * R.k
    >>> dot(v1, v2)
    R.x + R.y + R.z

    """
    if isinstance(vect1, Add):
        return Add.fromiter(dot(i, vect2) for i in vect1.args)
    if isinstance(vect2, Add):
        return Add.fromiter(dot(vect1, i) for i in vect2.args)
    if isinstance(vect1, BaseVector) and isinstance(vect2, BaseVector):
        if vect1._sys == vect2._sys:
            return S.One if vect1 == vect2 else S.Zero
        try:
            from .functions import express
            return dot(vect1, express(vect2, vect1._sys))
        except:
            return Dot(vect1, vect2)
    if isinstance(vect1, VectorZero) or isinstance(vect2, VectorZero):
        return S.Zero
    if isinstance(vect1, VectorMul):
        v1, m1 = next(iter(vect1.components.items()))
        return m1*dot(v1, vect2)
    if isinstance(vect2, VectorMul):
        v2, m2 = next(iter(vect2.components.items()))
        return m2*dot(vect1, v2)

    return Dot(vect1, vect2)


def _vect_div(one, other):
    """ Helper for division involving vectors. """
    if isinstance(one, Vector) and isinstance(other, Vector):
        raise TypeError("Cannot divide two vectors")
    elif isinstance(one, Vector):
        if other == S.Zero:
            raise ValueError("Cannot divide a vector by zero")
        return VectorMul(one, Pow(other, S.NegativeOne))
    else:
        raise TypeError("Invalid division involving a vector")

class CoordSysND(Basic):
    def __new__(cls,name:str,vector_names:List[str]=None,parent=None,transformation:tuple=None):
        if parent is not None:
            obj = super(CoordSysND, cls).__new__(
                cls, Symbol(name), transformation, parent)
        else:
            obj = super(CoordSysND, cls).__new__(
                cls, Symbol(name), transformation)
        obj._name = name
        rank=len(vector_names)
        obj.rank=rank
        #vector_names = [vector_name_prefix+'_'+str(i) for i in range(rank)]
        #_check_strings('vector_names', vector_names)
        obj._vector_names = vector_names
        
        base_vectors=[BaseVector(i,obj) for i in range(len(vector_names))]
        obj.base_vectors=base_vectors 
        for i in range(rank):
            setattr(obj,vector_names[i],base_vectors[i])
        
        return obj

    def create_new(self, name, vector_names, transformation):
        """
        Returns a CoordSysND which is connected to self by transformation.

        Parameters
        ==========

        name : str
            The name of the new CoordSysND instance.

        transformation : list of lists defining the Matrix P


        """
        #Examples
        #========

        #>>> from sympy.vector import CoordSys3D
        #>>> a = CoordSysND('a')
        #>>> b = a.create_new('b', transformation='spherical')
        #>>> b.transformation_to_parent()
        #(b.r*sin(b.theta)*cos(b.phi), b.r*sin(b.phi)*sin(b.theta), b.r*cos(b.theta))
        #>>> b.transformation_from_parent()
        #(sqrt(a.x**2 + a.y**2 + a.z**2), acos(a.z/sqrt(a.x**2 + a.y**2 + a.z**2)), atan2(a.y, a.x))

        #"""
        return CoordSysND(name, vector_names=vector_names,parent=self, transformation=transformation, )

    


#def _check_strings(arg_name, arg):
#    errorstr = arg_name + " must be an iterable of 3 string-types"
#    if len(arg) != 3:
#        raise ValueError(errorstr)
#    for s in arg:
#        if not isinstance(s, string_types):
#            raise TypeError(errorstr)

Vector._expr_type = Vector
Vector._mul_func = VectorMul
Vector._add_func = VectorAdd
Vector._zero_func = VectorZero
Vector._base_func = BaseVector
Vector._div_helper = _vect_div
Vector.zero = VectorZero()

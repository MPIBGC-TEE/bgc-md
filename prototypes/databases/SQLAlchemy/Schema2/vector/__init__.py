from .vector import (Vector, VectorAdd, VectorMul,
                     BaseVector, VectorZero,  Dot, dot)
from .dyadic import (Dyadic, DyadicAdd, DyadicMul,
                     BaseDyadic, DyadicZero)
from .scalar import BaseScalar
from .deloperator import Del
from .functions import (express, matrix_to_vector,
                        laplacian, is_conservative,
                        is_solenoidal, scalar_potential,
                        directional_derivative,
                        scalar_potential_difference)
#from .point import Point
from .orienters import (AxisOrienter, BodyOrienter,
                        SpaceOrienter, QuaternionOrienter)
from .operators import Gradient, Divergence, Curl, gradient, curl, divergence

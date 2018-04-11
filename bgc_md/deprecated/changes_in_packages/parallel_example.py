#
# This example does not work with the standard multiprocessing package.
# Furhtermore, it also does not work with pathos or multiprocessing_on_dill
# when we use the packages as they come.
#
# Some hacks on dill and multiprocessing_on_dill make it work.
# 
# author: goujou, 2017


from multiprocessing_on_dill import Pool as Pool
import numpy as np

from scipy.integrate import odeint
from sympy import Symbol, lambdify, flatten, Matrix, symbols, sin, pi

def get_numerical_rhs(symbolic_rhs, state_vector, time_symbol, parameter_dict):
    args = tuple(state_vector) + (time_symbol,)
    rhs_par = symbolic_rhs.subs(parameter_dict)

    # this line would be preferred, but it fails to dill 
    # even using the hacked versions of dill and multiprocessing_on_dill
    #FL = lambdify(args, rhs_par, modules = 'numpy') 

    # so we have to use these lines
    d = {'ImmutableMatrix': np.matrix, 'sin': np.sin, 'pi': np.pi}
    FL = lambdify(args, rhs_par, modules = d)

    def num_rhs(X, t):
        args = tuple(X) + (t,)
        Fval = FL(*args)
        return flatten(Fval.tolist())

    return num_rhs


class ModelRun():
    def __init__(self, symbolic_rhs, state_vector, time_symbol, times, parameter_dict):
        self.symbolic_rhs = symbolic_rhs
        self.state_vector = state_vector
        self.time_symbol = time_symbol
        self.times = times
        self.parameter_dict = parameter_dict
    
        self.initialize_sol_func()

    def initialize_sol_func(self):
        numerical_rhs = get_numerical_rhs(self.symbolic_rhs, 
                                          self.state_vector,
                                          self. time_symbol,
                                          self.parameter_dict)

        def sol_func(start_vector):
            return odeint(numerical_rhs, start_vector, self.times, mxstep=10000)[-1]

        self.sol_func = sol_func

    def compute(self, list_of_start_vectors, parallel):
        sol_func = self.sol_func

        def function_to_dill(start_vector):
            return sol_func(start_vector)

        if parallel:
            pool = Pool(processes=len(list_of_start_vectors))
            list_of_results = pool.map(function_to_dill, list_of_start_vectors)
        else:
            list_of_results = [function_to_dill(sv) for sv in list_of_start_vectors]

        return np.array(list_of_results)
            


if __name__ == '__main__':
    C_1, C_2, alpha, beta, t = symbols('C_1 C_2 alpha beta t')
    A = Matrix([[-alpha * 0.1*(2+sin(2*pi/10*t)),            0.5*beta],
                [                      0.5*alpha, -beta*(1/C_2**2**2)]])
    state_vector = Matrix([[C_1], 
                           [C_2]])
    input_vector = Matrix([[C_1/C_2],
                           [  1]])
    
    symbolic_rhs = A*state_vector + input_vector
    times = np.linspace(0, 10, 101)
    parameter_dict = {'alpha': 1,
                      'beta' : 2}

    mr = ModelRun(symbolic_rhs, state_vector, t, times, parameter_dict)
    
    n = 10
    list_of_start_vectors = [np.array([np.abs(np.random.normal(10, 2)),
                                       np.abs(np.random.normal(20, 4))]) for _ in range(n)]

    s_results = mr.compute(list_of_start_vectors, False)
    print('serial:\n\n', s_results)

    print()

    p_results = mr.compute(list_of_start_vectors, True)
    print('parallel:\n\n', p_results)



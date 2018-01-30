from sympy import symbols, Matrix, solve, lambdify, flatten

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

class Wang():

    @classmethod
    def steady_state(cls):
        f = Matrix(2, 1, [-V*y*x/(x+K) + mu*y + u,
                               epsilon*V*y*x/(x+K) - mu*y])

        sv = Matrix(2, 1, [x, y])
        ss = solve(f, sv, dict=True)
        x_ss = ss[0][x]

        y_ss = ss[0][y]
        ss = Matrix(2, 1, [x_ss, y_ss])
        
        return [ss[0], ss[1]]


    def __init__(self, par_dict, start_values):

        self.f = Matrix(2, 1, [-V*y*x/(x+K) + mu*y + u,
                               epsilon*V*y*x/(x+K) - mu*y])
        self.pd = par_dict
        self.start_values = start_values


    def solve(self, times):
        f_par = self.f.subs(self.pd)
        lam_F = lambdify([x, y, t], f_par)

        def rhs(X, t):
            Xt = tuple(X) + (t,)
            val = lam_F(*Xt)
            return flatten(val.tolist())

        soln = odeint(rhs, self.start_values, times)
        return soln

x, y, V, epsilon, K, mu, u, t = symbols('x y V epsilon K mu u t', positive=True)

N = 100
base_pd = {V: 59.13, K: 53954, mu: 4.38, epsilon: 0.39, u: 345}
base_iv = {'x0': 13000.0, 'y0': 50.0}

par_spread = 0
iv_spread = 0.01

models = []
ss = Wang.steady_state()

for i in range(N):
    iv_x, iv_y = [-1, -1]

    pd = {V: 1, epsilon: 1, mu: 2}
    # v*epsilon/u>1 necessary for positive steady state solution
    while pd[V]*pd[epsilon]/pd[mu] <= 1:
        for par in [V, K, mu, epsilon, u]:
            val = -1
            while val<0:
                if par_spread == 0:
                    val = base_pd[par]
                else:
                    val = np.random.normal(base_pd[par], par_spread * base_pd[par])

            pd[par] = val

    ss_vec = [ss[0].subs(pd), ss[1].subs(pd)]
    #print(ss_vec)

    # attention! model seems ot to converge to fixed point when iv_x < 5325!!!
    while(iv_x<0 or iv_y<0):
        iv_x = np.random.normal(ss_vec[0], iv_spread * ss_vec[0])
        #iv_x = 5000
        iv_y = np.random.normal(ss_vec[1], iv_spread * ss_vec[1])

    models.append(Wang(pd, [iv_x, iv_y]))


times = np.arange(0, 300, 0.1)

sols = np.array([model.solve(times) for model in models])
for i in range(N):
    plt.plot(times, sols[i,:,0])
    print(models[i].start_values, sols[i,-1,:])

plt.show()

for i in range(N):
    plt.plot(sols[i,:,0], sols[i,:,1])

plt.show()

mean_iv_x = sum([model.start_values[0] for model in models])/N
mean_iv_y = sum([model.start_values[1] for model in models])/N

mean_ss = sols.sum(0)[-1,:]/N
print([mean_iv_x, mean_iv_y], mean_ss)

mean_model = Wang(base_pd, [mean_iv_x, mean_iv_y])
sol = mean_model.solve(times)

#plt.plot(times, sols[1,:, 0], label = 'mean model')
#plt.plot(times, sols.sum(0)[:,0]/N, label = 'model mean')
plt.plot(sols.sum(0)[:,0]/N, sols.sum(0)[:,1]/N, label = 'model mean')
plt.legend()

plt.show()


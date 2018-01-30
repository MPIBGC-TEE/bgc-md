# vim:set ff=unix expandtab ts=4 sw=4:
import unittest
import sys
from concurrencytest import ConcurrentTestSuite, fork_for_tests

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sympy import Matrix, symbols, sin, Piecewise, DiracDelta

from bgc_md.helpers_reservoir import factor_out_from_matrix, parse_input_function, melt, MH_sampling, stride

class TestHelpers_reservoir(unittest.TestCase):

    def test_parse_input_function(self):
        t = symbols('t')
        u = 1+sin(t) + DiracDelta(2-t) +5*DiracDelta(3-t) + Piecewise((1,t<=1), (2,True))
        impulses, jump_times = parse_input_function(u, t)
        self.assertEqual(impulses, [{'time': 2, 'intensity': 1}, {'time': 3,'intensity': 5}])
        self.assertEqual(jump_times, [1,2,3])

        u = 1
        impulses, jump_times = parse_input_function(u, t)
        self.assertEqual(impulses, [])
        self.assertEqual(jump_times, [])


    def test_factor_out_from_matrix(self):
        gamma, k_1 = symbols('gamma k_1')
        M = Matrix([[12*gamma*k_1, 0], [3*gamma**2, 15*gamma]])
        cf = factor_out_from_matrix(M)

        self.assertEqual(cf, 3*gamma)


    def test_melt(self):
        ndarr = np.arange(24).reshape(3,4,2)
        
        a_ref = [[0,  0,  0,  0], 
                 [0,  0,  1,  1],
                 [0,  1,  0,  2],
                 [0,  1,  1,  3],
                 [0,  2,  0,  4],
                 [0,  2,  1,  5],
                 [0,  3,  0,  6],
                 [0,  3,  1,  7],
                 [1,  0,  0,  8],
                 [1,  0,  1,  9],
                 [1,  1,  0, 10],
                 [1,  1,  1, 11],
                 [1,  2,  0, 12],
                 [1,  2,  1, 13],
                 [1,  3,  0, 14],
                 [1,  3,  1, 15],
                 [2,  0,  0, 16],
                 [2,  0,  1, 17],
                 [2,  1,  0, 18],
                 [2,  1,  1, 19],
                 [2,  2,  0, 20],
                 [2,  2,  1, 21],
                 [2,  3,  0, 22],
                 [2,  3,  1, 23]]
        ref = np.array(a_ref).reshape((24,4))
        melted = melt(ndarr)
        self.assertTrue(np.all(melted==ref))

        ages = np.linspace(0,4,3)
        times = np.linspace(0,0.75,4)
        pools = [0,1]

        a_ref = [[0.,     0.  ,   0.,     0.  ], 
                 [0.,     0.  ,   1.,     1.  ],
                 [0.,     0.25,   0.,     2.  ],
                 [0.,     0.25,   1.,     3.  ],
                 [0.,     0.5 ,   0.,     4.  ],
                 [0.,     0.5 ,   1.,     5.  ],
                 [0.,     0.75,   0.,     6.  ],
                 [0.,     0.75,   1.,     7.  ],
                 [2.,     0.  ,   0.,     8.  ],
                 [2.,     0.  ,   1.,     9.  ],
                 [2.,     0.25,   0.,    10.  ],
                 [2.,     0.25,   1.,    11.  ],
                 [2.,     0.5 ,   0.,    12.  ],
                 [2.,     0.5 ,   1.,    13.  ],
                 [2.,     0.75,   0.,    14.  ],
                 [2.,     0.75,   1.,    15.  ],
                 [4.,     0.  ,   0.,    16.  ],
                 [4.,     0.  ,   1.,    17.  ],
                 [4.,     0.25,   0.,    18.  ],
                 [4.,     0.25,   1.,    19.  ],
                 [4.,     0.5 ,   0.,    20.  ],
                 [4.,     0.5 ,   1.,    21.  ],
                 [4.,     0.75,   0.,    22.  ],
                 [4.,     0.75,   1.,    23.  ]]
        melted = melt(ndarr, [ages, times, pools])
        ref = np.array(a_ref).reshape((24,4))
        self.assertTrue(np.all(melted==ref))

    def test_MH_sampling(self):
        # uniform distribution on [0,1]
        PDF = lambda x: 1 if x>=0 and x<=1 else 0
        rvs = MH_sampling(100000, PDF)
        self.assertTrue(abs(np.mean(rvs)-0.5) < 0.01)
        self.assertTrue(abs(np.std(rvs, ddof=1)-np.sqrt(1/12)) < 0.01)

        # exponential distribution
        l = 2
        PDF = lambda x: l*np.exp(-l*x)
        rvs = MH_sampling(100000, PDF, start = 1/l)
        #print(rvs)
        #print(np.mean(rvs))
        #count, bins, ignored = plt.hist(rvs, 100, normed=True)
        #ts = np.linspace(0, 5, 101)
        #plt.plot(ts, [PDF(t) for t in ts], color='red')
        #plt.show()
        self.assertTrue(abs(np.mean(rvs)-1/l) < 0.01)
        self.assertTrue(abs(np.std(rvs, ddof=1)-1/l) < 0.01)


    def test_stride(self):
        data = np.array([i*10+np.linspace(0,9,10) for i in range(20)])
        strided_data = stride(data, (2,4))
        ref = np.array([[   0.,    4.,    8.,    9.], 
                        [  20.,   24.,   28.,   29.],
                        [  40.,   44.,   48.,   49.],
                        [  60.,   64.,   68.,   69.],
                        [  80.,   84.,   88.,   89.],
                        [ 100.,  104.,  108.,  109.],
                        [ 120.,  124.,  128.,  129.],
                        [ 140.,  144.,  148.,  149.],
                        [ 160.,  164.,  168.,  169.],
                        [ 180.,  184.,  188.,  189.],
                        [ 190.,  194.,  198.,  199.]])
        self.assertTrue(np.all(strided_data==ref))

        times = np.linspace(0,100,101)
        strided_times = stride(times, 25)
        self.assertTrue(np.all(strided_times==np.array([0,25,50, 75, 100])))
        
        strided_times = stride(times, 1)
        self.assertTrue(np.all(strided_times==times))



####################################################################################################


if __name__ == '__main__':
    suite=unittest.defaultTestLoader.discover(".",pattern=__file__)
    # Run same tests across 16 processes
    concurrent_suite = ConcurrentTestSuite(suite, fork_for_tests(16))
    runner = unittest.TextTestRunner()
    res=runner.run(concurrent_suite)
    # to let the buildbot fail we set the exit value !=0 if either a failure or error occurs
    if (len(res.errors)+len(res.failures))>0:
        sys.exit(1)


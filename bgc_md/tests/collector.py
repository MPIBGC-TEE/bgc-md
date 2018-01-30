# vim:set ff=unix expandtab ts=4 sw=4:
# this scripts 
import unittest
def all_tests():
    print("################################### running tests ################################")
    s=unittest.defaultTestLoader.discover(example_package.tests.__path__[0],pattern="Test*")
    r=unittest.TextTestRunner()
    r.run(s)
    return(0) #(this should be 1 if something goes wrong)

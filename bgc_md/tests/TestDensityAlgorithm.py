# vim: set ff=unix expandtab ts=4 sw=4:
import unittest

if __name__ == "__main__":
    s=unittest.defaultTestLoader.discover(".", pattern=__file__)
    s.addTests(unittest.defaultTestLoader.discover(".", pattern="TestTsTpMassField.py"))
    s.addTests(unittest.defaultTestLoader.discover(".", pattern="TestTsTpField.py"))
    s.addTests(unittest.defaultTestLoader.discover(".", pattern="TestTsTpMassFieldsPerPool.py"))
    s.addTests(unittest.defaultTestLoader.discover(".", pattern="TestTsTpMassFieldsPerPipe.py"))
    s.addTests(unittest.defaultTestLoader.discover(".", pattern="TestCompatibleTsTpMassFieldsPerPool.py"))
    
    r=unittest.TextTestRunner()
    r.run(s)
    

# vim:set ff=unix expandtab ts=4 sw=4:
import unittest
import pathlib
import os
import sys
from string import Template
from subprocess import call,check_call,check_output
#from pythonPackage.LvBackup import LvBackup
#from pythonPackage.VmBackup import VmBackup

class InDirTest(unittest.TestCase):

    def myDirPath():
        myDirPath=pathlib.Path(__file__).absolute().parent
        return(myDirPath)

        
    def tmpDirPath():
        return(__class__.myDirPath().joinpath("tmp"))
        

    def run(self,*args):
        testDirPath=__class__.tmpDirPath().joinpath(self.id())
        testDirName=testDirPath.as_posix()

        self.oldDirName=os.getcwd()
        __class__.rootDir=pathlib.Path(self.oldDirName).parent.parent
        check_output(["rm","-rf",testDirName])
        check_output(["mkdir","-p",testDirName])
        print("testDirName")
        print(testDirName)
        
        os.chdir(testDirName)
        
        try:
            super().run(*args)
        finally:
            os.chdir(self.oldDirName)


from JackTokenizer import * 
from CompilationEngine import *
import os
import sys


def directoryCompiler(path):
    #path=os.path.abspath(path)
    if(os.path.isfile(path)):
        
        t=JackTokenizer(path)
        j=CompilationEngine(t,path[0:-5]+".vm")
        j.compile()
    else:
        for file in os.listdir(path):
            if file.endswith(".jack"):
                        print(path+"/"+file)
                        t=JackTokenizer(path+"/"+file)
                        j=CompilationEngine(t,path+"/"+file[0:-5]+".vm")
                        j.compile()
path=sys.argv[1]
directoryCompiler(path)
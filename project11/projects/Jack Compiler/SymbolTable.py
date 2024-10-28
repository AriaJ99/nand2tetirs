class SymbolTable:
    def __init__(self):
        self.table={}
        self.kindCount={
            "static": 0,
            "field" : 0,
            "argument" : 0,
            "var" : 0,
            "function" : 0,
            "method" : 0,
            "constructor" : 0
        }
    def reset(self):
        #reset the table
        self.table={}
        self.kindCount={
            "static": 0,
            "field" : 0,
            "argument" : 0,
            "var" : 0,
            "function" : 0,
            "method" : 0,
            "constructor" : 0
        }
    def define(self,name,type,kind,nArgs=0,nVars=0):
        if kind in ["method", "constructor", "function"]:
            self.table[name]=[type,kind,self.kindCount[kind],nArgs,nVars]
        else:
            self.table[name]=[type,kind,self.kindCount[kind]]
        self.kindCount[kind]+=1
    def varCount(self,kind):
        return self.kindCount[kind]
    def kindOf(self,name):
        #check existance
        if not name in self.table:
            return None
        return self.table[name][1]
    def typeOf(self,name):
        #check existance
        if not name in self.table:
            return None
        return self.table[name][0]
    def indexOf(self,name):
        #check existance
        if not name in self.table:
            return None
        return self.table[name][2]
    def nArgsOf(self,name):
        #check existance
        if not name in self.table:
            return None
        return self.table[name][3]
    def nVarsOf(self,name):
        #check existance
        if not name in self.table:
            return None
        return self.table[name][4]



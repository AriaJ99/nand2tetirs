keywords = [
    'class', 'constructor', 'function', 'method',
    'field', 'static', 'var', 'int', 'char', 'boolean',
    'void', 'true', 'false', 'null', 'this', 'let',
    'do', 'if', 'else', 'while', 'return'
]

symbols = [
    '{', '}', '(', ')', '[', ']', '.', ',', ';',
    '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'
]
class JackTokenizer:

    def __init__(self, jackFilePath):
        file = open(jackFilePath, "r")
        self.codeContent=file.read();
        file.close()

        self.position=-1;
        self.token=""
        self.tokenType=""
        self.keyWord=""
    def hasMoreTokens(self):
        #check if threre's still token left
        if(self.codeContent[self.position+1]!=""):
            return True
        return False
    def advance(self):
        if(not self.hasMoreTokens()):
            return
        

    def tokenType(self):
        return self.tokenType
    def keyWord(self):
        return self.keyWord
    def symbol(self):
        pass
    def identifies(self):
        pass
    def intVal(self):
        pass
    def stringVal(self):
        pass


j=JackTokenizer("jj.jack")
print(j.hasMoreTokens())


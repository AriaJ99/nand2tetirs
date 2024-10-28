import os
import sys
keywords = [
    'class', 'constructor', 'function', 'method',
    'field', 'static', 'var', 'int', 'char', 'boolean',
    'void', 'true', 'false', 'null', 'this', 'let',
    'do', 'if', 'else', 'while', 'return'
]
tokentypes=[
    "keyword",
    "symbol",
    "identifier",
    "integerConstant",
    "stringConstant"
]
symbols = [
    '{', '}', '(', ')', '[', ']', '.', ',', ';',
    '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'
]
#the tokens that should be changed to be compatible with browsers
should_change=True
changables="<>\"&"
change ={
    '<':'<',
    '>':'>',
    '\"':'\"',
    '&':'&',
}       

def match_keyword(input):
    for word in keywords:
        if(word in input[0:len(word)]):
            if(not input[len(word)].isalpha()):
                return word
    return None
def xml_wrap(name,tag):
    return f"<{tag}> {name} </{tag}>\n"


class JackTokenizer:

    def __init__(self, jackFilePath):
        file = open(jackFilePath, "r")
        self.codeContent=file.read();
        file.close()
        self.position=0;
        self.token=None
        self.tokenType=""
        #previous token tuple [-1,-2]
        self.prevTokens=[(None,""),(None,"")]
        self.preprocess()
    def preprocess(self):
        #remove comments
        #print(self.codeContent)
        pos=0
        double_qou=False
        while(pos<len(self.codeContent)):
            if(self.codeContent[pos]=='\"'):
                double_qou=not double_qou
            if(self.codeContent[pos]=='/' and double_qou==False):
                #// coments
                if(self.codeContent[pos+1]=='/'):
                    while(self.codeContent[pos]!='\n'):
                        self.codeContent=self.codeContent[:pos]+self.codeContent[pos+1:]
                    self.codeContent=self.codeContent[:pos]+self.codeContent[pos+1:]
                    pos-=1
                # /* */ comments
                elif(self.codeContent[pos+1]=='*'):
                    self.codeContent=self.codeContent[:pos]+self.codeContent[pos+1:]
                    
                    while(self.codeContent[pos:pos+2]!="*/"):
                        self.codeContent=self.codeContent[:pos]+self.codeContent[pos+1:]
                    self.codeContent=self.codeContent[:pos]+self.codeContent[pos+2:]
            
            
            pos+=1
        #print(self.codeContent)
                
            
    def hasMoreTokens(self):
        #check if threre's still token left
        if(self.position==len(self.codeContent)):
            return False
        while(self.codeContent[self.position] in [' ','\n','\t']):
            self.position+=1
            if(self.position==len(self.codeContent)):
                return False
        return True
    def advance(self):
        #take the next token
        if(not self.hasMoreTokens()):
            return
        self.prevTokens[1]=self.prevTokens[0]
        self.prevTokens[0]=((self.token,self.tokenType))
        self.token=""
        
        if(self.codeContent[self.position]=='\"'):
            #const string
            self.tokenType=tokentypes[4]
            while(self.codeContent[self.position+1]!='\"'):
                self.position+=1
                self.token+=self.codeContent[self.position]
            self.position+=1
        elif(self.codeContent[self.position] in symbols):
            #symbol
            #print(self.codeContent[self.position])
            self.tokenType=tokentypes[1]
            self.token=self.codeContent[self.position]
            #print(self.token)
            if(self.codeContent[self.position] in changables and should_change):
                self.token=change[self.codeContent[self.position]]
            

        elif(self.codeContent[self.position].isdigit()):
            #const int
            self.tokenType=tokentypes[3]
            while(self.codeContent[self.position].isdigit()):
                self.token+=self.codeContent[self.position]
                self.position+=1
            self.position-=1
        elif(match_keyword(self.codeContent[self.position:])!=None):
            #keyword
            self.token=match_keyword(self.codeContent[self.position:])
            self.position+=len(self.token)-1
            self.tokenType=tokentypes[0]
        else:
            #identifier
            self.tokenType=tokentypes[2]

            while(self.codeContent[self.position].isalpha() or self.codeContent[self.position].isdigit() or self.codeContent[self.position]=='_'):
                #print(self.codeContent[self.position])
                self.token+=self.codeContent[self.position]
                self.position+=1
            self.position-=1
        self.position+=1
        #print(self.token)
        return (self.token,self.tokenType)
    def getTokenType(self):
        return self.tokenType
    def getToken(self):
        return self.token
    def getFirstLastToken(self):
        return self.prevTokens[0]
    def getSecondLastToken(self):
        return self.prevTokens[1]
    def create_token_file(self,token_file_path):
        #create the xml file for tokenizer
        #print("loop")
        file=open(token_file_path,"w")
        file.write("<tokens>\n")
        while(self.hasMoreTokens()):
            self.advance()
            file.write(f"<{self.tokenType}> ")
            file.write(self.token)
            file.write(f" </{self.tokenType}>\n")
        file.write("</tokens>")
        file.close()

        




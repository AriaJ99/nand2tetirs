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
    '<':'&lt;',
    '>':'&gt;',
    '\"':'&quot;',
    '&':'&amp;',
}       

def match_keyword(input):
    for word in keywords:
        if(word in input[0:len(word)]):
            return word
    return None



class JackTokenizer:

    def __init__(self, jackFilePath):
        file = open(jackFilePath, "r")
        self.codeContent=file.read();
        file.close()
        self.position=-1;
        self.token=None
        self.tokenType=""
        self.preprocess()
    def preprocess(self):
        #remove comments
        pos=0
        double_qou=False
        while(pos<len(self.codeContent)):
            if(self.codeContent[pos]=='\"'):
                double_qou=not double_qou
            if(self.codeContent[pos]=='/' and double_qou==False):
                if(self.codeContent[pos+1]=='/'):
                    while(self.codeContent[pos]!='\n'):
                        self.codeContent=self.codeContent[:pos]+self.codeContent[pos+1:]
                    self.codeContent=self.codeContent[:pos]+self.codeContent[pos+1:]
                    pos-=1
                elif(self.codeContent[pos+1]=='*'):
                    self.codeContent=self.codeContent[:pos]+self.codeContent[pos+1:]
                    
                    while(self.codeContent[pos:pos+2]!="*/"):
                        self.codeContent=self.codeContent[:pos]+self.codeContent[pos+1:]
                    self.codeContent=self.codeContent[:pos]+self.codeContent[pos+2:]
            
            
            pos+=1
                
                
            
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
            self.tokenType=tokentypes[1]
            self.token=self.codeContent[self.position]
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
    def tokenType(self):
        return self.tokenType
    def token(self):
        return self.token
    def creat_token_file(self,token_file_path):
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

j=JackTokenizer("E:/Abo akademi/2024-2025/period 1/Software Construction/nand2tetirs/project10/Main.jack")
#s="abcd"
#print(changables)
#print(j.codeContent)
j.creat_token_file("E:/Abo akademi/2024-2025/period 1/Software Construction/nand2tetirs/project10/MainTokenizer.xml")


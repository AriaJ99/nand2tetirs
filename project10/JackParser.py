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
def xml_wrap(name,tag):
    return f"<{tag}> {name} </{tag}>\n"


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
        return (self.token,self.tokenType)
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
class CompilationEngine:
    def __init__(self, tokenizer):
        #get the tokenizer
        self.tokenizer=tokenizer
        #to store the parsed code
        self.parsedCode=""
        #status of the current token
        self.currentTokenChecked=False
    def compileClass(self):
        self.parsedCode+="<class>\n"
        #class token
        token,tokenType=self.tokenizer.token(), self.tokenizer.tokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        #class name
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #{ symbol
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #classVarDec
        (token,tokenType)=self.tokenizer.advance()
        while(token in ["static", "field"]):
            self.compileClassVarDec()
            (token,tokenType)=self.tokenizer.advance()
        #subRoutineDec
        while(token in ["constructor","function","method"]):
            self.compileSubroutine()
            (token,tokenType)=self.tokenizer.advance()
        #} symbol don't need advance it was done previously
        self.parsedCode+=xml_wrap(token,tokenType)
        self.parsedCode+="</class>\n"
        self.currentTokenChecked=True
    def compileClassVarDec(self):
        self.parsedCode+="<classVarDec>\n"
        #static or field
        token,tokenType=self.tokenizer.token(), self.tokenizer.tokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        #var type
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #name token
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #; or more vars?
        (token,tokenType)=self.tokenizer.advance()
        while(token==','):
            #, symbol
            self.parsedCode+=xml_wrap(token,tokenType)
            #name token
            (token,tokenType)=self.tokenizer.advance()
            self.parsedCode+=xml_wrap(token,tokenType)
            #next round
            (token,tokenType)=self.tokenizer.advance()
        #; symbol don't need advance it was done previously
        self.parsedCode+=xml_wrap(token,tokenType)
        self.parsedCode+="</classVarDec>\n"
        self.currentTokenChecked=True        
        
    def compileSubroutine(self):
        self.parsedCode+="<subroutineDec>\n"
        #constructor function method token
        token,tokenType=self.tokenizer.token(), self.tokenizer.tokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        #var type
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #name token
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #( symbol
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #parameter list check if there's any
        (token,tokenType)=self.tokenizer.advance()
        self.compileParameterList()
        #) symbol don't need advance it was done previously by parameter list
        self.parsedCode+=xml_wrap(token,tokenType)
        #subroutine body
        self.tokenizer.advance()
        self.compileSubroutineBody()
        self.parsedCode+="</subroutineDec>\n"
        self.currentTokenChecked=True   
    def compileParameterList(self):
        self.parsedCode+="<parameterList>\n"
        #static or field
        token,tokenType=self.tokenizer.token(), self.tokenizer.tokenType()
        self.parsedCode+=xml_wrap(token,tokenType)

        #check if there's any variable
        (token,tokenType)=self.tokenizer.advance()
        #check if the tokentype is keyword(in this case there's variable if it's symbol we should skip)
        if(tokenType=="keyword"):
            #first var
            #var type
            self.parsedCode+=xml_wrap(token,tokenType)
            #name token
            (token,tokenType)=self.tokenizer.advance()
            self.parsedCode+=xml_wrap(token,tokenType)
            #, symbol for loop
            (token,tokenType)=self.tokenizer.advance()
            while(tokenType==","):
                #var type
                self.parsedCode+=xml_wrap(token,tokenType)
                #name token
                (token,tokenType)=self.tokenizer.advance()
                self.parsedCode+=xml_wrap(token,tokenType)
                #next symbol(either , or ')')
                (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+="</parameterList>\n"
        self.currentTokenChecked=False     
    def compileSubroutineBody(self):
        self.parsedCode+="<subroutineBody>\n"
        #{ symbol
        token,tokenType=self.tokenizer.token(), self.tokenizer.tokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        #var dec check for var decleration
        (token,tokenType)=self.tokenizer.advance()
        if(token=="var"):
            # var keyword
            self.parsedCode+=xml_wrap(token,tokenType)
            # type
            (token,tokenType)=self.tokenizer.advance()
            self.parsedCode+=xml_wrap(token,tokenType)
            # name 
            (token,tokenType)=self.tokenizer.advance()
            self.parsedCode+=xml_wrap(token,tokenType)
            #look for , or statements
            (token,tokenType)=self.tokenizer.advance()
            while(token==","):
                #, symbol
                self.parsedCode+=xml_wrap(token,tokenType)
                # type
                (token,tokenType)=self.tokenizer.advance()
                self.parsedCode+=xml_wrap(token,tokenType)
                # name 
                (token,tokenType)=self.tokenizer.advance()
                self.parsedCode+=xml_wrap(token,tokenType)
                #next round
                (token,tokenType)=self.tokenizer.advance()
        #statements
        self.currentTokenChecked=False
        self.compileStatments()
        #( symbol
        #(token,tokenType)=self.tokenizer.advance() ####################################need to be completed due to statements
        if(not self.currentTokenChecked):
            #if last token is raw it's } else we should advance
            (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        self.parsedCode+="</subroutineBody>\n"
        self.currentTokenChecked=True   
    def compileVarDec(self):
        self.parsedCode+="<varDec>\n"
        #var token
        token,tokenType=self.tokenizer.token(), self.tokenizer.tokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        #var type
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #name token
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #; or more vars?
        (token,tokenType)=self.tokenizer.advance()
        while(token==','):
            #, symbol
            self.parsedCode+=xml_wrap(token,tokenType)
            #name token
            (token,tokenType)=self.tokenizer.advance()
            self.parsedCode+=xml_wrap(token,tokenType)
            #next round
            (token,tokenType)=self.tokenizer.advance()
        #; symbol don't need advance it was done previously
        self.parsedCode+=xml_wrap(token,tokenType)
        self.parsedCode+="</varDec>\n"
        self.currentTokenChecked=True   
    def compileStatments(self):
        # statement*
        self.parsedCode+="<statements>\n"
        #statement let if while do return
        token,tokenType=self.tokenizer.token(), self.tokenizer.tokenType()
        while(token in ["if","while","let","do","return"]):
            match token:
                case "if":
                    self.compileIf()
                case "while":
                    self.compileWhile
                case "let":
                    self.compileLet()
                case "do":
                    self.compileDo()
                case "return":
                    self.compileReturn()
                case defualt:
                    pass
            token,tokenType=self.tokenizer.token(), self.tokenizer.tokenType()
        self.currentTokenChecked=False
        self.parsedCode+="</statements>\n"
    def compileLet(self):
        #'let' varName ('[' expression ']')? '=' expression ';' 
        self.parsedCode+="<letStatement>\n"
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        #let token
        token,tokenType=self.tokenizer.token(), self.tokenizer.tokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        #name token
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #[ or = symbol
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        if(token=="["):
            #expression
            (token,tokenType)=self.tokenizer.advance()
            self.compileExpression()
            #) symbol
            (token,tokenType)=self.tokenizer.advance()
            self.parsedCode+=xml_wrap(token,tokenType)
            #= symbol
            (token,tokenType)=self.tokenizer.advance()
            self.parsedCode+=xml_wrap(token,tokenType)
        #expression
        (token,tokenType)=self.tokenizer.advance()
        self.compileExpression()
        if(self.currentTokenChecked):
            (token,tokenType)=self.tokenizer.advance()
        #; symbol
        self.parsedCode+=xml_wrap(token,tokenType)
        self.parsedCode+="</letStatement>\n"
        self.currentTokenChecked=True

    def compileIf(self):
        #'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}' )?
        self.parsedCode+="<ifStatement>\n"
        #if token
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.token(), self.tokenizer.tokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        #( symbol
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #expression
        self.compileExpression()
        #) symbol
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #{ symbol
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #statements
        self.compileStatments()
        #} symbol
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #check if there's else
        (token,tokenType)=self.tokenizer.advance()
        if(token=="else"):
            #else token
            self.parsedCode+=xml_wrap(token,tokenType)
            #{ symbol
            (token,tokenType)=self.tokenizer.advance()
            self.parsedCode+=xml_wrap(token,tokenType)
            #statements
            self.compileStatments()
            #} symbol
            (token,tokenType)=self.tokenizer.advance()
            self.parsedCode+=xml_wrap(token,tokenType)
            self.currentTokenChecked=True

        self.parsedCode+="</ifStatement>\n"
        
    def compileWhile(self):
        #'while' '(' expression ')' '{' statements '}'
        self.parsedCode+="<whileStatement>\n"
        #while token
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.token(), self.tokenizer.tokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        #( symbol
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #expression
        self.compileExpression()
        #) symbol
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #{ symbol
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #statements
        self.compileStatments()
        #} symbol
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)

        #end
        self.parsedCode+="</whileStatement>\n"
        self.currentTokenChecked=True
    def compileDo(self):
        # 'do' subroutineCall ';'
        self.parsedCode+="<doStatement>\n"
        #do token
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.token(), self.tokenizer.tokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        #subroutineCall#######################################################################################fix this
        self.compileSubroutine()
        #; symbol
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #end
        self.parsedCode+="</doStatement>\n"
        self.currentTokenChecked=True
    def compileReturn(self):
        # 'return' expression? ':'
        self.parsedCode+="<returnStatement>\n"
        #return token
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.token(), self.tokenizer.tokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        (token,tokenType)=self.tokenizer.advance()
        #check if there's subroutincall or semicolomn
        if(token==";"):
            self.parsedCode+=xml_wrap(token,tokenType)
        else:
            self.compileSubroutine()
            #; symbol
            (token,tokenType)=self.tokenizer.advance()
            self.parsedCode+=xml_wrap(token,tokenType)
        #end
        self.parsedCode+="</returnStatement>\n"
        self.currentTokenChecked=True
    def compileExpression(self):
        # term (op term)*
        self.parsedCode+="<statements>\n"
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        #term 
        self.compileTerm()
        (token,tokenType)=self.tokenizer.advance()
        while(token in ["+","-","*","/","&","|","<",">","="]):
            #op symbol
            self.parsedCode+=xml_wrap(token,tokenType)
            #term
            self.tokenizer.advance()
            self.compileTerm()
            #next token
            self.tokenizer.advance()
        self.currentTokenChecked=False

        self.parsedCode+="</statements>\n"
        pass
    def compileTerm(self):
        # integerConstant|stringConstant|keywordConstant|varName|varName '[' expression ']'|subroutineCall|'('expression')'|unaryOp term
        self.parsedCode+="<statements>\n"
        #statement let if while do return
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.token(), self.tokenizer.tokenType()
        if(tokenType=="integerConstant"):
            pass
        elif(tokenType=="stringConstant"):
            pass
        elif(token in ["true","false","null","this"]):
            #keywordConstant
            pass
        elif(token in ["-" , "~"]):
            pass
        else:
            #varName|varName '[' expression ']'|subroutineCall|'('expression')' 




            token,tokenType=self.tokenizer.token(), self.tokenizer.tokenType()
        self.currentTokenChecked=False
        self.parsedCode+="</statements>\n"
    def compileExpressionList(self):
        # (expression(','expression)*)?
        self.parsedCode+="<expressionList>\n"
        token=""
        if(self.currentTokenChecked):
            (token,tokenType)=self.tokenizer.advance()
            self.currentTokenChecked=False
        #check if there's expression
        if(token!=')'):
            #expression
            self.compileExpression()
            #check for more
            (token,tokenType)=self.tokenizer.advance()
            while(token==','):
                #, symbol
                self.parsedCode+=xml_wrap(token,tokenType)
                (token,tokenType)=self.tokenizer.advance()
                self.currentTokenChecked=False
                #expression
                self.compileExpression()
                #next round
                (token,tokenType)=self.tokenizer.advance()

        self.currentTokenChecked=False
        self.parsedCode+="</expressionList>\n"
        
j=JackTokenizer("E:/Abo akademi/2024-2025/period 1/Software Construction/nand2tetirs/project10/Main.jack")
#s="abcd"
#print(changables)
#print(j.codeContent)
j.creat_token_file("E:/Abo akademi/2024-2025/period 1/Software Construction/nand2tetirs/project10/MainTokenizer.xml")

##################################call advance before call a compilexxx and fix them using true or false token checker##############################################
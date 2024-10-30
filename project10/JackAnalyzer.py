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
    def getTokenType(self):
        return self.tokenType
    def getToken(self):
        return self.token
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
class CompilationEngine:
    def __init__(self, jackFilePath):
        #object of the tokenizer
        self.tokenizer=JackTokenizer(jackFilePath)
        #print(type(self.tokenizer))
        #to store the parsed code
        self.parsedCode=""
        #status of the current token
        self.currentTokenChecked=False
    def compileClass(self):
        #'class' className '{'classVarDec* subroutineDec*'}'
        self.parsedCode+="<class>\n"
        #class token
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        #class name
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #{ symbol
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #classVarDec
        (token,tokenType)=self.tokenizer.advance()
        self.currentTokenChecked=False
        while(token in ["static", "field"]):
            self.compileClassVarDec()
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()

        #subRoutineDec
        
        while(token in ["constructor","function","method"]):
            self.compileSubroutineDec()
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        #} symbol don't need advance it was done previously
        
        self.parsedCode+=xml_wrap(token,tokenType)
        self.parsedCode+="</class>\n"
        self.currentTokenChecked=True
    def compileClassVarDec(self):
        #('static'|'field') type varName (','varName)*';'
        self.parsedCode+="<classVarDec>\n"
        #static or field
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
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

    def compileSubroutineDec(self):
        #('cosntructor'|'function'|'method') ('void'|type)subroutineName'('parameterlList')'subroutineBody
        self.parsedCode+="<subroutineDec>\n"
        #constructor function method token
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
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
        self.currentTokenChecked=False
        self.compileParameterList()
        #) symbol don't need advance it was done previously by parameter list
        self.parsedCode+=xml_wrap(token,tokenType)
        #subroutine body
        self.tokenizer.advance()
        self.compileSubroutineBody()
        self.parsedCode+="</subroutineDec>\n"
        self.currentTokenChecked=True   
    def compileParameterList(self):
        #((type varName)(',' type varName)*)?
        self.parsedCode+="<parameterList>\n"
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        #check if there's any
        #self.parsedCode+=xml_wrap(token,tokenType)
        #variable name
        #(token,tokenType)=self.tokenizer.advance()
        #self.parsedCode+=xml_wrap(token,tokenType)
        #check if there's any variable
        #(token,tokenType)=self.tokenizer.advance()
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
            self.currentTokenChecked=False
            while(token==","):
                self.parsedCode+=xml_wrap(token,tokenType)
                #var type
                (token,tokenType)=self.tokenizer.advance()
                self.parsedCode+=xml_wrap(token,tokenType)
                #name token
                (token,tokenType)=self.tokenizer.advance()
                self.parsedCode+=xml_wrap(token,tokenType)
                #next symbol(either , or ')')
                (token,tokenType)=self.tokenizer.advance()
                self.currentTokenChecked=False
        self.parsedCode+="</parameterList>\n"
        
    def compileSubroutineBody(self):
        #'{' varDec* statements'}'
        self.parsedCode+="<subroutineBody>\n"
        #{ symbol
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        #var dec check for var decleration
        (token,tokenType)=self.tokenizer.advance()
        self.currentTokenChecked=False
        while(token=="var"):
            self.compileVarDec()
            #look for , or statements
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
            
        #statements
        self.currentTokenChecked=False
        self.compileStatments()
        #} symbol
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        self.currentTokenChecked=True
        #if(not self.currentTokenChecked):
            #if last token is raw it's } else we should advance
            #(token,tokenType)=self.tokenizer.advance()
        #self.parsedCode+=xml_wrap(token,tokenType)
        self.parsedCode+="</subroutineBody>\n"
        self.currentTokenChecked=True   
    def compileVarDec(self):
        # 'var'type varName (',' varName)*';'
        self.parsedCode+="<varDec>\n"
        #var token
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
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
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        while(token in ["if","while","let","do","return"]):
            match token:
                case "if":
                    self.compileIf()
                case "while":
                    self.compileWhile()
                case "let":
                    self.compileLet()
                case "do":
                    self.compileDo()
                case "return":
                    self.compileReturn()
                case defualt:
                    pass
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        self.parsedCode+="</statements>\n"
    def compileLet(self):
        #'let' varName ('[' expression ']')? '=' expression ';' 
        self.parsedCode+="<letStatement>\n"
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        #let token

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
            self.currentTokenChecked=False
            self.compileExpression()
            #] symbol
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
            self.parsedCode+=xml_wrap(token,tokenType)
            #= symbol
            (token,tokenType)=self.tokenizer.advance()
            self.parsedCode+=xml_wrap(token,tokenType)
        #expression
        (token,tokenType)=self.tokenizer.advance()
        self.currentTokenChecked=False
        self.compileExpression()
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
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
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        #( symbol
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #expression
        self.tokenizer.advance()
        self.currentTokenChecked=False
        self.compileExpression()
        #) symbol
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        #{ symbol
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #statements
        self.tokenizer.advance()
        self.currentTokenChecked=False
        self.compileStatments()
        #} symbol
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        #check if there's else
        (token,tokenType)=self.tokenizer.advance()
        self.currentTokenChecked=False
        if(token=="else"):
            #else token
            self.parsedCode+=xml_wrap(token,tokenType)
            #{ symbol
            (token,tokenType)=self.tokenizer.advance()
            self.parsedCode+=xml_wrap(token,tokenType)
            #statements
            self.tokenizer.advance()
            self.currentTokenChecked=False
            self.compileStatments()
            #} symbol
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
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
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        #( symbol
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #expression
        self.tokenizer.advance()
        self.currentTokenChecked=False
        self.compileExpression()
        #) symbol
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        #{ symbol
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #statements
        self.tokenizer.advance()
        self.currentTokenChecked=False
        self.compileStatments()
        #} symbol
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
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
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        self.currentTokenChecked=True
        #subroutineCall
        # subroutineName or (className|varName)
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        #. or ( symbol
        (token,tokenType)=self.tokenizer.advance()
        self.parsedCode+=xml_wrap(token,tokenType)
        if(token=="."):
            #(className | varName)'.'subroutineName'(' expressionList ')'
            #subroutineName
            (token,tokenType)=self.tokenizer.advance()
            self.parsedCode+=xml_wrap(token,tokenType)
            #( symbol
            (token,tokenType)=self.tokenizer.advance()
            self.parsedCode+=xml_wrap(token,tokenType)
            
            self.tokenizer.advance()
            self.currentTokenChecked=False
            self.compileExpressionList()
            #) symbol
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
            self.parsedCode+=xml_wrap(token,tokenType)
            
            self.currentTokenChecked=True
            
        elif(token=="("):
            #print(self.parsedCode[-80:-1])
            self.tokenizer.advance()
            self.currentTokenChecked=False
            
            self.compileExpressionList()
            #) symbol
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
            self.parsedCode+=xml_wrap(token,tokenType)
            self.currentTokenChecked=True

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
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        self.parsedCode+=xml_wrap(token,tokenType)
        (token,tokenType)=self.tokenizer.advance()
        self.currentTokenChecked=False
        #check if there's subroutincall or semicolomn
        if(token==";"):
            self.parsedCode+=xml_wrap(token,tokenType)
        else:
            self.compileExpression()
            #; symbol
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
            self.parsedCode+=xml_wrap(token,tokenType)
        #end
        self.parsedCode+="</returnStatement>\n"
        self.currentTokenChecked=True
    def compileExpression(self):
        # term (op term)*
        self.parsedCode+="<expression>\n"
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        #term 
        self.compileTerm()
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        
        while(token in ["+","-","*","/",change["&"],"|",change["<"],change[">"],"="]):
            #op symbol
            self.parsedCode+=xml_wrap(token,tokenType)
            #term
            self.tokenizer.advance()
            self.currentTokenChecked=False
            self.compileTerm()
            #next token
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        

        self.parsedCode+="</expression>\n"
        
    def compileTerm(self):
        # integerConstant|stringConstant|keywordConstant|varName|varName '[' expression ']'|subroutineCall|'('expression')'|unaryOp term
        self.parsedCode+="<term>\n"
        #statement let if while do return
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        if(tokenType=="integerConstant"):
            #integer
            self.parsedCode+=xml_wrap(token,tokenType)
            #token answered
            self.currentTokenChecked=True
        elif(tokenType=="stringConstant"):
            #string
            self.parsedCode+=xml_wrap(token,tokenType)
            #token answered
            self.currentTokenChecked=True
        elif(token in ["true","false","null","this"]):
            #keyword constant
            self.parsedCode+=xml_wrap(token,tokenType)
            #token answered
            self.currentTokenChecked=True
        elif(token in ["-" , "~"]):
            #unaryOp
            self.parsedCode+=xml_wrap(token,tokenType)
            #term
            self.tokenizer.advance()
            self.currentTokenChecked=False
            self.compileTerm()
        elif(token=="("):
            #( symbol
            self.parsedCode+=xml_wrap(token,tokenType)
            #expression
            self.tokenizer.advance()
            self.currentTokenChecked=False
            self.compileExpression()
            #)symbol
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
            self.parsedCode+=xml_wrap(token,tokenType)
            self.currentTokenChecked=True
        else:
            #varName|varName '[' expression ']'|subroutineCall|
            # here we have to check a word forward LL(2)
            # so we stored the token and token type to move forward
            prev_token,prev_tokenType=token,tokenType
            #check the next token
            self.tokenizer.advance()
            self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
            # determine the case
            if(token=="["):
                #var Name '[' expression ']'
                #varName
                self.parsedCode+=xml_wrap(prev_token,prev_tokenType)
                #[ symbol
                self.parsedCode+=xml_wrap(token,tokenType)
                #expression
                self.tokenizer.advance()
                self.currentTokenChecked=False
                self.compileExpression()
                #] symbol
                if(self.currentTokenChecked):
                    self.tokenizer.advance()
                    self.currentTokenChecked=False
                token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
                self.parsedCode+=xml_wrap(token,tokenType)
                self.currentTokenChecked=True
            elif(token in ["(" , "."]):
                #subroutineCall
                if(token=="("):
                    #subroutineName
                    self.parsedCode+=xml_wrap(prev_token,prev_tokenType)
                    #( symbol
                    self.parsedCode+=xml_wrap(token,tokenType)
                    #expressionList
                    self.tokenizer.advance()
                    self.currentTokenChecked=False
                    self.compileExpressionList()
                    #) symbol
                    if(self.currentTokenChecked):
                        self.tokenizer.advance()
                        self.currentTokenChecked=False
                    token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
                    self.parsedCode+=xml_wrap(token,tokenType)
                    self.currentTokenChecked=True

                elif(token=="."):
                    #(className | varName)'.'subroutineName'(' expressionList ')'
                    #className|varName
                    self.parsedCode+=xml_wrap(prev_token,prev_tokenType)
                    #. symbol
                    self.parsedCode+=xml_wrap(token,tokenType)
                    #subroutineName
                    (token,tokenType)=self.tokenizer.advance()
                    self.parsedCode+=xml_wrap(token,tokenType)
                    #( symbol
                    (token,tokenType)=self.tokenizer.advance()
                    self.parsedCode+=xml_wrap(token,tokenType)
                    #expressionList
                    self.tokenizer.advance()
                    self.currentTokenChecked=False
                    self.compileExpressionList()
                    #) symbol
                    if(self.currentTokenChecked):
                        self.tokenizer.advance()
                        self.currentTokenChecked=False
                    token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
                    self.parsedCode+=xml_wrap(token,tokenType)
                    self.currentTokenChecked=True
                
            else:
                #var Name
                #tag the previous token
                self.parsedCode+=xml_wrap(prev_token,prev_tokenType)
                #the current token is still unanswered
                self.currentTokenChecked=False
        self.parsedCode+="</term>\n"
    def compileExpressionList(self):
        # (expression(','expression)*)?
        self.parsedCode+="<expressionList>\n"
        
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        #print(token)
        #check if there's expression
        if(token!=')'):
            #expression
            self.compileExpression()
            #check for more
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()    
            
            while(token==','):
                
                #, symbol
                self.parsedCode+=xml_wrap(token,tokenType)
                (token,tokenType)=self.tokenizer.advance()
                self.currentTokenChecked=False
                #expression
                self.compileExpression()
                #next round
                if(self.currentTokenChecked):
                    self.tokenizer.advance()
                    self.currentTokenChecked=False
                token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()

        
        self.parsedCode+="</expressionList>\n"
    def create_parser_file(self,token_file_path):
        #create xml file for parser 
        #print("loop")
        
        
        self.tokenizer.advance()
        self.compileClass()
            #file.write(self.token)
        file=open(token_file_path,"w")
        file.write(self.parsedCode)
        file.close()

        
j=JackTokenizer("E:/Abo akademi/2024-2025/period 1/Software Construction/nand2tetirs/project10/Square.jack")
#s="abcd"
#print(changables)

#j.create_token_file("E:/Abo akademi/2024-2025/period 1/Software Construction/nand2tetirs/project10/MainTokenizer.xml")
#p=CompilationEngine("E:/Abo akademi/2024-2025/period 1/Software Construction/nand2tetirs/project10/Square.jack")
#p.create_parser_file("E:/Abo akademi/2024-2025/period 1/Software Construction/nand2tetirs/project10/MainParser.xml")
def directory_tokenizer(path):
    path=os.path.abspath(path)

    if(os.path.isfile(path)):

        j=JackTokenizer(path)
        j.create_token_file(path[0:-3]+"T.xml")
    else:
        for file in os.listdir(path):
            if file[-4:]=="jack":
                        #print(path)
                        j=JackTokenizer(path)
                        j.create_token_file(path[0:-3]+"T.xml")

def directory_parser(path):
    path=os.path.abspath(path)
    if(os.path.isfile(path)):
        j=CompilationEngine(path)
        j.create_parser_file(path[0:-3]+".xml")
    else:
        for file in os.listdir(path):
            if file[-4:]=="jack":
                        j=CompilationEngine(path)
                        j.create_parser_file(path[0:-3]+".xml")
directory_tokenizer(sys.argv[1])
directory_parser(sys.argv[1])

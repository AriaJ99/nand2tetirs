from JackTokenizer import *
import os
import sys
from SymbolTable import *
from VMWriter import *
labelCnt=0
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
class CompilationEngine:
    def __init__(self,tokenizer,outputFile):
        #object of the tokenizer
        self.tokenizer=tokenizer
        #print(type(self.tokenizer))
        #to store the parsed code
        self.parsedCode=""
        #status of the current token
        self.currentTokenChecked=False
        self.outputFile=outputFile
        #symbol tables
        self.firstSymbolTable=SymbolTable()
        self.secondSymbolTable=SymbolTable()
        #VMWriter
        self.VMWriter=VMWriter(open(outputFile,"w"))
        self.className=""
    def compileClass(self):
        #'class' className '{'classVarDec* subroutineDec*'}'
        self.parsedCode+="<class>\n"
        #class token
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        #class name
        #print(token)
        (token,tokenType)=self.tokenizer.advance()
        #storing the class name
        self.className=token
        #{ symbol
        (token,tokenType)=self.tokenizer.advance()
        #classVarDec
        (token,tokenType)=self.tokenizer.advance()
        self.currentTokenChecked=False
        #print(token)
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
        #store kind name
        kind=token
        #var type name
        (token,tokenType)=self.tokenizer.advance()
        #store type
        type=token
        #name token
        (token,tokenType)=self.tokenizer.advance()
        #add entry to symbol table
        self.firstSymbolTable.define(token, type, kind) 
        #; or more vars?
        (token,tokenType)=self.tokenizer.advance()
        while(token==','):
            #, symbol  
            #name token
            (token,tokenType)=self.tokenizer.advance()
            #add entry to symbol table
            self.firstSymbolTable.define(token, type, kind) 
            #next round
            (token,tokenType)=self.tokenizer.advance()
        #; symbol don't need advance it was done previously
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
        #reset the second table
        self.secondSymbolTable.reset()
        functionKind=token
        #if method then add object as first argument
        if functionKind=="method":
            self.secondSymbolTable.define("this",self.className,"argument") 
        #var type
        (token,tokenType)=self.tokenizer.advance()
        functionType=token
        #name token
        (token,tokenType)=self.tokenizer.advance()
        functionName=token
        #( symbol
        (token,tokenType)=self.tokenizer.advance()
        
        #parameter list check if there's any
        (token,tokenType)=self.tokenizer.advance()
        self.currentTokenChecked=False
        nArgs=self.compileParameterList()
        #) symbol 
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        #subroutine body
        self.tokenizer.advance()
        self.currentTokenChecked=False
        self.compileSubroutineBody(functionName,functionType,functionKind,nArgs)
        self.parsedCode+="</subroutineDec>\n"
        self.currentTokenChecked=True   
    def compileParameterList(self):
        #((type varName)(',' type varName)*)?
        self.parsedCode+="<parameterList>\n"
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        nArgs=0
        #check if there's any
        #
        #variable name
        #(token,tokenType)=self.tokenizer.advance()
        #
        #check if there's any variable
        #(token,tokenType)=self.tokenizer.advance()
        #check if the tokentype is keyword(in this case there's variable if it's symbol we should skip)
        if(tokenType=="keyword"):
            #first var
            #var type

            varType=token
            #name token
            (token,tokenType)=self.tokenizer.advance()
            nArgs+=1
            self.secondSymbolTable.define(token,varType,"argument")
            #, symbol for loop
            (token,tokenType)=self.tokenizer.advance()
            self.currentTokenChecked=False
            while(token==","):
                nArgs+=1
                #var type
                (token,tokenType)=self.tokenizer.advance()
                varType=token
                #name token
                (token,tokenType)=self.tokenizer.advance()
                self.secondSymbolTable.define(token,varType,"argument")
                nArgs+=1
                #next symbol(either , or ')')
                (token,tokenType)=self.tokenizer.advance()
                self.currentTokenChecked=False
        self.parsedCode+="</parameterList>\n"
        return nArgs
    def compileSubroutineBody(self,functionName,functionType,functionKind,nArgs):
        #'{' varDec* statements'}'
        self.parsedCode+="<subroutineBody>\n"
        #{ symbol
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        #for method
        #print(functionName,"***####$$@#@@",functionKind)
 
           
        #var dec check for var decleration
        (token,tokenType)=self.tokenizer.advance()
        self.currentTokenChecked=False
        nVars=0
        while(token=="var"):
            nVars+=self.compileVarDec()
            #look for , or statements
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
            
        #statements
        self.currentTokenChecked=False
        #VMWrite function className.name nVars
        self.VMWriter.writeFunction(self.className+"."+functionName,nVars)
        if functionKind=="method":
            #print("hereeee")
            self.VMWriter.writePush("argument",0)
            self.VMWriter.writePop("pointer",0)
        #add function entry to symbol table
        self.firstSymbolTable.define(functionName,functionType,functionKind,nArgs,nVars)
        #if constructor
        if functionKind=="constructor":
            self.VMWriter.writePush("constant",self.firstSymbolTable.varCount("field"))
            self.VMWriter.writeCall("Memory.alloc",1)
            self.VMWriter.writePop("pointer",0)
        self.compileStatments()
        #} symbol
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        
        self.currentTokenChecked=True
        #if(not self.currentTokenChecked):
            #if last token is raw it's } else we should advance
            #(token,tokenType)=self.tokenizer.advance()
        #
        self.parsedCode+="</subroutineBody>\n"
    def compileVarDec(self):
        # 'var'type varName (',' varName)*';'
        self.parsedCode+="<varDec>\n"
        #var token
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        
        #var type
        (token,tokenType)=self.tokenizer.advance()
        varType=token
        #name token
        (token,tokenType)=self.tokenizer.advance()
        varName=token
        self.secondSymbolTable.define(varName,varType,"var")
        #; or more vars?
        (token,tokenType)=self.tokenizer.advance()
        nVars=1
        while(token==','):
            #, symbol
            
            #name token
            (token,tokenType)=self.tokenizer.advance()
            self.secondSymbolTable.define(token,varType,"var")
            #next round
            (token,tokenType)=self.tokenizer.advance()
            nVars+=1
        #; symbol don't need advance it was done previously
        
        self.parsedCode+="</varDec>\n"
        self.currentTokenChecked=True   
        return nVars
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
        right_pointer=False
        #let token
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
         
        #name token
        (token,tokenType)=self.tokenizer.advance()
        varName=token
        #[ or = symbol
        (token,tokenType)=self.tokenizer.advance()
        #if right side pointer
        #if left side pointer
        left_pointer=False
        
        
        if(token=="["):
            #push the base of variable
            self.VMWriter.writePush(self.secondSymbolTable.kindOf(varName),self.secondSymbolTable.indexOf(varName))
            #expression
            
            (token,tokenType)=self.tokenizer.advance()
            self.currentTokenChecked=False
            self.compileExpression()
            #] symbol
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
            #add the index with the base
            self.VMWriter.writeArithmetic("add")
            #= symbol
            (token,tokenType)=self.tokenizer.advance()
            #expression
            (token,tokenType)=self.tokenizer.advance()
            self.currentTokenChecked=False
            self.compileExpression()
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
            #write the assignment
            self.VMWriter.writePop("temp",0)
            self.VMWriter.writePop("pointer",1)
            self.VMWriter.writePush("temp",0)
            self.VMWriter.writePop("that",0)
        else:
            (token,tokenType)=self.tokenizer.advance()
            self.currentTokenChecked=False
            self.compileExpression()
            if self.secondSymbolTable.kindOf(varName)!=None:
                self.VMWriter.writePop(self.secondSymbolTable.kindOf(varName),self.secondSymbolTable.indexOf(varName))
            else:
                self.VMWriter.writePop(self.firstSymbolTable.kindOf(varName),self.firstSymbolTable.indexOf(varName))
        #; symbol
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()   
        
        
        self.parsedCode+="</letStatement>\n"
        self.currentTokenChecked=True

    def compileIf(self):
        global labelCnt
        firstLabel=labelCnt
        secondLabel=labelCnt+1
        labelCnt+=2
        #'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}' )?
        self.parsedCode+="<ifStatement>\n"
        #if token
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        
        #( symbol
        (token,tokenType)=self.tokenizer.advance()
        
        #expression
        self.tokenizer.advance()
        self.currentTokenChecked=False
        self.compileExpression()
        #) symbol
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        #not
        self.VMWriter.writeArithmetic("not")
        #if-goto label1
        self.VMWriter.writeIf(f"L{firstLabel}")
        #{ symbol
        (token,tokenType)=self.tokenizer.advance()
        #statements
        self.tokenizer.advance()
        self.currentTokenChecked=False
        self.compileStatments()
        #} symbol
        #goto L2
        self.VMWriter.writeGoto(f"L{secondLabel}")
        #label L1
        self.VMWriter.writeLabel(f"L{firstLabel}")
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        
        #check if there's else
        (token,tokenType)=self.tokenizer.advance()
        self.currentTokenChecked=False
        if(token=="else"):
            #else token
            
            #{ symbol
            (token,tokenType)=self.tokenizer.advance()
            
            #statements
            self.tokenizer.advance()
            self.currentTokenChecked=False
            self.compileStatments()
            #} symbol
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
            
            self.currentTokenChecked=True
        #label L2
        self.VMWriter.writeLabel(f"L{secondLabel}")
        #Updating label
        
        self.parsedCode+="</ifStatement>\n"
        
    def compileWhile(self):
        global labelCnt
        firstLabel=labelCnt
        secondLabel=labelCnt+1
        labelCnt+=2
        #'while' '(' expression ')' '{' statements '}'
        self.parsedCode+="<whileStatement>\n"
        #while token
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        #label L1
        self.VMWriter.writeLabel(f"L{firstLabel}")
        #( symbol
        (token,tokenType)=self.tokenizer.advance()
        
        #expression
        self.tokenizer.advance()
        self.currentTokenChecked=False
        self.compileExpression()
        #) symbol
        #not
        self.VMWriter.writeArithmetic("not")
        self.VMWriter.writeIf(f"L{secondLabel}")
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        
        #{ symbol
        (token,tokenType)=self.tokenizer.advance()
        
        #statements
        self.tokenizer.advance()
        self.currentTokenChecked=False
        self.compileStatments()
        #} symbol
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        #goto L1
        self.VMWriter.writeGoto(f"L{firstLabel}")
        #label L2
        self.VMWriter.writeLabel(f"L{secondLabel}")
        
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
        
        self.currentTokenChecked=True
        #subroutineCall
        # subroutineName or (className|varName)
        (token,tokenType)=self.tokenizer.advance()

        prev_token=token
        prev_tokeType=tokenType
        #print(prev_token)
        #. or ( symbol
        (token,tokenType)=self.tokenizer.advance()
        nArgs=0
        if(token=="."):
            #(className | varName)'.'subroutineName'(' expressionList ')'
            #subroutineName
            (token,tokenType)=self.tokenizer.advance()
            subroutineName=token
            varType=self.firstSymbolTable.typeOf(prev_token)
            className=prev_token
            isVar=True
            varType=""
            varName=""
            varKind=""
            varIndex=0
            if self.secondSymbolTable.typeOf(prev_token)==None :
                if self.firstSymbolTable.typeOf(prev_token)==None:
                    isVar = False
                else:
                    varType=self.firstSymbolTable.typeOf(prev_token)
                    varKind=self.firstSymbolTable.kindOf(prev_token)
                    varIndex=self.firstSymbolTable.indexOf(prev_token)
                    varName=prev_token        
            else:
                varType=self.secondSymbolTable.typeOf(prev_token)
                varKind=self.secondSymbolTable.kindOf(prev_token)
                varIndex=self.secondSymbolTable.indexOf(prev_token)
                varName=prev_token
            if isVar:
                nArgs=1
                className=varType
                #method
                self.VMWriter.writePush(varKind,varIndex)
            #( symbol
            (token,tokenType)=self.tokenizer.advance()
            
            
            self.tokenizer.advance()
            self.currentTokenChecked=False
            nArgs+=self.compileExpressionList()
            #) symbol
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
            
            self.VMWriter.writeCall(className+"."+subroutineName,nArgs)
            
            self.currentTokenChecked=True
            
        elif(token=="("):
            
            self.tokenizer.advance()
            self.currentTokenChecked=False
            funcName=prev_token
            #push this
            if self.secondSymbolTable.kindOf("this")!=None:
                #method
                self.VMWriter.writePush("argument",0)
            else:
                #constructor
                self.VMWriter.writePush("pointer",0)
            name=self.className+"."+funcName
            nArgs=self.compileExpressionList()+1
            #) symbol
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
            self.currentTokenChecked=True
           
            self.VMWriter.writeCall(name,nArgs)

        #; symbol
        self.VMWriter.writePop("temp",0)
        (token,tokenType)=self.tokenizer.advance()
        
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
        
        (token,tokenType)=self.tokenizer.advance()
        self.currentTokenChecked=False
        #check if there's subroutincall or semicolomn
        if(token==";"):
            #void
            self.VMWriter.writePush("constant",0)
        else:
            self.compileExpression()
            #; symbol
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        #return  

        self.VMWriter.writeReturn()
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
        
        while(token in ["+","-","*","/","&","|","<",">","="]):
            #op symbol
            op=token
            #term
            self.tokenizer.advance()
            self.currentTokenChecked=False
            self.compileTerm()

            match op:
                case "+":
                    self.VMWriter.writeArithmetic("add")
                case "-":
                    self.VMWriter.writeArithmetic("sub")
                case "*":
                    self.VMWriter.writeCall("Math.multiply",2)
                    
                case "/":
                    self.VMWriter.writeCall("Math.divide",2)
                    
                case "&":
                    self.VMWriter.writeArithmetic("and")
                case "|":
                    self.VMWriter.writeArithmetic("or")
                case "<":
                    self.VMWriter.writeArithmetic("lt")
                case ">":
                    
                    self.VMWriter.writeArithmetic("gt")
                case "=":
                    self.VMWriter.writeArithmetic("eq")
            #next token
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        

        self.parsedCode+="</expression>\n"
        
    def compileTerm(self):
        # integerConstant|stringConstant|keywordConstant|varName|varName '[' expression ']'|subroutineCall|'('expression')'|unaryOp term
        self.parsedCode+="<term>\n"
        nArgs=0
        #statement let if while do return
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        if(tokenType=="integerConstant"):
            #integer
            self.VMWriter.writePush("constant",token)
            #token answered
            self.currentTokenChecked=True
        elif(tokenType=="stringConstant"):
            #string
            self.VMWriter.writePush("constant",len(token))
            self.VMWriter.writeCall("String.new",1)
            for ch in token:
                    self.VMWriter.writePush("constant", ord(ch));
                    self.VMWriter.writeCall('String.appendChar', 2)
            #token answered
            self.currentTokenChecked=True
        elif(token in ["true","false","null","this"]):

            #keyword constant
            match token:
                case "true":
                    self.VMWriter.writePush("constant", 1)
                    self.VMWriter.writeArithmetic("neg")
                case "false":
                    self.VMWriter.writePush("constant", 0)
                case "null":
                    self.VMWriter.writePush("constant", 0)
                case "this":
                    self.VMWriter.writePush("pointer", 0)
            #token answered
            self.currentTokenChecked=True
        elif(token in ["-" , "~"]):
            #unaryOp
            #term
            self.tokenizer.advance()
            self.currentTokenChecked=False
            self.compileTerm()
            if token=='-':
                self.VMWriter.writeArithmetic("neg")
            else:
                self.VMWriter.writeArithmetic("not")
        elif(token=="("):
            #( symbol
            
            #expression
            self.tokenizer.advance()
            self.currentTokenChecked=False
            self.compileExpression()
            #)symbol
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
            
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
               
                varName=prev_token
                if self.secondSymbolTable.kindOf(varName)!=None:
                    #it's argument or local
                    self.VMWriter.writePush(self.secondSymbolTable.kindOf(varName),self.secondSymbolTable.indexOf(varName))
                else :
                    # it's a field or static variable of a class
                    self.VMWriter.writePush(self.firstSymbolTable.kindOf(varName),self.firstSymbolTable.indexOf(varName))

                #[ symbol
                #expression
                self.tokenizer.advance()
                self.currentTokenChecked=False
                self.compileExpression()
                #add index to the base
                self.VMWriter.writeArithmetic("add")
                #push value to the stack
                self.VMWriter.writePop("pointer",1)
                self.VMWriter.writePush("that",0)
                #] symbol
                if(self.currentTokenChecked):
                    self.tokenizer.advance()
                    self.currentTokenChecked=False
                token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
                
                self.currentTokenChecked=True
            elif(token in ["(" , "."]):
                #subroutineCall
                if(token=="("):
                    #subroutineName
                    subroutineName=prev_token
                    #( symbol
                    #expressionList
                    self.tokenizer.advance()
                    self.currentTokenChecked=False
                    #push this
                    if self.secondSymbolTable.kindOf("this")!=None:
                        #method
                        self.VMWriter.writePush("argument",0)
                    else:
                        #constructor
                        self.VMWriter.writePush("pointer",0)
                    nArgs=self.compileExpressionList()+1
                    #) symbol
                    if(self.currentTokenChecked):
                        self.tokenizer.advance()
                        self.currentTokenChecked=False
                    token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
                    #call name nArgs
                    name=self.className+"."+subroutineName
                    
                    self.VMWriter.writeCall(name,nArgs)
                    
                    self.currentTokenChecked=True

                elif(token=="."):
                    #(className | varName)'.'subroutineName'(' expressionList ')'
                    #className|varName
                    #check wether it is a var or a class and if it's a var find the type(class)
                    isVar=True
                    varType=""
                    varName=""
                    varKind=""
                    varIndex=0
                    className=prev_token
                    if self.secondSymbolTable.typeOf(prev_token)==None :
                        if self.firstSymbolTable.typeOf(prev_token)==None:
                            isVar = False
                        else:
                            varType=self.firstSymbolTable.typeOf(prev_token)
                            varKind=self.firstSymbolTable.kindOf(prev_token)
                            varIndex=self.firstSymbolTable.indexOf(prev_token)
                            varName=prev_token
                    else:
                        varType=self.secondSymbolTable.typeOf(prev_token)
                        varKind=self.secondSymbolTable.kindOf(prev_token)
                        varIndex=self.secondSymbolTable.indexOf(prev_token)
                        varName=prev_token
                    
                    if isVar:
                        nArgs=1
                        className=varType
                        #method
                        self.VMWriter.writePush(varKind,varIndex)
                    #. symbol
                    
                    #subroutineName
                    (token,tokenType)=self.tokenizer.advance()
                    subroutineName=token
                    #( symbol
                    (token,tokenType)=self.tokenizer.advance()
                    
                    #expressionList
                    self.tokenizer.advance()
                    self.currentTokenChecked=False
                    nArgs+=self.compileExpressionList()
                    #) symbol
                    if(self.currentTokenChecked):
                        self.tokenizer.advance()
                        self.currentTokenChecked=False
                    token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
                    self.currentTokenChecked=True
                    name=className+"."+subroutineName
                   
                    self.VMWriter.writeCall(name,nArgs)
                    
                
            else:
                #varName
                #tag the previous token
                #the current token is still unanswered
                self.currentTokenChecked=False
                varName=prev_token
                if self.secondSymbolTable.kindOf(varName)!=None:
                    #it's argument or local
                    self.VMWriter.writePush(self.secondSymbolTable.kindOf(varName),self.secondSymbolTable.indexOf(varName))
                elif self.firstSymbolTable.kindOf(varName)=="field" :
                    # it's a field or static variable of a class
                    self.VMWriter.writePush("this",self.firstSymbolTable.indexOf(varName))
                else:
                    #it's a static variable
                    self.VMWriter.writePush("static",self.firstSymbolTable.indexOf(varName))
        self.parsedCode+="</term>\n"
    def compileExpressionList(self):
        # (expression(','expression)*)?
        self.parsedCode+="<expressionList>\n"
        nArgs=0
        if(self.currentTokenChecked):
            self.tokenizer.advance()
            self.currentTokenChecked=False
        token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()
        #print(token)
        #check if there's expression
        if(token!=')'):
            #expression
            self.compileExpression()
            nArgs=1
            #check for more
            if(self.currentTokenChecked):
                self.tokenizer.advance()
                self.currentTokenChecked=False
            token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()    
            
            while(token==','):
                
                #, symbol
                
                (token,tokenType)=self.tokenizer.advance()
                self.currentTokenChecked=False
                #expression
                self.compileExpression()
                nArgs+=1
                #next round
                if(self.currentTokenChecked):
                    self.tokenizer.advance()
                    self.currentTokenChecked=False
                token,tokenType=self.tokenizer.getToken(), self.tokenizer.getTokenType()

        return nArgs
        self.parsedCode+="</expressionList>\n"
    def compile(self):
        #create xml file for parser 
        #print("loop")
        
        
        self.tokenizer.advance()
        self.compileClass()
            #file.write(self.token)
        
        self.VMWriter.close()

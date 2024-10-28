class VMWriter:
    def __init__(self,file):
        #get an already opened file and store it
        self.file=file
    def writePush(self,segment,index):
        #push (segment) (index)
        self.file.write(f"push {transform(segment)} {index}\n")
    def writePop(self,segment,index):
        #pop (segment) (index)
        self.file.write(f"pop {transform(segment)} {index}\n")
    def writeArithmetic(self,command):
        #(command) (ADD SUB etc)
        self.file.write(command+"\n")
    def writeLabel(self,label):
        #label (label)
        self.file.write(f"label {label}\n")
    def writeGoto(self,label):
        #goto (label)
        self.file.write(f"goto {label}\n")
    def writeIf(self,label):
        #if-goto (label)
        self.file.write(f"if-goto {label}\n")
    def writeCall(self,name,nArgs):
        #call (name) (nArgs)
        self.file.write(f"call {name} {nArgs}\n")
    def writeFunction(self,name,nVars):
        #function (name) (nVars)
        self.file.write(f"function {name} {nVars}\n")
    def writeReturn(self):
        #return 
        self.file.write("return\n")
    def close(self):
        #close the file
        self.file.close()
def transform(s):
    if s=="var":
        return "local"
    elif s=="field":
        return "this"
    return s
    

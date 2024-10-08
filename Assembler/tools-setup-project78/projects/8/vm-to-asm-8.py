# This is a draft of a solution, implemented in the online session 
# on 10.9.2024
#
# This implementation is rather barebones, I suggest to implement a
# proper CodeWriter class
#

import sys
import os
#counters for jump labels
eq_cnt=0
gt_cnt=0
lt_cnt=0
ret_cnt=0
func_cnt=0
def op_push(args, ofd,file_name="foo"):
    memorysegment=args[0]
    value=args[1]

    match memorysegment:
        case "constant":
            ofd.write("@"+value+"\n")
            ofd.write("D=A\n")
            ofd.write("@SP\n")
            ofd.write("A=M\n")
            ofd.write("M=D\n")
            ofd.write("@SP\n")
            ofd.write("M=M+1\n")
        case "local":
            ofd.write("@"+value+"\n")
            ofd.write("D=A\n")
            ofd.write("@LCL\n")
            ofd.write("A=M+D\n")
            ofd.write("D=M\n")
            ofd.write("@SP\n")
            ofd.write("A=M\n")
            ofd.write("M=D\n")
            ofd.write("@SP\n")
            ofd.write("M=M+1\n")
        case "argument":
            ofd.write("@"+value+"\n")
            ofd.write("D=A\n")
            ofd.write("@ARG\n")
            ofd.write("A=M+D\n")
            ofd.write("D=M\n")
            ofd.write("@SP\n")
            ofd.write("A=M\n")
            ofd.write("M=D\n")
            ofd.write("@SP\n")
            ofd.write("M=M+1\n")
        case "this":
            ofd.write("@"+value+"\n")
            ofd.write("D=A\n")
            ofd.write("@THIS\n")
            ofd.write("A=M+D\n")
            ofd.write("D=M\n")
            ofd.write("@SP\n")
            ofd.write("A=M\n")
            ofd.write("M=D\n")
            ofd.write("@SP\n")
            ofd.write("M=M+1\n")
        case "that":
            ofd.write("@"+value+"\n")
            ofd.write("D=A\n")
            ofd.write("@THAT\n")
            ofd.write("A=M+D\n")
            ofd.write("D=M\n")
            ofd.write("@SP\n")
            ofd.write("A=M\n")
            ofd.write("M=D\n")
            ofd.write("@SP\n")
            ofd.write("M=M+1\n")
        case "static":
            ofd.write(f"@{file_name}.{value}\n")
            ofd.write("D=M\n")
            ofd.write("@SP\n")
            ofd.write("A=M\n")
            ofd.write("M=D\n")
            ofd.write("@SP\n")
            ofd.write("M=M+1\n")
        case "temp":
            ofd.write("@"+str(5+int(value))+"\n")
            #ofd.write("A=M\n")
            ofd.write("D=M\n")
            ofd.write("@SP\n")
            ofd.write("A=M\n")
            ofd.write("M=D\n")
            ofd.write("@SP\n")
            ofd.write("M=M+1\n")
        case "pointer":
            
                
            match value:
                case '0': 
                    ofd.write("@THIS\n")
                    ofd.write("D=M\n")
                    ofd.write("@SP\n")
                    ofd.write("A=M\n")
                    ofd.write("M=D\n")
                    ofd.write("@SP\n")
                    ofd.write("M=M+1\n")
                case '1':
                    ofd.write("@THAT\n")
                    ofd.write("D=M\n")
                    ofd.write("@SP\n")
                    ofd.write("A=M\n")
                    ofd.write("M=D\n")
                    ofd.write("@SP\n")
                    ofd.write("M=M+1\n")
                case _:
                    raise Exception("Wrong value for pointer")


        case _:
            raise Exception("Unknown memory segment"+memorysegment)

def op_pop(args, ofd,file_name="foo "):
    memorysegment=args[0]
    value=args[1]

    match memorysegment:
        case "local":
            #ofd.write(memorysegment)

            ofd.write("@LCL\n")
            ofd.write("D=M\n")
            ofd.write("@"+value+"\n")
            ofd.write("D=A+D\n")
            ofd.write("@R13\n")
            ofd.write("M=D\n")
            ofd.write("@SP\n")
            ofd.write("AM=M-1\n")
            ofd.write("D=M\n")
            ofd.write("@R13\n")
            ofd.write("A=M\n")
            ofd.write("M=D\n")
        case "argument":

            ofd.write("@ARG\n")
            ofd.write("D=M\n")
            ofd.write("@"+value+"\n")
            ofd.write("D=A+D\n")
            ofd.write("@R13\n")
            ofd.write("M=D\n")
            ofd.write("@SP\n")
            ofd.write("AM=M-1\n")
            ofd.write("D=M\n")
            ofd.write("@R13\n")
            ofd.write("A=M\n")
            ofd.write("M=D\n")
        case "this":

            ofd.write("@THIS\n")
            ofd.write("D=M\n")
            ofd.write("@"+value+"\n")
            ofd.write("D=A+D\n")
            ofd.write("@R13\n")
            ofd.write("M=D\n")
            ofd.write("@SP\n")
            ofd.write("AM=M-1\n")
            ofd.write("D=M\n")
            ofd.write("@R13\n")
            ofd.write("A=M\n")
            ofd.write("M=D\n")
        case "that":
            ofd.write("@THAT\n")
            ofd.write("D=M\n")
            ofd.write("@"+value+"\n")
            ofd.write("D=A+D\n")
            ofd.write("@R13\n")
            ofd.write("M=D\n")
            ofd.write("@SP\n")
            ofd.write("AM=M-1\n")
            ofd.write("D=M\n")
            ofd.write("@R13\n")
            ofd.write("A=M\n")
            ofd.write("M=D\n")
        case "static":
            ofd.write("@SP\n")
            ofd.write("AM=M-1\n")
            ofd.write("D=M\n")
            ofd.write(f"@{file_name}.{value}\n")
            ofd.write("M=D\n")
        case "temp":
            ofd.write("@SP\n")
            ofd.write("AM=M-1\n")
            ofd.write("D=M\n")
            ofd.write("@"+str(5+int(value))+"\n")
            #ofd.write("A=M\n")
            ofd.write("M=D\n")
        case "pointer":
            match value:
                case '0':
                    ofd.write("@SP\n")
                    ofd.write("AM=M-1\n")
                    ofd.write("D=M\n")
                    ofd.write("@THIS\n")
                    ofd.write("M=D\n")
                case '1':
                    ofd.write("@SP\n")
                    ofd.write("M=M-1\n")
                    ofd.write("A=M\n")
                    ofd.write("D=M\n")
                    ofd.write("@THAT\n")
                    ofd.write("M=D\n")
                case _:
                    raise Exception("Wrong value for pointer")
        case _:
            raise Exception("Unknown memory segment"+memorysegment)
def op_add(args, ofd):
    ofd.write("@SP\n")
    ofd.write("AM=M-1\n")
    ofd.write("D=M\n")
    ofd.write("A=A-1\n")
    ofd.write("M=M+D\n")
def op_sub(args, ofd):
    ofd.write("@SP\n")
    ofd.write("AM=M-1\n")
    ofd.write("D=M\n")
    ofd.write("A=A-1\n")
    ofd.write("M=M-D\n")
def op_eq(args, ofd):
    global eq_cnt
    ofd.write("@SP\n")
    ofd.write("AM=M-1\n")
    ofd.write("D=M\n")
    ofd.write("A=A-1\n")
    ofd.write("D=D-M\n")
    ofd.write("M=-1\n")#true
    ofd.write("@EQ_TRUE"+str(eq_cnt)+"\n")
    ofd.write("D;JEQ\n")
    ofd.write("@SP\n")
    ofd.write("A=M-1\n")
    ofd.write("M=0\n")#false
    ofd.write("(EQ_TRUE"+str(eq_cnt)+")\n") 
    eq_cnt+=1 



def op_gt(args,ofd):
    global gt_cnt
    ofd.write("@SP\n")
    ofd.write("AM=M-1\n")
    ofd.write("D=M\n")
    ofd.write("A=A-1\n")
    ofd.write("D=M-D\n")
    ofd.write("M=-1\n")#true
    ofd.write("@GT_TRUE"+str(gt_cnt)+"\n")
    ofd.write("D;JGT\n")
    ofd.write("@SP\n")
    ofd.write("A=M-1\n")
    ofd.write("M=0\n")#false
    ofd.write("(GT_TRUE"+str(gt_cnt)+")\n")
    gt_cnt+=1
def op_lt(args,ofd):
    global lt_cnt
    ofd.write("@SP\n")
    ofd.write("AM=M-1\n")
    ofd.write("D=M\n")
    ofd.write("A=A-1\n")
    ofd.write("D=M-D\n")
    ofd.write("M=-1\n")#true
    ofd.write("@LT_TRUE"+str(lt_cnt)+"\n")
    ofd.write("D;JLT\n")
    ofd.write("@SP\n")
    ofd.write("A=M-1\n")
    ofd.write("M=0\n")#false
    ofd.write("(LT_ TRUE"+str(lt_cnt)+")\n")
    lt_cnt+=1
def op_and(args,ofd):
    ofd.write("@SP\n")
    ofd.write("AM=M-1\n")
    ofd.write("D=M\n")
    ofd.write("A=A-1\n")
    ofd.write("M=D&M\n")
def op_or(args,ofd):
    ofd.write("@SP\n")
    ofd.write("AM=M-1\n")
    ofd.write("D=M\n")
    ofd.write("A=A-1\n")
    ofd.write("M=D|M\n")
def op_not(args,ofd):
    ofd.write("@SP\n")
    ofd.write("A=M-1\n")
    ofd.write("M=!M\n") 
def op_neg(args,ofd):
    ofd.write("@SP\n")
    ofd.write("A=M-1\n")
    ofd.write("M=-M\n")
###################################################
###################################################
#here starts the project 8
def op_label(args,ofd):
    ofd.write(f"({args[0]})\n")
def op_goto(args,ofd):
    ofd.write(f"@{args[0]}\n")
    ofd.write("0;JMP\n")
def op_if_goto(args,ofd):
    ofd.write("@SP\n")
    ofd.write("AM=M-1\n")
    ofd.write("D=M\n")
    ofd.write(f"@{args[0]}\n")
    ofd.write("D;JNE\n")
def op_call(args,ofd):
    global ret_cnt
    nArgs=int(args[1])
    retAddress=f"retAddress{ret_cnt}"
    ret_cnt+=1

    Arg_offset=5+nArgs
    #Pushing args into the stack 
    #for i in range(nArgs):
        #op_push(["argument",str(i)],ofd)
    #push return label
    
    ofd.write(f"@{retAddress}\n")
    ofd.write("D=A\n")
    ofd.write("@SP\n")
    ofd.write("A=M\n")
    ofd.write("M=D\n")
    ofd.write("@SP\n")
    ofd.write("M=M+1\n")

    #Save caller's segment pointers
    #Save LCL
    ofd.write("@LCL\n")
    ofd.write("D=M\n")
    ofd.write("@SP\n")
    ofd.write("A=M\n")
    ofd.write("M=D\n")
    ofd.write("@SP\n")
    ofd.write("M=M+1\n")
    #Save ARG
    ofd.write("@ARG\n")
    ofd.write("D=M\n")
    ofd.write("@SP\n")
    ofd.write("A=M\n")
    ofd.write("M=D\n")
    ofd.write("@SP\n")
    ofd.write("M=M+1\n")
    #Save THIS
    ofd.write("@THIS\n")
    ofd.write("D=M\n")
    ofd.write("@SP\n")
    ofd.write("A=M\n")
    ofd.write("M=D\n")
    ofd.write("@SP\n")
    ofd.write("M=M+1\n")
    #Save THAT
    ofd.write("@THAT\n")
    ofd.write("D=M\n")
    ofd.write("@SP\n")
    ofd.write("A=M\n")
    ofd.write("M=D\n")
    ofd.write("@SP\n")
    ofd.write("M=M+1\n")
    #Reposition ARG for callee

    ofd.write(f"@{Arg_offset}\n")
    ofd.write("D=A\n")
    ofd.write("@SP\n")
    ofd.write("D=M-D\n")
    ofd.write("@ARG\n")
    ofd.write("M=D\n")
    #Reposition LCL for callee
    ofd.write("@SP\n")
    ofd.write("D=M\n")
    ofd.write("@LCL\n")
    ofd.write("M=D\n")
    op_goto(args ,ofd)  
    ofd.write(f"({retAddress})\n")


    

def op_function(args,ofd):
    global func_cnt
    nVals=int(args[1])
    #Label
    ofd.write(f"({args[0]})\n")
    func_cnt+=1
    #creating local vars for callee
    for i in range(nVals):
        op_push(['constant','0'],ofd)
    #ofd.write(f"@{nVals}\n")
    #ofd.write("D=A\n")
    #ofd.write("@SP\n")
    #ofd.write("M=M+D\n")
def op_return(args,ofd):
    #save return address(in case that function had zero argument and return address was replaced with return value)
    ofd.write("@LCL\n")
    ofd.write("A=M\n")
    ofd.write("A=A-1\n")
    ofd.write("A=A-1\n")
    ofd.write("A=A-1\n")
    ofd.write("A=A-1\n")
    ofd.write("D=A-1\n")
    ofd.write("A=D\n")
    ofd.write("D=M\n")  
    ofd.write("@R14\n")
    ofd.write("M=D\n")
    #Replace return value with first arg
    ofd.write("@SP\n")
    ofd.write("A=M-1\n")
    ofd.write("D=M\n")
    ofd.write("@ARG\n")
    ofd.write("A=M\n")
    ofd.write("M=D\n")
    #Update Stack Pointer
    ofd.write("@ARG\n")
    ofd.write("D=M+1\n")
    ofd.write("@SP\n")
    ofd.write("M=D\n")
    #Restore THAT           
    ofd.write("@LCL\n")
    ofd.write("A=M\n")
    ofd.write("A=A-1\n")
    ofd.write("D=M\n")
    ofd.write("@THAT\n")
    ofd.write("M=D\n")
    #Restore THIS
    ofd.write("@LCL\n")
    ofd.write("A=M\n")
    ofd.write("A=A-1\n")
    ofd.write("A=A-1\n")
    ofd.write("D=M\n")
    ofd.write("@THIS\n")
    ofd.write("M=D\n")
    #Restore ARG
    ofd.write("@LCL\n")
    ofd.write("A=M\n")
    ofd.write("A=A-1\n")
    ofd.write("A=A-1\n")
    ofd.write("A=A-1\n")
    ofd.write("D=M\n")
    ofd.write("@ARG\n")
    ofd.write("M=D\n")
    #Restore LCL
    ofd.write("@LCL\n")
    ofd.write("A=M\n")
    ofd.write("A=A-1\n")
    ofd.write("A=A-1\n")
    ofd.write("A=A-1\n")
    ofd.write("A=A-1\n")
    ofd.write("D=M\n")
    ofd.write("@LCL\n")
    ofd.write("M=D\n")
    #in case that we had zero arguments
    #ofd.write("@R14\n")
    #ofd.write("D=M\n")
    #ofd.write("@R13\n")
    #ofd.write("A=M\n")
    #ofd.write("M=D\n")
    #Goto: here we have address of the label and should put it in A to access the memory
    ofd.write("@R14\n")
    ofd.write("A=M\n")
    ofd.write("0;JMP\n")

def boot_strap(ofd):
    ofd.write("//system boot strap\n")
    ofd.write("//allocate Stack Pointer\n")
    ofd.write("@256\n")
    ofd.write("D=A\n")
    ofd.write("@SP\n")
    ofd.write("M=D\n")
    ofd.write("//call Sys.init\n")
    op_call(["Sys.init","0"],ofd)
def translate_to_asm(ifn,ofd):
    ifd = open(ifn, "r")
    
    for line in ifd.readlines():  # iterate each line of the input file
        line=line.lstrip()
        if line[:2] == "//":      # skip comment lines
            continue
        words = line.split()      # split line into words

        if len(words) == 0:       # skip empty lines
            continue

        # process an actual vm instruction
        op = words[0]             # first word is operation
        args = words[1:]
        ofd.write("\n//"+line+"\n")
        match op:
            # push pop
            case 'push':
                op_push(args, ofd,ifn.split('/')[-1][:-3])
            case 'pop':
                op_pop(args, ofd,ifn.split('/')[-1][:-3])
            #logic and arithemic
            case 'add':
                op_add(args,ofd)
            case 'sub':
                op_sub(args,ofd)
            case 'neg':
                op_neg(args,ofd)
            case 'gt':   
                op_gt(args,ofd)
            case 'and':
                op_and(args,ofd)
            case 'or':
                op_or(args,ofd)
            case 'lt':                
                op_lt(args,ofd)
            case 'eq':
                op_eq(args,ofd)
            case 'not':
                op_not(args,ofd)
            #conditional and loop
            case 'label':
                op_label(args,ofd)
            case 'goto':
                op_goto(args,ofd)
            case 'if-goto':
                op_if_goto(args,ofd)
            case 'call':
                op_call(args,ofd)
            case 'function':
                op_function(args,ofd)
            case 'return':
                op_return(args,ofd)
            case _:
                raise Exception("Unexpected operation " + op)
    ifd.close()
def explore_dir(ifn,ofd):
    #print(os.listdir(ifn))
    #print(os.listdir(ifn)[0][-2:])
    vm_files = [f for f in os.listdir(ifn) if not os.path.isdir(f) and f[-2:]=="vm"]
    #print(vm_files)
    for vm in vm_files:
        #print (vm)
        translate_to_asm(ifn+"/"+vm,ofd)       
def main(ifn: str):
    



    
 
    
    if os.path.isdir(ifn):
        print("Directory")
        if ifn[-1]=="/":
            ifn=ifn[:-1]
        ofn = ifn+"/"+ifn.split("/")[-1] +".asm"
        ofd = open(ofn, "w")
        boot_strap(ofd)
        print("Translating", ifn, "into", ofn)
        explore_dir(ifn,ofd)

    else:
        #print(ifn)
        if ifn[-2:]=="vm":
            ofn = ifn[:-3] + ".asm"
            ofd = open(ofn, "w")
            # we don't need boot strap for single files
            #boot_strap(ofd)
            print("Translating", ifn, "into", ofn)
            translate_to_asm(ifn,ofd)
        else:
            raise Exception("Wrong file")
       

    
    
    ofd.close()

if __name__ == "__main__":
        print("Command line arguments:", sys.argv)
        main(sys.argv[1])

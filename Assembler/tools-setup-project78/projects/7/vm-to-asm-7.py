# This is a draft of a solution, implemented in the online session 
# on 10.9.2024
#
# This implementation is rather barebones, I suggest to implement a
# proper CodeWriter class
#

import sys
#counters for jump labels
eq_cnt=0
gt_cnt=0
lt_cnt=0
def op_push(args, ofd):
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
            ofd.write("@Foo."+value+"\n")
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

def op_pop(args, ofd):
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
            ofd.write("@Foo."+value+"\n")
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


def main(ifn: str):

    ofn = ifn[:-3] + ".asm"
    print("Translating", ifn, "into", ofn)

    ifd = open(ifn, "r")
    ofd = open(ofn, "w")

    for line in ifd.readlines():  # iterate each line of the input file
        if line[:2] == "//":      # skip comment lines
            continue
        words = line.split()      # split line into words

        if len(words) == 0:       # skip empty lines
            continue

        # process an actual vm instruction
        op = words[0]             # first word is operation
        args = words[1:]
        ofd.write("\n//"+line)
        match op:
            case 'push':
                op_push(args, ofd)
            case 'pop':
                op_pop(args, ofd)

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
            case _:
                raise Exception("Unexpected operation " + op)
        
    ifd.close()
    ofd.close()

if __name__ == "__main__":
        print("Command line arguments:", sys.argv)
        main(sys.argv[1])

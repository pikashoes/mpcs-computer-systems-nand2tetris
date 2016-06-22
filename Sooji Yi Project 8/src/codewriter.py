# -*- coding: utf-8 -*-
"""
Sooji Yi
"""
import os

class CodeWriter(object):
    
    #Opens the output file/stream and gets ready to write into it
    def __init__(self, input_file):
        self.VM = ""
        self.a = open(input_file, 'w')
        self.label = 0
        self.uniquelabel = []
        self.currentFunction = ""
    
    #Informs the code writer that the translation of a new VM file is started
    def setFileName(self, fileName):     
        self.VM, ext = os.path.splitext(fileName)
    
    def close(self):
        self.a.close()
        
    #Writes assembly code that effects the VM initlization (the bootstrap code). Placed at beginning of output file.
    def writeInit(self):
        self.a_command("256")
        self.c_command("D", "A", None)
        self.a_command("SP")
        self.c_command("M", "D", None)
        self.writeCall("Sys.init", 0)
    
    #Writes assembly code that effects the label command
    def writeLabel(self, label):
        if label not in self.uniquelabel:
            newLabel = self.currentFunction + "$" + label
            self.addUniqueLabel(newLabel)
            self.loop(newLabel)
        else:
            self.loop(label)

    #Writes assembly code that effects the goto command
    def writeGoTo(self, label):
        if label in self.uniquelabel:
            self.a_command(label)            #@Label
            self.c_command(None, "0", "JMP") #0;JMP
        else:
            newLabel = self.currentFunction + "$" + label
            self.addUniqueLabel(newLabel)
            self.a_command(newLabel)            
            self.c_command(None, "0", "JMP")
    
    #Writes assembly code that effects the if-goto command.
    def writeIf(self, label):
        if label in self.uniquelabel:
            self.arthimeticTemp()
            self.a_command(label)
            self.c_command(None, "D", "JNE")
        else:
            newLabel = self.addUniqueLabel(self.currentFunction + "$" + label)
            self.arthimeticTemp()
            self.a_command(newLabel)
            self.c_command(None, "D", "JNE")
        
    #Writes assembly code that effects the call command
    def writeCall(self, functionName, numArgs):
        self.currentFunction = functionName
        RETURN_ADDRESS = self.getUniqueLabel(self.currentFunction + "$" + "RETURN")
        self.a_command(RETURN_ADDRESS)
        self.equals("D", "A")
        self.a_command("SP") #Push D = index into SP
        self.equals("A", "M")
        self.equals("M", "D")
        self.a_command("SP")
        self.equals("M", "M+1")
               
        #Push LCL, ARG, THIS, THAT
        self.pushTemp_yesP("LCL", 0);
        self.pushTemp_yesP("ARG", 0);
        self.pushTemp_yesP("THIS", 0);
        self.pushTemp_yesP("THAT", 0);
        
        self.a_command("SP")
        self.equals("D", "M")
        self.a_command("5")
        self.equals("D", "D-A") #D = SP - 5
        self.a_command(numArgs)
        self.equals("D", "D-A") #D = SP - 5 - numArgs
        self.a_command("ARG")
        self.equals("M", "D")
        self.a_command("SP") #Now set LCL = SP to reposition LCL
        self.equals("D", "M")
        self.a_command("LCL")
        self.equals("M", "D")
        self.a_command(functionName) #goto functionName
        self.c_command(None, "0", "JMP")
        self.loop(RETURN_ADDRESS)
    
    #writes assembly code that effects the return command
    def writeReturn(self):
        self.a_command("LCL")
        self.equals("D", "M")
        self.a_command("R15") #FRAME (Temp variable)
        self.equals("M", "D")
        
        self.a_command("5") #FRAME - 5
        self.equals("A", "D-A")
        self.equals("D", "M")
        self.a_command("R14") #RET = *(FRAME - 5)
        self.equals("M", "D")
        
        self.a_command("SP") #*ARG = pop()
        self.equals("AM", "M-1")        
        self.a_command("SP")
        self.equals("A", "M")
        self.equals("D", "M")
        self.a_command("ARG")
        self.c_command("A", "M")
        self.equals("M", "D")
        
        self.a_command("ARG")
        self.equals("M", "M+1")
        self.equals("D", "M")
        self.a_command("SP")
        self.equals("M", "D")
        
        self.preTemplate("THAT")
        self.preTemplate("THIS")
        self.preTemplate("ARG")
        self.preTemplate("LCL") 
        
        self.a_command("R14")
        self.equals("A", "M")
        self.c_command(None, "0", "JMP")
           
    def preTemplate(self, pos):
        self.a_command("R15")
        self.equals("D", "M-1")
        self.equals("AM", "D")
        self.equals("D", "M")
        self.a_command(pos)
        self.equals("M", "D")
    
    #writes assembly code that effects the function command
    def writeFunction(self, functionName, numLocals):
        self.currentFunction = functionName
        self.addUniqueLabel(functionName)
        self.loop(self.currentFunction)
        for i in range(0, int(numLocals)):
            self.writePushPop(1, "constant", 0) #push constants 0 to stack
    
    #Writes the assembly code that is the translation of the given arithmetic command
    def writeArithmetic(self, command):
        #Arithmetic
        if command == "sub":
            self.arthimeticTemp()
            self.equals("M", "M-D")
        elif command == "add":
            self.arthimeticTemp()
            self.equals("M", "M + D")
        elif command == "or":
            self.arthimeticTemp()
            self.equals("M", "D|M")
        elif command == "and":
            self.arthimeticTemp()
            self.equals("M", "D&M")
        elif command == "not":
            self.a_command("SP")
            self.equals("A", "M-1")
            self.equals("M", "!M")
        elif command == "neg":
            self.equals("D", "0")
            self.a_command("SP")
            self.equals("A", "M-1")
            self.equals("M", "D-M")
        #Boolean
        elif command == "gt":
            self.arthimeticTemp()
            self.equals("D", "M-D")
            FALSE_gt = self.getUniqueLabel("FALSE_gt") #Ensures that the labels are consistent within code
            self.a_command(FALSE_gt)
            self.c_command(None, "D", "JLE")
            self.a_command("SP")
            self.equals("A", "M-1")
            self.equals("M", "-1")
            CONTINUE_gt = self.getUniqueLabel("CONTINUE_gt")
            self.a_command(CONTINUE_gt)
            self.c_command(None, "0", "JMP")
            self.loop(FALSE_gt)
            self.a_command("SP")
            self.equals("A", "M-1")
            self.equals("M", "0")
            self.loop(CONTINUE_gt)
        elif command == "eq":
            self.arthimeticTemp()
            self.equals("D", "M-D")
            FALSE_eq = self.getUniqueLabel("FALSE_eq")
            self.a_command(FALSE_eq)
            self.c_command(None, "D", "JNE")
            self.a_command("SP")
            self.equals("A", "M-1")
            self.equals("M", "-1")
            CONTINUE_eq = self.getUniqueLabel("CONTINUE_eq")
            self.a_command(CONTINUE_eq)
            self.c_command(None, "0", "JMP")
            self.loop(FALSE_eq)
            self.a_command("SP")
            self.equals("A", "M-1")
            self.equals("M", "0")
            self.loop(CONTINUE_eq)
        elif command == "lt":
            self.arthimeticTemp()
            self.equals("D", "M-D")
            FALSE_lt = self.getUniqueLabel("FALSE_lt")           
            self.a_command(FALSE_lt)
            self.c_command(None, "D", "JGE")
            self.a_command("SP")
            self.equals("A", "M-1")
            self.equals("M", "-1")
            CONTINUE_lt = self.getUniqueLabel("CONTINUE_lt")
            self.a_command(CONTINUE_lt)
            self.c_command(None, "0", "JMP")
            self.loop(FALSE_lt)
            self.a_command("SP")
            self.equals("A", "M-1")
            self.equals("M", "0")
            self.loop(CONTINUE_lt)

    #Push and Pop
    def writePushPop(self, command, segment, index):
        if command == 1: #C_PUSH
            if segment == "constant": #push constant <index>
                self.a_command(index)
                self.equals("D", "A")
                self.a_command("SP") #Push D = index into SP
                self.equals("A", "M")
                self.equals("M", "D")
                self.a_command("SP")
                self.equals("M", "M+1")
            elif segment == "local": #push local index means getting base address
                self.pushTemp_noP("LCL", index)
            elif segment == "argument":
                self.pushTemp_noP("ARG", index)
            elif segment == "this":
                self.pushTemp_noP("THIS", index)
            elif segment == "that":
                self.pushTemp_noP("THAT", index)
            elif segment == "pointer":
                if index == "0": #This
                    self.pushTemp_yesP("THIS", index)
                elif index == "1": #That
                    self.pushTemp_yesP("THAT", index)
            elif segment == "temp":
                self.pushTemp_noP("R5", int(index) + 5)
            elif segment == "static":
                self.a_command(self.VM + str(index))
                self.equals("D", "M")
                self.pushD_toSP()
                
        elif command == 2: #C_POP
            if segment == "local":
                self.popTemp_noP("LCL", index)
            elif segment == "argument":
                self.popTemp_noP("ARG", index)
            elif segment == "this":
                self.popTemp_noP("THIS", index)
            elif segment == "that":
                self.popTemp_noP("THAT", index)
            elif segment == "pointer":
                if index == "0":
                    self.popTemp_yesP("THIS", index)
                elif index == "1":
                    self.popTemp_yesP("THAT", index)  
            elif segment == "temp":
                self.popTemp_noP("R5", int(index) + 5)
            elif segment == "static":
                self.a_command(self.VM + str(index))
                self.equals("D", "A")
                self.a_command("R13")
                self.equals("M", "D")
                self.a_command("SP")
                self.equals("AM", "M-1")
                self.equals("D", "M")
                self.a_command("R13")
                self.equals("A", "M")
                self.equals("M", "D")  
            else:
                print("Something is wrong")

    """
    Templates that are repeated in the above methods, so put here to
    remove duplicate code.
    """
    #Template for Arithmetic
    def arthimeticTemp(self):
        self.a_command("SP")
        self.equals("AM", "M-1")
        self.equals("D", "M")
        self.equals("A", "A-1")
    
    #Template for Push w/ Pointer
    def pushTemp_yesP(self, segment, index):
        #Just read the data from THIS or THAT
#        print ("push with pointer is working")
        self.a_command(segment)            
        self.equals("D", "M") #Read the data from segment (THIS or THAT)
        self.pushD_toSP() #Push it to stack
    
    #Template for Push w/o Pointer
    def pushTemp_noP(self, segment, index):
#        print("push without pointer is working")
        self.a_command(segment) #Get the memory address of the segment  
        self.equals("D", "M")
        self.a_command(index)
        self.equals("A", "D+A")
        self.equals("D", "M")
        self.pushD_toSP()
    
    #Template for Pop w/ Pointer
    def popTemp_yesP(self, segment, index):
        #Store address of THIS or THAT in R13
#        print("pop with pointer is working")
        self.a_command(segment)
        self.equals("D", "A") #Get address of THIS or THAT
        self.a_command("R13")
        self.equals("M", "D")
        self.a_command("SP")
        self.equals("AM", "M-1")
        self.equals("D", "M") #D = what's in SP
        self.a_command("R13")
        self.equals("A", "M")
        self.equals("M", "D")

    #Template for normal Pop
    def popTemp_noP(self, segment, index):
#        print("pop without pointer is working")
        self.a_command(segment)
        self.equals("D", "M")
        self.a_command(index)
        self.equals("D", "D+A")
        self.a_command("R13")
        self.equals("M", "D")
        self.a_command("SP")
        self.equals("AM", "M-1")
        self.equals("D", "M") #D = what's in SP
        self.a_command("R13")
        self.equals("A", "M")
        self.equals("M", "D")

    #Template for pushing D to SP
    def pushD_toSP(self):      
        self.a_command("SP")
        self.equals("A", "M")
        self.equals("M", "D")
        self.a_command("SP")
        self.equals("M", "M+1")  

    """
    To be used for both the writeArithmetic and writePushPop methods
    to make things a little easier to read.
    """

    #<something>=<something>
    def equals(self, left, right):
        self.a.write(left + "=" + right + "\n")

    def loop(self, item):
        self.a.write("(" + item + ")" + "\n")

    #Writes an A command (@-something)
    def a_command(self, address):
#        print(address)
        address = str(address)
        self.a.write("@" + address + "\n")
    
    #Writes a C command
    def c_command(self, dest, comp, jump = None):
        if dest != None and jump == None:
            self.a.write(dest + "=" + comp) #<dest>=<comp>
        elif dest == None and jump != None:
            self.a.write(comp + ";" + jump) #<comp>;<jump>
        elif dest != None and jump != None:
            self.a.write(dest + "=" + comp + ";" + jump) #<dest>=<comp>;<jump>
        elif dest == None and jump == None:
            self.a.write(comp) #<comp>
        self.a.write("\n")
    
    #This function generates unique labels
    def getUniqueLabel(self, oldLabel):
        self.label += 1
        unique = oldLabel + str(self.label) #Now all of the loops will be unique
        self.uniquelabel.append(unique) #Append to the list of labels
        return unique
    
    #Appends label to the list of unique labels
    def addUniqueLabel(self, label):
        self.uniquelabel.append(label)
        return label

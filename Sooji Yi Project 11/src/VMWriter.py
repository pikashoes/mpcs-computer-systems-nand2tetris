# -*- coding: utf-8 -*-
"""
VMWriter: Emits VM commands into a file, using the VM command syntax
"""

class VMWriter(object):
    
    """
    Constructor. Creates a new file and prepares it for writing.
    """
    def __init__(self, outputFile):
        self.outputFile = open(outputFile, "w")
    
    """
    Writes a VM push command.
    CONST = constant
    ARG = argument
    LOCAL, STATIC, THIS, THAT, POINTER, TEMP (do not need to be changed)
    """
    def writePush(self, segment, index):
        index = str(index)
        if segment == "CONST":
            segment = "constant"
        elif segment == "ARG":
            segment = "argument"
        
        self.outputFile.write("push {} {}\n".format(segment.lower(), index))
    
    """
    Writes a VM pop command.
    """
    def writePop(self, segment, index):
        index = str(index)
        if segment == "CONST":
            segment = "constant"
        elif segment == "ARG":
            segment = "argument"
        
        self.outputFile.write("pop {} {}\n".format(segment.lower(), index))

    """
    Writes a VM arithmetic command.
    ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT (do not need to be changed except
    to be made lowercase)
    """
    def writeArithmetic(self, command):
        self.outputFile.write(command.lower() + "\n")
    
    """
    Writes a VM label command.
    """
    def writeLabel(self, label):
        self.outputFile.write("label {}\n".format(label))
    
    """
    Writes a VM goto command.
    """
    def writeGoto(self, label):
        self.outputFile.write("goto {}\n".format(label))
    
    """
    Writes a VM if-goto command.
    """
    def writeIf(self, label):
        self.outputFile.write("if-goto {}\n".format(label))
    
    """
    Writes a VM call command.
    """
    def writeCall(self, name, nArgs):
        self.outputFile.write("call {} {}\n".format(name, nArgs))
    
    """
    Writes a VM function command.
    """
    def writeFunction(self, name, nLocals):
        self.outputFile.write("function {} {}\n".format(name, nLocals))
    
    """
    Writes a VM return command.
    """
    def writeReturn(self):
        self.outputFile.write("return\n")
    
    """
    Writes anything
    """
    def writeToFile(self, data):
        self.outputFile.write(data + "\n")
    
    """
    Closes the output file.
    """
    def close(self):
        self.outputFile.close()
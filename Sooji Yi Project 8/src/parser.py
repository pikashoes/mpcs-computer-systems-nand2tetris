# -*- coding: utf-8 -*-
"""
Sooji Yi
"""
import re

class Parser(object):
    
    C_ARITHMETIC = 0 #
    C_PUSH = 1 #push segment index
    C_POP = 2 #pop segment index
    C_LABEL = 3 #label symbol
    C_GOTO = 4 #goto symbol
    C_IF = 5 #if-goto symbol
    C_FUNCTION = 6 #function functionName nLocals
    C_RETURN = 7 #return
    C_CALL = 8 #functionName nArgs
    
    #Constructor: Opens the input file/stream and gets ready to parse it
    def __init__(self, input_file):
        with open(input_file, "r+") as f:
            self.lines = f.readlines()
        self.command = ""
        self.current_line = 0
    
    #Are there more commands in the input?
    def hasMoreCommands(self):
        if self.current_line <= (len(self.lines) - 1):
            return True
        else:
            return False
    
    #Reads the next command from the input and makes it the current command
    def advance(self):
        self.command = self.lines[self.current_line]
        self.current_line += 1

    #Returns the type of the current VM command
    def commandType(self):     
        if re.match(r'(\s|^|$)push(\s|^|$)', self.command, flags=re.IGNORECASE): #searches exact word
            return Parser.C_PUSH
        elif re.match(r'(\s|^|$)pop(\s|^|$)', self.command, flags=re.IGNORECASE):
            return Parser.C_POP
        elif re.match(r'(\s|^|$)label(\s|^|$)', self.command, flags=re.IGNORECASE):
            return Parser.C_LABEL
        elif re.match(r'(\s|^|$)goto(\s|^|$)', self.command, flags=re.IGNORECASE):
            return Parser.C_GOTO
        elif re.match(r'(\s|^|$)if-goto(\s|^|$)', self.command, flags=re.IGNORECASE):
            return Parser.C_IF
        elif re.match(r'(\s|^|$)function(\s|^|$)', self.command, flags=re.IGNORECASE):
            return Parser.C_FUNCTION
        elif re.match(r'(\s|^|$)return(\s|^|$)', self.command, flags=re.IGNORECASE): 
            return Parser.C_RETURN
        elif re.match(r'(\s|^|$)call(\s|^|$)', self.command, flags=re.IGNORECASE):
            return Parser.C_CALL
        else:
            return Parser.C_ARITHMETIC
        
    #Returns the first argument of the current command
    def arg1(self):
        splitC = self.command.split()
        if self.commandType() == Parser.C_ARITHMETIC:
            return splitC[0]
        elif self.commandType() == Parser.C_RETURN:
            return "RETURN has no arguments."
        else:
            return splitC[1] #Return the first argument (2nd in the list)
    
    #Returns the second argument of the current command (if push, pop, function, or call)
    def arg2(self):
        splitC = self.command.split()
        return splitC[2] #Return second argument (3rd in the list)
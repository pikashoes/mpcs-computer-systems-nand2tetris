"""
Built following based on the outline on page 113, section 6.3.1 in 'The Elements
of Computer Systems' textbook. This class includes all the 'Routines' suggested
by the book.
"""

import re

class Parser(object):

    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2

#Opens the input file/stream and gets ready to parse it
    def __init__(self, input_file):
        with open(input_file, "r+") as f:
            self.lines = f.readlines()
        self.command = ""
        self.current_line = 0

#Check if there are more lines in the input
    def hasMoreCommands(self):
        if self.current_line <= (len(self.lines) - 1):
            return True
        else:
            return False

#Reads the next command from te input and makes it current command.
    def advance(self):
        self.command = self.lines[self.current_line]
        self.current_line += 1

#Returns the type of the current command
    def commandType(self):
        if re.match(r'^@.*', self.command): #Match for the @ sign at the beginning of the line in the current command from advance function
            return Parser.A_COMMAND #This indicates a-command
        elif re.match(r'^\(.*', self.command): #Match for the ( sign at the beginning of the line
            return Parser.L_COMMAND #Pseudocommand for symbol
        else:
            return Parser.C_COMMAND #Any other command will be a C-command

#Returns the symbol or decimal Xxx of the current command @Xxx or (Xxx)
    def symbol(self):
        matchingSymbol = re.match(r'^[@\(](.*?)\)?$', self.command)
        #Match for any character after the @ or the ( wich means A or L-command
        #Match 0 or 1 occurrences of this, grouped.
        #And look for ) at the end of line, optionally (will occur if beginning in "(")
        symbol = matchingSymbol.group(1) #Get the symbol or decimal
        return symbol

#Returns the dest mnemonic in the current C-command (8 possibilities)
    def dest(self):
        matchingDest = re.match(r'^(.*?)=.*$', self.command) #This looks for the Dest before the = sign in the beginning of the line
        if matchingDest: #If it returns something
            dest = matchingDest.group(1)
        else: #Else, return empty string
            dest = ""
        return dest

#Returns the comp mnemonic in the current C-command (28 possibilities)
    def comp(self):
        #There are different variations of possible places that comp might be in
        findEquals = self.command.find('=')
        findSemicolon = self.command.find(';')
        #Check which variation it is
        if findEquals != -1 and findSemicolon != -1: #dest=comp;jump
            compFinal = re.sub(r'^.*?=', '', self.command) #Remove Dest
            compFinal = re.sub(r';\w+$', '', compFinal) #Get Comp
            return compFinal.strip()
        elif findEquals != -1 and findSemicolon == -1: #dest=comp
            compFinal = re.sub(r'^.*?=', '', self.command) #Remove Dest
            compFinal = re.sub(r'=.*?', '', compFinal) #Get Comp
            return compFinal.strip()
        elif findEquals == -1 and findSemicolon != -1: #comp;jump
            compFinal = re.sub(r';\w+$', '', self.command) #Remove Jump
            compFinal = re.sub(r'^.*;', '', compFinal) #Get Comp
            return compFinal.strip()
        #If we can't find a comp....
#        if not compFinal:
#            print("ERROR: THERE IS NO COMP")


#Returns the jump mnemonic in the current C-command (8 possibilities)
    def jump(self):
        matchingJump = re.match(r"^.*;(\w+)$", self.command)
        if not matchingJump:
            jump = ""
        else:
            jump = matchingJump.group(1)
        return jump
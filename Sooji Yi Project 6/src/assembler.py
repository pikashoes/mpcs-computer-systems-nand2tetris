# -*- coding: utf-8 -*-
"""
Built following based on the outline on page 116, section 6.3.5 in 'The Elements
of Computer Systems' textbook.
"""

import sys
import parser
import code
import symboltable

class Assembler(object):

    #Initialization
    def __init__(self, inputFile):
        self.inputFile = inputFile
        self.outputFile = self.prepOutFile(inputFile)
        self.table = symboltable.SymbolTable()
        self.newSymbolAddress = 16 #New symbols have addresses starting at R16.

    #Goes through first and second pass
    def assemble(self):
        self.first_pass()
        self.second_pass()

    #Builds the symbol table without generating any code
    #Also keeps track of # of C- and A-instructions being loaded
    def first_pass(self):
        firstParser = parser.Parser(self.inputFile) #First parse
        #Then, make a running number recording the ROM address into which the current command will be eventually loaded
        currentAddress = 0         
        while firstParser.hasMoreCommands(): #Check if there are more lines in input
            firstParser.advance() #Keep moving through lines
            #If it's an A-command or a C-command, increment the current address
            if (firstParser.commandType() == firstParser.A_COMMAND) or (firstParser.commandType() == firstParser.C_COMMAND):
                currentAddress += 1
            #Else if it's a pseudocommand, then it doesn't change and we add a new entry to symbol table
            elif firstParser.commandType() == firstParser.L_COMMAND:
                self.table.addEntry(firstParser.symbol(), currentAddress)
            #Anything else, don't incremement, don't add (theoretically after stripWhiteSpace, nothing should be here)
            else:
                pass

    #Go through entire program and assemble
    def second_pass(self):
        secondParser = parser.Parser(self.inputFile)
        outfile = open(self.outputFile, 'w')
        codeAssemble = code.Code()
        
        #While there are lines
        while(secondParser.hasMoreCommands()):
            secondParser.advance() #Keep moving through lines
            #If it is a A-command
            if secondParser.commandType() == secondParser.A_COMMAND:
                #Get the a-instruction in binary, then add a new line
                outfile.write(codeAssemble.get_a_inst(self.getSymAddress(secondParser.symbol())) + '\n')
            #If it is a C-command
            elif secondParser.commandType() == secondParser.C_COMMAND:
                #Get the c-instruction
                outfile.write(codeAssemble.get_c_inst(secondParser.comp(), secondParser.dest(),
                    secondParser.jump()) + '\n')
            elif secondParser.commandType == secondParser.L_COMMAND:
                pass
        outfile.close()

    #Gets the symbol address
    def getSymAddress(self, symbol):
        #If it is a number, like @8, then return 8.
        if symbol.isdigit():
            return symbol
        #If it is a symbol like (LOOP) or @R8, then see if it's in the table
        else:
            #If it's not in the table
            if not self.table.contains(symbol):
                self.table.addEntry(symbol, self.newSymbolAddress) #add it using the provided method from symboltable
                self.newSymbolAddress += 1 #increment the address so we don't replace it next time
            #Once it's been added (or if it's already in the table), return the address of the symbol
            return self.table.GetAddress(symbol)

    #Change .asm to .hack
    @staticmethod
    def prepOutFile(toChangeFile):
        return toChangeFile.replace('.out', '.hack')


def main():
    mainInputFile = sys.argv[-1] #Get the file from the last argument
    toAsm = Assembler(mainInputFile)
    toAsm.assemble()

main()
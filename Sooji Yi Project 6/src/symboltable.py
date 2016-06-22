# -*- coding: utf-8 -*-
"""
Built following based on the outline on page 115, section 6.3.4 in 'The Elements
of Computer Systems' textbook. This class includes all the recommended 'Routines.
"""

class SymbolTable(object):

    #Symbol table that is given
    givenSymbols = {
            'SP': 0,
            'LCL':1,
            'ARG':2,
            'THIS':3,
            'THAT':4,
            'R0':0,
            'R1':1,
            'R2':2,
            'R3':3,
            'R4':4,
            'R5':5,
            'R6':6,
            'R7':7,
            'R8':8,
            'R9':9,
            'R10':10,
            'R11':11,
            'R12':12,
            'R13':13,
            'R14':14,
            'R15':15,
            'SCREEN':16384, 'KBD':24576}
    
    # Adds the pair (symbol, address) to the table
    def addEntry(self, symbol, address):
        self.givenSymbols[symbol] = address

    #Does the symbol table contain the given symbol?
    def contains(self, symbol):
        if symbol in self.givenSymbols: #Check if it is in the table
            return True
        else:
            return False

    #Returns the address associated with the symbol
    def GetAddress(self, symbol):
        return self.givenSymbols[symbol]

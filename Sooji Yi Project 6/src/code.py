# -*- coding: utf-8 -*-
"""
Built following based on the outline on page 115, section 6.3.2 in 'The Elements
of Computer Systems' textbook. This class includes all three tables (comp, dest,
and jump) but does not include the symbol table, following recommended guidelines.
"""

class Code(object):

# Table with Comp codes + binary equivalents
    comp_table = {
#a = 0 is put first.
    "0":"0101010",
    "1":"0111111",
    "-1":"0111010",
    "D":"0001100",
    "A":"0110000",
    "!D":"0001101",
    "!A":"0110001",
    "-D":"0001111",
    "-A":"0110011",
    "D+1":"0011111",
    "A+1":"0110111",
    "D-1":"0001110",
    "A-1":"0110010",
    "D+A":"0000010",
    "A+D":"0000010",
    "D-A":"0010011",
    "A-D":"0000111",
    "D&A":"0000000",
    "A&D":"0000000",
    "D|A":"0010101",
    "A|D":"0010101", #Interchangeable with D|A. Put here for corner cases
#a = 1 is next
    "M":"1110000",
    "!M":"1110001",
    "-M":"1110011",
    "M+1":"1110111",
    "M-1":"1110010",
    "D+M":"1000010",
    "M+D":"1000010",
    "D-M":"1010011",
    "M-D":"1000111",
    "D&M":"1000000",
    "M&D":"1000000",
    "D|M":"1010101", #Same as above
    "M|D":"1010101"
    }

#C-instruction Destination codes + binary equivalents
    dest_table =  {
    "" : "000",
    "M" : "001",
    "D" : "010",
    "MD" : "011",
    "A" : "100",
    "AM" : "101",
    "AD" : "110",
    "AMD" : "111"
    }

#C-instruction Jump codes + binary equivalents
    jump_table = {
    "" : "000",
    "JGT" : "001",
    "JEQ" : "010",
    "JGE" : "011",
    "JLT" : "100",
    "JNE" : "101",
    "JLE" : "110",
    "JMP" : "111"
    }

    """
    We need two functions to return either the a-instruction or c-instruction in
    binary. Depending on what command it is, we will call either one. That command
    can be determined after the file has been parsed and one of these functions will
    be called.
    """  
    #Return the a-instruction code in binary  
    def get_a_inst(self, address):
        return "0" + self.toBits(address).zfill(15)

    #Return the c-instruction code in binary
    def get_c_inst(self, compCode, destCode, jumpCode):
        return "111" + self.comp_table[compCode] + self.dest_table[destCode] + self.jump_table[jumpCode]
        #We get the comp in binary, the dest in binary, and the jump in binary all from their respective tables.

    #Converts an integer to binary
    @staticmethod #This is a static method.
    def toBits(anyNumber):
        return bin(int(anyNumber))[2:]
    #Gets rid of unnecessary first two parts of the bit.

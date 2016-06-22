# -*- coding: utf-8 -*-
"""
Symbol Table for Compiler.
Implemented using two separate hash tables: one for the class scope and another
one for the subroutine scope.
"""

class SymbolTable(object):
    
    """
    Constructor. Creates a new empty symbol table.
    """
    def __init__(self):
        self.classScope = {}            #Create a new class-scope symbol table
        self.subScope = {}              #Create a new subroutine-scope symbol table
        self.symbolCount = {}           #Create a new counter for symbols        
        self.symbolCount['STATIC'] = 0
        self.symbolCount['FIELD'] = 0
        self.symbolCount['ARG'] = 0
        self.symbolCount['VAR'] = 0

    """
    Starts a new subroutine scope (resets the subroutine's symbol table)
    """
    def startSubroutine(self):
        self.subScope = {}
        self.symbolCount['ARG'] = 0
        self.symbolCount['VAR'] = 0

    """
    Defines a new identifier of a given name, type, and kind and assigns it a
    running index.
    """
    def define(self, name, typeString, kind):
        #If ARG or VAR, add it to subroutines symbol table
        if kind == "ARG" or kind == "VAR":
            count = self.symbolCount[kind]
            self.symbolCount[kind] = count + 1
            self.subScope[name] = (typeString, kind, count)
#            print (self.subScope)
            
        #If STATIC or FIELD, add it to class scope symbol table
        elif kind == "STATIC" or kind == "FIELD":
            count = self.symbolCount[kind]
            self.symbolCount[kind] = count + 1
            self.classScope[name] = (typeString, kind, count)
    
    """
    Returns the number of variables of the given kind already defined in the 
    current scope.
    """
    def varCount(self, kind):
        
        return self.symbolCount[kind]
    
    """
    Returns the kind of the named identifier in the current scope. If the
    identifier is unknown in the current scope, returns NONE.
    """
    def kindOf(self, name):
        if name in self.subScope.keys():
            return self.subScope[name][1]
        elif name in self.classScope.keys():
            return self.classScope[name][1]
        else:
            return "NONE"
    
    """
    Returns the type of the named identifier in the current scope.
    """
    def typeOf(self, name):
        if name in self.subScope.keys():
            return self.subScope[name][0]
        elif name in self.classScope.keys():
            return self.classScope[name][0]
        else:
            return ""
    
    """
    Returns the index assigned to the named identifier.
    """
    def indexOf(self, name):
        if name in self.subScope.keys():
            return self.subScope[name][2]
        elif name in self.classScope.keys():
            return self.classScope[name][2]
        else:
            return -1
    

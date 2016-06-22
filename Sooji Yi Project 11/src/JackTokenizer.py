# -*- coding: utf-8 -*-
"""
Created on Sat May 14 15:07:26 2016
@author: pikashoes

Removes all comments and white space from the input stream
and breaks it into Jack-language tokens.

1. Constructor
2. hasMoreTokens (@return boolean)
3. advance (void)
4. tokenType (@return type of current token)
5. keyWord (@return keyword which is the current token if tokenType() = KEYWORD)
6. symbol (@return Char which is the current token when tokenType() = SYMBOL)
7. identifier (@return String when tokenType() = IDENTIFIER)
8. intVal (@return Int when tokenType() = INT_CONST
9. stringVal (@return String when tokenType() = STRING_CONST)

"""

import re

class JackTokenizer(object):
    
    KEYWORD = 1;
    SYMBOL = 2;
    IDENTIFIER = 3;
    INT_CONST = 4;
    STRING_CONST = 5;
    
    """Create lists to be searched """
    #=====================================
    keywordList = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean",
                     "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"}
    symbolList = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '<', '>', '=', '~'}

    operatorList = ["+", "-", "*", "/", "&", "|", "<", ">", "=", '"']
    
    symbolReg  = '[' + re.escape('|'.join(symbolList)) + ']'
    keywordReg = '(?!\w)|'.join(keywordList) + '(?!\w)'
    integerReg = r'\d+'
    stringReg = r'"[^"\n]*"'
    identifierReg = r'[\w]+'
    tokenWord = re.compile(symbolReg + "|" + keywordReg + "|" + integerReg + "|" + stringReg + "|" + identifierReg)

    #=====================================
    """
    Constructor
    """
    def __init__(self, input_file):
        self.words = []   #List of tokens      
        self.f = open(input_file, "r").read()
        
        self.words = self.tokenize()
        self.words = self.replaceSymb()
        print (self.words)
            
        self.token = ""
        self.currentToken = 0
        self.currentTokenType = -1

    """
    Retrieves the tokens
    """
    def tokenize(self):
        return [self.tokenMatch(word) for word in self.split(self.f)]
    
    def split(self, line):
        return self.tokenWord.findall(line)
    
    """
    Matches the tokens
    """
    def tokenMatch(self, word):
        if re.match(self.keywordReg, word) != None:
            return (JackTokenizer.KEYWORD, word)
        elif re.match(self.symbolReg, word) != None:
            return (JackTokenizer.SYMBOL, word)
        elif re.match(self.integerReg, word) != None:
            return (JackTokenizer.INT_CONST, word)
        elif re.match(self.stringReg, word) != None:
            return (JackTokenizer.STRING_CONST, word)
        elif re.match(self.identifierReg, word) != None:
            return (JackTokenizer.IDENTIFIER, word)

    def replaceSymb(self):
        return [self.replace(pair) for pair in self.words]

    def replace(self, pair):
        token, value = pair           
        return (token, value)

    """
    Checks to see if there are more tokens.
    """
    def hasMoreTokens(self):
        if self.currentToken + 1 < len(self.words):
            return True
        else:
            return False
    
    """
    Reads the next token and makes it the current token.
    """
    def advance(self):
        if (self.hasMoreTokens()):
            self.token = self.words[self.currentToken]
            self.currentToken += 1
        
    """
    Goes back to the previous token and sets that to the current token.
    """
    def revert(self):
        if self.currentToken > 0:        
            self.currentToken -= 1
    
    """
    Returns the type of the current token.
    """
    def tokenType(self):
        self.currentTokenType = self.token[0]
        return self.currentTokenType
            
    """
    Returns keyword when token type is KEYWORD.
    """
    def keyWord(self):
        if (self.currentTokenType == 1): #KEYWORD
            return self.token[1]
    
    """
    Returns symbol when token type is SYMBOL.
    """
    def symbol(self):
        if (self.currentTokenType == 2): #SYMBOL
            return self.token[1]
    
    """
    Returns identifier when token type is IDENTIFIER.
    """
    def identifier(self):
        if (self.currentTokenType == 3): #IDENTIFIER
            return self.token[1]
        else:
            print (self.token[0], self.token[1] + " is not an identifier!")
    
    """
    Returns integer value of token when token type is INT_CONST.
    """
    def intVal(self):
        if (self.currentTokenType == 4): #INT_CONST
            return int(self.token[1])
        else:
            print ("This token is not an integer constant!")
    
    """
    Returns string value of token when token type is STR_CONST.
    """   
    def stringVal(self):
        if (self.currentTokenType == 5): #STR_CONST
            stringVal = self.token[1]
            return stringVal[1:-1]
        else:
            print ("This token is not a string constant!")
    
    """
    Returns the current token. Generic method (above methods are more specific).
    """
    def getToken(self):
        return self.token[1]
        
    """
    Returns true if it's an operator.
    """
    def isOp(self):
        if (self.symbol() in self.operatorList):
            return True
        else:
            return False

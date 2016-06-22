# -*- coding: utf-8 -*-
"""
Created on Sat May 14 15:10:42 2016
@author: pikashoes

1. Constructor (@param Input file/stream, Output file/stream) that creates a new
compilation engine with given input and output. Call compileClass().
2. compileClass (compiles a complete class)
3. compileClassVarDec (compiles a static declaration or a field declaration)
4. compileSubroutine (compiles a complete method, function, or constructor)
5. compileParameterList (compiles a possibly empty parameter list, not including
the enclosing "()")
6. compileVarDec (compiles a var declaration)
7. compileStatements (compiles a sequence of statements, not including the
enclosing "{}")
8. compileDo (compiles a do statement)
9. compileLet (compiles a let statement)
10. compileWhile (compiles a while statement)
11. compileReturn (compiles a return statement)
12. compileIf (compiles an if statement, possibly with a trailing else clause)
13. compileExpression (compiles an expression)
14. compileTerm (compiles a term)
15. compileExpressionList (compiles a possibly empty comma-separated list of
expressions)
"""
from JackTokenizer import JackTokenizer

class CompilationEngine:
    
    """
    Constructor that creates a new compilation engine. Calls compileClass()
    """
    def __init__(self, tokenizerInput, outputFile):
        self.tokenizer = tokenizerInput
        self.outputFile = outputFile
        self.a = open(self.outputFile, 'w')
        
        self.compileClass()

    """
    Compiles a complete class.
    """
    def compileClass(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != JackTokenizer.KEYWORD) or (self.tokenizer.keyWord() != "class"):
            print ("ERROR: This is not a class.")
        
        self.writeOpen("class") #<class>
        self.writeLine("keyword", self.tokenizer.keyWord()) #<keyword>class</keyword>
        
        self.tokenizer.advance()
        
        if (self.tokenizer.tokenType() != JackTokenizer.IDENTIFIER):
            print ("ERROR: This is not an identifier.")
        
        self.writeLine("identifier", self.tokenizer.identifier())
        
        self.tokenizer.advance()
        self.writeSymbol("{") # <symbol>(</symbol>
        
        self.compileClassVarDec()           #*******************************
        self.compileSubroutine()            #*******************************
        
        self.tokenizer.advance()
        self.writeSymbol("}") # <symbol>}</symbol>
        
        if (self.tokenizer.hasMoreTokens()):
            print ("ERROR: Tokens remaining.")
        
        self.writeClose("class") #</class>
        self.a.close()
        
    """
    Compiles a static declaration or a field declaration.
    """
    def compileClassVarDec(self):
        self.tokenizer.advance()
        
        # Check if the next token is a symbol "}"
        if (self.tokenizer.tokenType() == JackTokenizer.SYMBOL) and (self.tokenizer.symbol() == "}"):
            self.tokenizer.revert()
            return
        
        if (self.tokenizer.tokenType() != JackTokenizer.KEYWORD):
            print ("ERROR: CompileClassVarDec keyword")
        
        # Check if the next token is a subroutine
        if (self.tokenizer.keyWord() == "constructor") or (self.tokenizer.keyWord() == "function") or (self.tokenizer.keyWord() == "method"):
            self.tokenizer.revert()
            return
            
        # If it's none of the above, the below code will execute.
        self.writeOpen("classVarDec") #<classVarDec>
        
        if (self.tokenizer.keyWord() != "static") and (self.tokenizer.keyWord() != "field"):
            print ("ERROR: Static or field.")
            
        self.writeLine("keyword", self.tokenizer.getToken())
        self.compileTokenType()

        boolState = True       
        
        while(boolState):
            self.tokenizer.advance()
            
            if (self.tokenizer.tokenType() != JackTokenizer.IDENTIFIER):
                print ("ERROR: compileClassVarDec needs identifier.")
            
            self.writeLine("identifier", self.tokenizer.identifier())
            
            self.tokenizer.advance()
            
            if (self.tokenizer.tokenType() != JackTokenizer.SYMBOL):
                print ("ERROR: compileClassVarDec needs symbol.")
                
            if (self.tokenizer.symbol() == ","):
                self.writeLine("symbol", ",")
            else:
                self.writeLine("symbol", ";")
                boolState = False
        
        self.writeClose("classVarDec")    
        self.compileClassVarDec()
            
    """
    Compiles a complete method, function, or constructor.
    """
    def compileSubroutine(self):
        self.tokenizer.advance()
        
        # Check if the next token is a symbol "}"
        if (self.tokenizer.tokenType() == JackTokenizer.SYMBOL) and (self.tokenizer.symbol() == "}"):
            self.tokenizer.revert()
            return
        
        # Starts the subroutine if return is not called above.
        if (self.tokenizer.tokenType() != JackTokenizer.KEYWORD):
                print ("ERROR: keyword in subroutine.")
                
        self.writeOpen("subroutineDec")
        self.writeLine("keyword", self.tokenizer.getToken())
        
        self.tokenizer.advance()
        if (self.tokenizer.keyWord() == "void") and (self.tokenizer.tokenType() == JackTokenizer.KEYWORD):
            self.writeLine("keyword", "void")
        else:
            self.tokenizer.revert()
            self.compileTokenType()
            
        self.tokenizer.advance()
        
        if (self.tokenizer.tokenType() != JackTokenizer.IDENTIFIER):
            print ("ERROR. Need identifier in compile Subroutine.")
            
        self.writeLine("identifier", self.tokenizer.identifier())
        
        self.tokenizer.advance()
        self.writeSymbol("(")
        
        self.writeOpen("parameterList")
        self.compileParameterList()     #*******************************
        self.writeClose("parameterList")
        
        self.tokenizer.advance()
        self.writeSymbol(")")
        
        #Subroutine Body
        self.writeOpen("subroutineBody")
        self.tokenizer.advance()
        self.writeSymbol("{")
        
        self.compileVarDec()            #*******************************
        
        self.writeOpen("statements")
        self.compileStatements()        #*******************************
        self.writeClose("statements")
        self.tokenizer.advance()
        self.writeSymbol("}")
        self.writeClose("subroutineBody")
        
        self.writeClose("subroutineDec")
        self.compileSubroutine()
      
    """
    Compiles a (possibly empty) parameter list.
    """
    def compileParameterList(self):
        self.tokenizer.advance()
        
        #Check if the next is }
        if (self.tokenizer.tokenType() == JackTokenizer.SYMBOL) and (self.tokenizer.symbol() == ")"):
            self.tokenizer.revert()
            return
        
        self.tokenizer.revert()
        
        #Breaks when symbol is not ","
        while(True):
            self.compileTokenType()
        
            self.tokenizer.advance()
            if (self.tokenizer.tokenType() != JackTokenizer.IDENTIFIER):
                print ("ERROR: compileParameterList needs identifier.")
            self.writeLine("identifier", self.tokenizer.identifier())
        
            self.tokenizer.advance()
            if (self.tokenizer.tokenType() != JackTokenizer.SYMBOL):
                print ("ERROR: compileParameterList needs symbol.")
            if (self.tokenizer.symbol() == ","):
                self.writeLine("symbol", ",")
            else:
                self.tokenizer.revert()
                break
    
    """
    Compiles a var declaration
    """
    def compileVarDec(self):
        self.tokenizer.advance()
        
        #Check if there is a var declaration
        if (self.tokenizer.tokenType() != JackTokenizer.KEYWORD) or (self.tokenizer.keyWord() != "var"):
            self.tokenizer.revert()
            return
        
        #If there is, then the following code is executed.
        self.writeOpen("varDec")
        self.writeLine("keyword", "var")
        self.compileTokenType()
        
        while(True):
            self.tokenizer.advance()
            
            if (self.tokenizer.tokenType() != JackTokenizer.IDENTIFIER):
                print ("ERROR. Identifier is 'None'")
            self.writeLine("identifier", self.tokenizer.identifier())
            
            self.tokenizer.advance()
            
            if (self.tokenizer.tokenType() != JackTokenizer.SYMBOL):
                print ("ERROR. Symbol error in VarDec")
            if (self.tokenizer.symbol() == ","):
                self.writeLine("symbol", ",")
            else:
                self.writeLine("symbol", ";")
                break
        
        self.writeClose("varDec")
        
        self.compileVarDec()
    
    """
    Compiles a sequence of statements.
    """
    def compileStatements(self):
        self.tokenizer.advance()
        
        #Check if the next is }
        if (self.tokenizer.tokenType() == JackTokenizer.SYMBOL) and (self.tokenizer.symbol() == "}"):
            self.tokenizer.revert()
            return
        
        #Otherwise, do below
        if (self.tokenizer.keyWord() == "do"):
            self.compileDo()            #*******************************
        elif (self.tokenizer.keyWord() == "let"):
            self.compileLet()           #*******************************
        elif (self.tokenizer.keyWord() == "while"):
            self.compileWhile()         #*******************************
        elif (self.tokenizer.keyWord() == "return"):
            self.compileReturn()        #*******************************
        elif (self.tokenizer.keyWord() == "if"):
            self.compileIf()
        
        self.compileStatements()
        
    """
    Compiles a do statement.
    """
    def compileDo(self):
        self.writeOpen("doStatement")
        self.writeLine("keyword", "do")
        self.compileSubCall()
        self.writeLine("symbol", ";")
        self.writeClose("doStatement")
    
    """
    Compiles a let statement.
    """
    def compileLet(self):
        self.writeOpen("letStatement")
        self.writeLine("keyword", "let")
        self.tokenizer.advance()
        
        if (self.tokenizer.tokenType() != JackTokenizer.IDENTIFIER):
            print ("CompileLet needs an identifier.")
        self.writeLine("identifier", self.tokenizer.identifier())
        self.tokenizer.advance()
        
        #Make sure it's either a [ or a =
        if (self.tokenizer.tokenType() != JackTokenizer.SYMBOL) or ((self.tokenizer.symbol() != "[")  and (self.tokenizer.symbol() != "=")):
            print ("ERROR: compile Let needs a [ or a =.")
        
        checkExp = False        
        
        #Check for expression
        if (self.tokenizer.symbol() == "["):
            checkExp = True
            self.writeLine("symbol", "[")
            self.compileExpression()            #**********************       
            self.tokenizer.advance()
            if (self.tokenizer.tokenType() == JackTokenizer.SYMBOL) and (self.tokenizer.symbol() == "]"):
                self.writeLine("symbol", "]")
            else:
                print ("ERROR: need ]")
        
        if (checkExp):
            self.tokenizer.advance()
        
        if (self.tokenizer.symbol() == "="):
            self.writeLine("symbol", "=")
            
        self.compileExpression()
        self.tokenizer.advance()
        self.writeSymbol(";")
        self.writeClose("letStatement")
        
    """
    Compiles a while statement.
    """
    def compileWhile(self):
        self.writeOpen("whileStatement")
        self.writeLine("keyword", "while")
        self.tokenizer.advance()
        self.writeSymbol("(")
        self.compileExpression()
        self.tokenizer.advance()
        self.writeSymbol(")")

        self.tokenizer.advance()
        self.writeSymbol("{")
        self.writeOpen("statements")
        self.compileStatements()
        self.writeClose("statements")
        self.tokenizer.advance()
        self.writeSymbol("}")

        self.writeClose("whileStatement")        
    
    """
    Compiles a return statement.
    """
    def compileReturn(self):
        self.writeOpen("returnStatement")
        self.writeLine("keyword", "return")
        self.tokenizer.advance()
        
        #Return something? Or just return?
        if (self.tokenizer.tokenType() == JackTokenizer.SYMBOL) and (self.tokenizer.symbol() == ";"):
            self.writeSymbol(";")
            self.writeClose("returnStatement")
            return
        
        self.tokenizer.revert()
        self.compileExpression()
        self.tokenizer.advance()
        self.writeSymbol(";")
        self.writeClose("returnStatement")
    
    """
    Compiles an if statement, possibly with a trailing else clause.
    """
    def compileIf(self):
        #If (some expression)
        self.writeOpen("ifStatement")
        self.writeLine("keyword", "if")
        self.tokenizer.advance()
        self.writeSymbol("(")
        self.compileExpression()
        self.tokenizer.advance()
        self.writeSymbol(")")
        
        #{some statements}
        self.tokenizer.advance()
        self.writeSymbol("{")
        self.writeOpen("statements")
        self.compileStatements()
        self.writeClose("statements")
        self.tokenizer.advance()
        self.writeSymbol("}")
        
        #Check if there is a trailing 'else' clause
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() == JackTokenizer.KEYWORD) and (self.tokenizer.keyWord() == "else"):
            #Else {some statements}
            self.writeLine("keyword", "else")
            self.tokenizer.advance()
            self.writeSymbol("{")
            self.writeOpen("statements")
            self.compileStatements()
            self.writeClose("statements")
            self.tokenizer.advance()
            self.writeSymbol("}")
        
        #No trailing 'else' clause
        else:
            self.tokenizer.revert()
        
        self.writeClose("ifStatement")
    
    """
    Compiles an expression
    """
    def compileExpression(self):
        self.writeOpen("expression")
        self.compileTerm()
        
        while(True):
            self.tokenizer.advance()              
            if (self.tokenizer.tokenType() == JackTokenizer.SYMBOL and self.tokenizer.isOp()):
                if (self.tokenizer.symbol() == ">"):
                    self.writeLine("symbol", "&gt;")
                elif (self.tokenizer.symbol() == "<"):
                    self.writeLine("symbol", "&lt;")
                elif (self.tokenizer.symbol() == "&"):
                    self.writeLine("symbol", "&amp;")
                elif (self.tokenizer.symbol() == '"'):
                    self.writeLine("symbol", "&quot;")
                else: #The other ones can just be taken directly     
                    self.writeSymbol(self.tokenizer.symbol())
                self.compileTerm()
            else:
                self.tokenizer.revert()
                break;
        
        self.writeClose("expression")
    
    """
    Compiles a term.
    """
    def compileTerm(self):
        self.writeOpen("term")
        self.tokenizer.advance()
        
        #Check if it's an identifier
        if (self.tokenizer.tokenType() == JackTokenizer.IDENTIFIER):
            temporaryToken = self.tokenizer.identifier()
            
            #Look one ahead
            self.tokenizer.advance()
            if (self.tokenizer.tokenType() == JackTokenizer.SYMBOL) and (self.tokenizer.symbol() == "["):
                self.writeLine("identifier", temporaryToken)
                self.writeSymbol("[")
                self.compileExpression() #Array
                self.tokenizer.advance()
                self.writeSymbol("]")
            
            elif (self.tokenizer.tokenType() == JackTokenizer.SYMBOL) and ((self.tokenizer.symbol() == "(") or (self.tokenizer.symbol() == ".")):
                #Subroutine Call
                self.tokenizer.revert()
                self.tokenizer.revert()
                self.compileSubCall()
            
            else:
                self.writeLine("identifier", temporaryToken)
                self.tokenizer.revert()
        else:
            if (self.tokenizer.tokenType() == JackTokenizer.INT_CONST):
                self.writeLine("integerConstant", self.tokenizer.intVal())
            elif (self.tokenizer.tokenType() == JackTokenizer.STRING_CONST):
                self.writeLine("stringConstant", self.tokenizer.stringVal())
            elif ((self.tokenizer.tokenType() == JackTokenizer.KEYWORD) and
                (self.tokenizer.keyWord() == "true" or
                self.tokenizer.keyWord() == "false" or
                self.tokenizer.keyWord() == "null" or
                self.tokenizer.keyWord() == "this")):
                self.writeLine("keyword", self.tokenizer.getToken())
            elif (self.tokenizer.tokenType() == JackTokenizer.SYMBOL and self.tokenizer.symbol() == "("):
                self.writeSymbol("(")
                self.compileExpression()
                self.tokenizer.advance()
                self.writeSymbol(")")
            elif (self.tokenizer.tokenType() == JackTokenizer.SYMBOL and (self.tokenizer.symbol() == "-" or self.tokenizer.symbol() == "~")):
                self.writeSymbol(self.tokenizer.symbol())
                self.compileTerm()
            else:
                print ("ERROR: CompileTerm missing")
        
        self.writeClose("term")
    
    """
    Compiles a (possibly empty) comma-searated list of expressions.
    """
    def compileExpressionList(self):
        self.tokenizer.advance()
        
        # Check if there is any expression at all
        if (self.tokenizer.tokenType() == JackTokenizer.SYMBOL) and (self.tokenizer.symbol() == ")"):
            self.tokenizer.revert()
        else:
            self.tokenizer.revert()
            self.compileExpression()
            
            while(True):
                self.tokenizer.advance()
                if ((self.tokenizer.tokenType() == JackTokenizer.SYMBOL) and (self.tokenizer.symbol() == ",")):
                    self.writeSymbol(",")
                    self.compileExpression()
                else:
                    self.tokenizer.revert()
                    break;        
    
    """
    Compiles a subroutine call.
    """
    def compileSubCall(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != JackTokenizer.IDENTIFIER):
            print("ERROR. Compile Subroutine call needs identifier.")
            
        self.writeLine("identifier", self.tokenizer.identifier())

        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != JackTokenizer.SYMBOL):
            print ("ERROR: Compile Subroutine call needs symbol.")
            
        if (self.tokenizer.symbol() == "("):
            self.writeSymbol("(")
            self.writeOpen("expressionList")
            self.compileExpressionList()
            self.writeClose("expressionList")
            
            self.tokenizer.advance()
            self.writeSymbol(")") #close
        
        elif (self.tokenizer.symbol() == "."):
            self.writeSymbol(".")
            
            self.tokenizer.advance()
            if (self.tokenizer.tokenType() != JackTokenizer.IDENTIFIER):
                print("ERROR. Compile sub-Subroutine call needs identifier.")
            
            self.writeLine("identifier", self.tokenizer.identifier())
            self.tokenizer.advance()
            self.writeSymbol("(")
            self.writeOpen("expressionList")
            self.compileExpressionList()
            self.writeClose("expressionList")
            self.tokenizer.advance()
            self.writeSymbol(")")
        else:
            print ("ERROR: sub call")
    
    """
    Writes output based on if it's keyword or identifier.
    """    
    def compileTokenType(self):
        self.tokenizer.advance()
        
        check = False
        if (self.tokenizer.tokenType() == JackTokenizer.KEYWORD) and ((self.tokenizer.keyWord() == "int") or (self.tokenizer.keyWord() == "boolean") or (self.tokenizer.keyWord() == "char")):
            self.writeLine("keyword", self.tokenizer.getToken())
            check = True
        elif (self.tokenizer.tokenType() == JackTokenizer.IDENTIFIER):
            self.writeLine("identifier", self.tokenizer.identifier())
            check = True
            
        if (check == False):
            print("TOKEN TYPE ERROR: needs token.")
    
    """
    Writes symbol.
    """
    def writeSymbol(self, symbol):
        if (self.tokenizer.tokenType() == JackTokenizer.SYMBOL) and (self.tokenizer.symbol() == symbol):
            self.writeLine("symbol", symbol)
        else:
            print ("ERROR:" + symbol)
    
    """
    Writes the opening <>.
    """
    def writeOpen(self, something):
        self.a.write("<{}>\n".format(something))
        
    """
    Writes the closing </>
    """
    def writeClose(self, something):
        self.a.write("</{}>\n".format(something))    
    
    """
    Writes the <> item </>
    """
    def writeLine(self, brackets, middle):
        self.a.write("<{}> {} </{}>\n".format(brackets, middle, brackets))

# -*- coding: utf-8 -*-
"""
Copied from previous assignment and enhanced.
"""
from JackTokenizer import JackTokenizer
from VMWriter import VMWriter
from SymbolTable import SymbolTable

class CompilationEngine:
    
    """
    Constructor that creates a new compilation engine. Calls compileClass()
    """
    def __init__(self, tokenizerInput, outputFile):
        self.tokenizer = tokenizerInput
        self.a = VMWriter(outputFile)
        self.symboltable = SymbolTable()
        self.currentClass = ""
        self.currentSub = ""
        
        self.whileLabelNumber = 0
        self.ifLabelNumber = 0
        
        self.compileClass()

    """
    Compiles a complete class.
    """
    def compileClass(self):   
        #Check to see that the token is the keyword "Class". If not, error.
        self.tokenizer.advance()        
        if (self.tokenizer.tokenType() != JackTokenizer.KEYWORD) or (self.tokenizer.keyWord() != "class"):
            print ("ERROR: This is not a class.")
        
        #The next token is the class name.
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != JackTokenizer.IDENTIFIER):
            print ("ERROR: This is not an identifier.")
        
        #Set the current class to the name of the class
        self.currentClass = self.tokenizer.identifier()
        
        #"Class className" is followed by "{". Check if this is the next token.
        self.tokenizer.advance()
        self.checkSymbol("{")
        
        self.compileClassVarDec()           
        self.compileSubroutine()           
        
        #The class is closed with the "}" symbol. Check it is present.
        self.tokenizer.advance()
        self.checkSymbol("}")
        
        #If there is more after the closing }
        if (self.tokenizer.hasMoreTokens()):
            print ("ERROR: Tokens remaining.")
        
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

        if (self.tokenizer.keyWord() != "static") and (self.tokenizer.keyWord() != "field"):
            print ("ERROR: Static or field.")
            
        kind = self.tokenizer.keyWord().upper()
        typeString = self.compileTokenType()    
        
        while(True):
            self.tokenizer.advance()
            
            if (self.tokenizer.tokenType() != JackTokenizer.IDENTIFIER):
                print ("ERROR: compileClassVarDec needs identifier.")
            
            name = self.tokenizer.identifier()
            self.symboltable.define(name, typeString, kind)
            
            self.tokenizer.advance() 
            if (self.tokenizer.tokenType() != JackTokenizer.SYMBOL):
                print ("ERROR: compileClassVarDec needs symbol.")
                print(self.tokenizer.tokenType())
                break
            if (self.tokenizer.symbol() == ";"):
                break
         
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
        
        keyword = self.tokenizer.keyWord()
        self.symboltable.startSubroutine() #new subroutine
        if (self.tokenizer.keyWord() == "method"):
            self.symboltable.define("this", self.currentClass, "ARG")         

        #Void
        self.tokenizer.advance()
        if (self.tokenizer.keyWord() == "void") and (self.tokenizer.tokenType() == JackTokenizer.KEYWORD):
            typeString = "void"
        else:
            self.tokenizer.revert()
            typeString = self.compileTokenType()
            
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != JackTokenizer.IDENTIFIER):
            print ("ERROR. Need identifier in compile Subroutine.")
        
        #Set the current subroutine
        self.currentSub = self.tokenizer.identifier()
        
        self.tokenizer.advance() #(
        self.compileParameterList()
        self.tokenizer.advance() #)
        
        #Subroutine Body
        self.tokenizer.advance() #{
        self.compileVarDec()
        #This will advance when it is called again and returns, so no need to advance here

        #Name the current function
        if (len(self.currentClass) != 0 and self.currentSub != 0):
            currentFunction = self.currentClass + "." + self.currentSub

        #VMWriter write function
        self.a.writeFunction(currentFunction, self.symboltable.varCount("VAR"))
        if (keyword == "method"):
            self.a.writePush("ARG", 0)            
            self.a.writePop("POINTER", 0)
        
        elif (keyword == "constructor"):
            self.a.writePush("CONST", self.symboltable.varCount("FIELD"))
            self.a.writeCall("Memory.alloc", 1)
            self.a.writePop("POINTER", 0)
        
        self.compileStatements()
        self.tokenizer.advance() #}
        
        self.compileSubroutine()
      
    """
    Compiles a (possibly empty) parameter list.
    """
    def compileParameterList(self):
        self.tokenizer.advance()
        
        #Check if the next is )
        if (self.tokenizer.tokenType() == JackTokenizer.SYMBOL) and (self.tokenizer.symbol() == ")"):
            self.tokenizer.revert()
            return
        
        #There are parameters
        self.tokenizer.revert()
        
        #Breaks when symbol is not ","
        while(True):
            typeString = self.compileTokenType()
        
            self.tokenizer.advance()
            if (self.tokenizer.tokenType() != JackTokenizer.IDENTIFIER):
                print ("ERROR: compileParameterList needs identifier.")
            
            self.symboltable.define(self.tokenizer.identifier(), typeString, "ARG")
        
            self.tokenizer.advance()
            if (self.tokenizer.tokenType() != JackTokenizer.SYMBOL):
                print ("ERROR: compileParameterList needs symbol.")
            elif (self.tokenizer.symbol() == ")"):
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
        typeString = self.compileTokenType()
        
        while(True):
            self.tokenizer.advance()
            
            #VarName
            if (self.tokenizer.tokenType() != JackTokenizer.IDENTIFIER):
                print ("ERROR. Identifier is 'None'")
            
            self.symboltable.define(self.tokenizer.identifier(), typeString, "VAR")
            
            #Symbol , or ;            
            self.tokenizer.advance()            
            if (self.tokenizer.tokenType() != JackTokenizer.SYMBOL):
                print ("ERROR. Symbol error in VarDec")
            
            if (self.tokenizer.symbol() == ";"):
                break

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
        self.compileSubCall()
        self.tokenizer.advance() #;
        self.a.writePop("TEMP", 0)
    
    """
    Compiles a let statement.
    """
    def compileLet(self):
        self.tokenizer.advance()
        
        if (self.tokenizer.tokenType() != JackTokenizer.IDENTIFIER):
            print ("CompileLet needs an identifier.")
        name = self.tokenizer.identifier()
        
        self.tokenizer.advance()
        
        #Make sure it's either a [ or a =
        if (self.tokenizer.tokenType() != JackTokenizer.SYMBOL) or ((self.tokenizer.symbol() != "[")  and (self.tokenizer.symbol() != "=")):
            print ("ERROR: compile Let needs a [ or a =.")
        
        checkExp = False        
        
        #Check for expression
        if (self.tokenizer.symbol() == "["):
            checkExp = True
            self.a.writePush(self.convertKind(self.symboltable.kindOf(name)), self.symboltable.indexOf(name))
            self.compileExpression()            
            self.tokenizer.advance()
            self.tokenizer.advance() #"]"
            self.a.writeArithmetic("ADD")
        
        if (checkExp):
            self.tokenizer.advance()
        
        self.compileExpression()
        self.tokenizer.advance() #;

        if (checkExp):
            self.a.writePop("TEMP", 0)
            self.a.writePop("POINTER", 1)
            self.a.writePush("TEMP", 0)
            self.a.writePop("THAT", 0)
        else:
            self.a.writePop(self.convertKind(self.symboltable.kindOf(name)), self.symboltable.indexOf(name))
     
    """
    Accounts for FIELD, STATIC, VAR, ARG
    """
    def convertKind(self, kind):
        if (kind == "FIELD"):
            return "THIS"
        elif (kind == "STATIC"):
            return "STATIC"
        elif (kind == "VAR"):
            return "LOCAL"
        elif (kind == "ARG"):
            return "ARG"
        else:
            return "NONE"
    
    """
    Compiles a while statement.
    """
    def compileWhile(self):
        whileNumber = self.whileLabelNumber        
        self.whileLabelNumber += 1 #Increment so it's unique
        
        self.a.writeLabel("WHILE{}\n".format(whileNumber))
        self.tokenizer.advance() #(
        self.compileExpression()
        self.tokenizer.advance() #)

        #If not-condition, then continue
        self.a.writeArithmetic("NOT")
        self.a.writeIf("END_WHILE{}\n".format(whileNumber))
        
        self.tokenizer.advance() #{
        self.compileStatements()
        self.tokenizer.advance() #}

        #If condition, then loop back to while
        self.a.writeGoto("WHILE{}\n".format(whileNumber))
        #Or continue
        self.a.writeLabel("END_WHILE{}\n".format(whileNumber))
    
    """
    Compiles a return statement.
    """
    def compileReturn(self):
        self.tokenizer.advance()
        
        #Peek ahead. Return expression or just return.
        if (self.tokenizer.tokenType() == JackTokenizer.SYMBOL) and (self.tokenizer.symbol() == ";"):
            self.a.writePush("CONST", 0)
        else:
            self.tokenizer.revert()
            self.compileExpression()
            self.tokenizer.advance() #;
        
        self.a.writeReturn()
    
    """
    Compiles an if statement, possibly with a trailing else clause.
    """
    def compileIf(self):
        ifNumber = self.ifLabelNumber
        self.ifLabelNumber += 1 #Increment each time so it's unique
        
        #If (some expression)
        self.tokenizer.advance() #(
        self.compileExpression()
        self.tokenizer.advance() #)
        
        self.a.writeArithmetic("NOT")
        self.a.writeIf("ELSE{}\n".format(ifNumber)) #if-goto jumps if it's not zero (0 = False)
        
        #{some statements}
        self.tokenizer.advance() #{
        self.compileStatements()
        self.tokenizer.advance() #}
        
        self.a.writeGoto("END{}\n".format(ifNumber))
        
        #Check if there is a trailing 'else' clause
        self.tokenizer.advance()
        self.a.writeLabel("ELSE{}\n".format(ifNumber))
        if (self.tokenizer.tokenType() == JackTokenizer.KEYWORD) and (self.tokenizer.keyWord() == "else"):
            #Else {some statements}
            self.tokenizer.advance() #{
            self.compileStatements()
            self.tokenizer.advance() #}
        
        #No trailing 'else' clause
        else:
            self.tokenizer.revert()
        
        self.a.writeLabel("END{}\n".format(ifNumber))
    
    """
    Compiles an expression
    """
    def compileExpression(self):
        self.compileTerm()
        
        while(True):
            self.tokenizer.advance()              
            if (self.tokenizer.tokenType() == JackTokenizer.SYMBOL and self.tokenizer.isOp()):
                command = ""                
                if (self.tokenizer.symbol() == ">"):
                    command = "gt"
                elif (self.tokenizer.symbol() == "<"):
                    command = "lt"
                elif (self.tokenizer.symbol() == "+"):
                    command = "add"
                elif (self.tokenizer.symbol() == "-"):
                    command = "sub"
                elif (self.tokenizer.symbol() == "*"):
                    command = "call Math.multiply 2"
                elif (self.tokenizer.symbol() == "/"):
                    command = "call Math.divide 2"
                elif (self.tokenizer.symbol() == "="):
                    command = "eq"
                elif (self.tokenizer.symbol() == "&"):
                    command = "and"
                elif (self.tokenizer.symbol() == "|"):
                    command = "or"
                else:
                    print ("NOT AN OP")
                self.compileTerm()  #Compile Term again so that the "add" or "sub" will come after both have been pushed              
                self.a.writeToFile(command)
            else:
                self.tokenizer.revert()
                break;
    
    
    """
    Compiles a term.
    """
    def compileTerm(self):
        self.tokenizer.advance()
        
        #Check if it's an identifier
        if (self.tokenizer.tokenType() == JackTokenizer.IDENTIFIER):
            temporaryToken = self.tokenizer.identifier()
            
            #Look one ahead
            self.tokenizer.advance()
            #Array
            if (self.tokenizer.tokenType() == JackTokenizer.SYMBOL) and (self.tokenizer.symbol() == "["):
                self.a.writePush(self.convertKind(self.symboltable.kindOf(temporaryToken)), self.symboltable.indexOf(temporaryToken))
                self.compileExpression()
                self.tokenizer.advance() #] to end array
                
                self.a.writeArithmetic("ADD")
                self.a.writePop("POINTER", 1)
                self.a.writePush("THAT", 0)
            
            elif (self.tokenizer.tokenType() == JackTokenizer.SYMBOL) and ((self.tokenizer.symbol() == "(") or (self.tokenizer.symbol() == ".")):
                #Subroutine Call
                self.tokenizer.revert()
                self.tokenizer.revert()
                self.compileSubCall()
            
            else:
                self.tokenizer.revert()
                self.a.writePush(self.convertKind(self.symboltable.kindOf(temporaryToken)), self.symboltable.indexOf(temporaryToken))
        else:
            if (self.tokenizer.tokenType() == JackTokenizer.INT_CONST):
                self.a.writePush("CONST", self.tokenizer.intVal())
            elif (self.tokenizer.tokenType() == JackTokenizer.STRING_CONST):
                string = self.tokenizer.stringVal()
                self.a.writePush("CONST",len(string))
                self.a.writeCall("String.new", 1)
                
                for i in range(0, len(string)):
                    self.a.writePush("CONST", string[i])
                    self.a.writeCall("String.appendChar", 2)
            elif ((self.tokenizer.tokenType() == JackTokenizer.KEYWORD) and (self.tokenizer.keyWord() == "true")):
                self.a.writePush("CONST", 0)
                self.a.writeArithmetic("NOT")           
            elif ((self.tokenizer.tokenType() == JackTokenizer.KEYWORD) and ((self.tokenizer.keyWord() == "false") or (self.tokenizer.keyWord() == "null"))):
                self.a.writePush("CONST", 0)          
            elif ((self.tokenizer.tokenType() == JackTokenizer.KEYWORD) and (self.tokenizer.keyWord() == "this")):
                self.a.writePush("POINTER", 0)
            elif (self.tokenizer.tokenType() == JackTokenizer.SYMBOL and self.tokenizer.symbol() == "("):
                self.compileExpression()
                self.tokenizer.advance() #)
            elif (self.tokenizer.tokenType() == JackTokenizer.SYMBOL and (self.tokenizer.symbol() == "-" or self.tokenizer.symbol() == "~")):
                symbol = self.tokenizer.symbol()
                self.compileTerm()
                if symbol == "-":
                    self.a.writeArithmetic("NEG")
                elif symbol == "~":
                    self.a.writeArithmetic("NOT")
            else:
                print ("ERROR: CompileTerm missing")

    
    """
    Compiles a (possibly empty) comma-searated list of expressions.
    """
    def compileExpressionList(self):
        self.tokenizer.advance()
        nArgs = 0
        
        # Check if there is any expression at all
        if (self.tokenizer.tokenType() == JackTokenizer.SYMBOL) and (self.tokenizer.symbol() == ")"):
            self.tokenizer.revert()
        else:
            nArgs = 1
            self.tokenizer.revert()
            self.compileExpression()
            
            while(True):
                self.tokenizer.advance()
                if ((self.tokenizer.tokenType() == JackTokenizer.SYMBOL) and (self.tokenizer.symbol() == ",")):
                    self.compileExpression()
                    nArgs += 1
                elif ((self.tokenizer.tokenType() == JackTokenizer.SYMBOL) and (self.tokenizer.symbol() == "(")): #Multiple parentheses expressions
                    #nArgs doesn't change
                    self.compileExpression()#BOOKMARK                
                else:
                    self.tokenizer.revert()
                    break;   
        return nArgs
    
    """
    Compiles a subroutine call.
    """
    def compileSubCall(self):
        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != JackTokenizer.IDENTIFIER):
            print("ERROR. Compile Subroutine call needs identifier.")
            
        identifier = self.tokenizer.identifier()
        nArgs = 0

        self.tokenizer.advance()
        if (self.tokenizer.tokenType() != JackTokenizer.SYMBOL):
            print ("ERROR: Compile Subroutine call needs symbol.")
            
        if (self.tokenizer.symbol() == "("):
            self.a.writePush("POINTER", 0)
            nArgs = self.compileExpressionList() + 1
            self.tokenizer.advance() #)
            self.a.writeCall(self.currentClass + "." + identifier, nArgs)
        
        #class/var.subroutine(expressionList)
        elif (self.tokenizer.symbol() == "."):
            
            self.tokenizer.advance()
            if (self.tokenizer.tokenType() != JackTokenizer.IDENTIFIER):
                print("ERROR. Compile sub-Subroutine call needs identifier.")
            
            identifier2 = self.tokenizer.identifier()
            typeString = self.symboltable.typeOf(identifier)
#            kind = self.symboltable.kindOf(identifier)

            if (typeString == "int") or (typeString == "boolean") or (typeString == "char") or (typeString == "void"):
                print ("ERROR")
            elif (typeString == ""): #if not in the symbol table
                name = identifier + "." + identifier2
            else:
                self.a.writePush(self.convertKind(self.symboltable.kindOf(identifier)), self.symboltable.indexOf(identifier))
                name = self.symboltable.typeOf(identifier) + "." + identifier2
            
            self.tokenizer.advance() #(
            nArgs += self.compileExpressionList()
            self.tokenizer.advance() #)
#            print (nArgs)
            self.a.writeCall(name, nArgs)
        else:
            print ("ERROR: sub call")
    
    """
    Writes output based on if it's keyword or identifier.
    """    
    def compileTokenType(self):
        self.tokenizer.advance()
        
        check = False
        if (self.tokenizer.tokenType() == JackTokenizer.KEYWORD) and ((self.tokenizer.keyWord() == "int") or (self.tokenizer.keyWord() == "boolean") or (self.tokenizer.keyWord() == "char")):
            return self.tokenizer.getToken()
            check = True
        elif (self.tokenizer.tokenType() == JackTokenizer.IDENTIFIER):
            return self.tokenizer.identifier()
            check = True
            
        if (check == False):
            print("TOKEN TYPE ERROR: needs token.")
    
    """
    Checks the symbol to ensure it is a symbol and that it is correct.
    """
    def checkSymbol(self, symbol):
        if (self.tokenizer.tokenType() != JackTokenizer.SYMBOL) and (self.tokenizer.symbol() != symbol):
            print ("ERROR:" + symbol)
    
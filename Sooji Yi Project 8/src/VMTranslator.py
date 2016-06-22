# -*- coding: utf-8 -*-
"""
Sooji Yi
"""
import parser, codewriter, sys, glob, os

class VMTranslator(object):
    
    #Open the files -- there could be multiple input files
    def codeWriterTranslate(self, input_files, output_file):
        codeWriter = codewriter.CodeWriter(output_file)
        for file in input_files:
            self.stripWhiteSpace(file)
            codeWriter.writeInit()
            self.parserTranslate(file, codeWriter)
        codeWriter.close()
    
    #Only one input file for the parser
    def parserTranslate(self, input_file, code_writer):
        parse = parser.Parser(input_file)
        code_writer.setFileName(os.path.basename(input_file)) #Account for directories
        while parse.hasMoreCommands():
            parse.advance()
            self.getASM(parse, code_writer)
    
    #Strip the white space, except spaces and new lines (taken from my stripWhiteSpace.py code)
    def stripWhiteSpace(self, input_file):
        with open(input_file, 'r+') as f:
            final_file = ""
            
            for line in f:
                if len(line.strip()) == 0:
                    continue
                else:
                    if line.partition('//')[1] == '//': #We check first if the '//' is present. If it is, then we ensure we keep the new line.
                        if line.partition('//')[0] != '': #If the '//' does not begin the line
                            line = line.partition('//')[0] + '\n' #Return the first element, which does not include \n, and then add \n
                            line = line.replace('\t','') #Remove tabs
                            final_file += line
                    else: #If the comment does begin the line
                        line = line.partition('//')[0] #Return the first element, which will include the newline character
                        line = line.replace('\t','') #Remove tabs
                        final_file += line

            outputFile = input_file #replacing the input_file with the new stripped output
            a = open(outputFile, 'w')
            a.write(final_file)            
            
    #Get the .asm file
    def getASM(self, parser, code_writer):
        CT = parser.commandType()
        if CT == parser.C_ARITHMETIC:
#            print(parser.arg1())
            code_writer.writeArithmetic(parser.arg1())
        elif CT == parser.C_PUSH or CT == parser.C_POP:
#            print (parser.arg1(), parser.arg2())
            code_writer.writePushPop(CT, parser.arg1(), parser.arg2())
        elif CT == parser.C_LABEL:
#            print(parser.arg1())
            code_writer.writeLabel(parser.arg1())
        elif CT == parser.C_GOTO:
#            print(parser.arg1())
            code_writer.writeGoTo(parser.arg1())
        elif CT == parser.C_IF:
#            print(parser.arg1())
            code_writer.writeIf(parser.arg1())
        elif CT == parser.C_RETURN:
#            print("return")
            code_writer.writeReturn()
        elif CT == parser.C_FUNCTION:
#            print(parser.arg1(), parser.arg2())
            code_writer.writeFunction(parser.arg1(), parser.arg2())
        elif CT == parser.C_CALL:
#            print(parser.arg1(), parser.arg2())
            code_writer.writeCall(parser.arg1(), parser.arg2())
    
#Main method
def main():
    inF, outF = getFiles(sys.argv[-1])
    translateFiles = VMTranslator()
    translateFiles.codeWriterTranslate(inF, outF)

def getFiles(files):
    if files.endswith(".vm"): #Then we know it's a single .vm file, not a directory
        return [files], files.replace(".vm", ".asm")
    else:
        return glob.glob(files + "/*.vm"), files + "/" + files + ".asm"

main()
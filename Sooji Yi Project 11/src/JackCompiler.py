# -*- coding: utf-8 -*-
"""
The compiler operates on a given source, where source is either a file name of the
form Xxx.jack or a directory name containing one or more such files. For each
Xxx.jack input file, the compiler creates a JackTokenizer and an output Xxx.vm file.
Next, the compiler uses the CompilationEngine, SymbolTable, and VMWriter modules
to write the output file.
"""
from CompilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer
import sys, glob, os

class JackCompiler(object):
    
    def getJack(self, inputFile):
        for file in inputFile:
            self.outputFileName = self.getFileName(file)
            self.stripWhiteSpace(file)
            self.compileJack(file, self.outputFileName) 
        
    def compileJack(self, inputFile, outputFile):
        jacktokenizer = JackTokenizer(inputFile)
        CompilationEngine(jacktokenizer, outputFile)
    
    def getFileName(self, file):
        self.filename, ext = os.path.splitext(file)
        self.outputFileName = self.filename + ".vm"
        return self.outputFileName
        
    #Strip the white space, except spaces and new lines (taken from my stripWhiteSpace.py code)
    def stripWhiteSpace(self, input_file):
        with open(input_file, 'r+') as f:
            tempFile = ""
            
            for line in f:
                if len(line.strip()) == 0:
                    continue
                else:
                    if line.partition('//')[1] == '//': #We check first if the '//' is present. If it is, then we ensure we keep the new line.
                        if line.partition('//')[0] != '' and line.partition('//')[0] != '\t' and len(line.partition('//')[0].strip()) != 0: #If the '//' does not begin the line
                            line = line.partition('//')[0] + '\n' #Return the first element, which does not include \n, and then add \n
                            line = line.replace('\t','') #Remove tabs
                            tempFile += line
                        else: #If the comment does begin the line
                            continue
                    
                    elif line.partition('/*')[1] == '/*':
                        line = line.lstrip() #Remove beginning spaces
                        if line.partition('/*')[0] != '': #It does not start the line
                            line = line.partition('/*')[0] + '\n'
                            tempFile += line
                        else: #If /* starts the line
                            continue
                    
                    elif line.partition('*')[1] == '*':
                        line = line.lstrip()
                        if line.partition('*')[0] != '': #So that the multiplication sign is preserved                          
                            tempFile += line
                        else:
                            continue
                    
                    elif line.partition('*/')[1] == '*/':
                        line = line.lstrip()
                        if line.partition('*/')[1] != '': #If there is stuff after
                            line = line.partition('*/')[1] #Grab what's after
                            tempFile += line
                        else:
                            continue
                    
                    else: # If // or /* or */ is not present
                        line = line.lstrip() #Remove leading spaces
                        tempFile += line
            
            outputFile = input_file #replacing the input_file with the new stripped output
            a = open(outputFile, 'w')
            a.write(tempFile) 


def main():
    inF  = getFiles(sys.argv[-1])
    analyzeFiles = JackCompiler()
    analyzeFiles.getJack(inF)

def getFiles(files):
    if files.endswith(".jack"): #Then we know it's a single file, not a directory
        return [files]
    else:
#        print (glob.glob(files + "/*.jack"))
        return glob.glob(files + "/*.jack")

main()
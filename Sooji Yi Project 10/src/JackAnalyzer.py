# -*- coding: utf-8 -*-
"""
Created on Sat May 14 14:56:32 2016
@author: pikashoes

The analyzer program operates on a given source, where the source is either
a file (Xxx.jack) or directory name containing one or more of these files.

1. Create a JackTokenizer from the input file/directory.
2. Create an output file called Xxx.xml and prepare it for writing.
3. Use the CompilationEngine to compile the input JackTokenizer into the output file.

"""

import sys, glob, os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

class JackAnalyzer(object):
    
    def getJack(self, inputFile):
        for file in inputFile:
            self.outputFileName = self.getFileName(file)
            self.stripWhiteSpace(file)
            self.compileJack(file, self.outputFileName) #Input is a JackTokenizer file and outputFile
        
    def compileJack(self, inputFile, outputFile):
        jacktokenizer = JackTokenizer(inputFile)
        CompilationEngine(jacktokenizer, outputFile)
    
    def getFileName(self, file):
        self.filename, ext = os.path.splitext(file)
        self.outputFileName = self.filename + ".xml"
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
                        if line.partition('*')[0] != '':
                            line = line.partition('*')[0] + '\n'
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
    analyzeFiles = JackAnalyzer()
    analyzeFiles.getJack(inF)

def getFiles(files):
    if files.endswith(".jack"): #Then we know it's a single file, not a directory
        return [files]
    else:
        return glob.glob(files + "/*.jack")

main()
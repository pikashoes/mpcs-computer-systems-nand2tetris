# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 17:46:35 2016

@author: pikashoes
"""

import sys, os
file = sys.argv[-1] #The last argument in the command line will be the file.

#Open the file
with open(file, 'r+') as f:
    final_file = ""
    path = os.path.dirname(file)

#Check to see if 'no-comments' has been added (after this program is opened).    
    if sys.argv[1] == "no-comments":
        for line in f:
            if len(line.strip()) == 0:
                continue
            else:
                if line.partition('//')[1] == '//': #We check first if the '//' is present. If it is, then we ensure we keep the new line.
                    if line.partition('//')[0] != '': #If the '//' does not begin the line
                        line = line.partition('//')[0] + '\n' #Return the first element, which does not include \n, and then add \n
                        line = line.replace(' ','') #Remove spaces
                        line = line.replace('\t','') #Remove tabs
                        final_file += line
                else: #If the comment does begin the line
                    line = line.partition('//')[0] #Return the first element, which will include the newline character
                    line = line.replace(' ','') #Remove spaces
                    line = line.replace('\t','') #Remove tabs
                    final_file += line


#If there is no 'no-comments', then we skip the removing comments above and go straight to removing the rest.
    else:   
        for line in f:
            if len(line.strip()) == 0:
                continue
            else:
                line = line.replace(' ','')
                line = line.replace('\t','')
                final_file += line

#Renaming the file to include 'out' and to put it in the same directory.    
    file = file.replace('.asm', '.out')
    outputFile = os.path.join(path, file)    

#Write to a new file.    
    a = open(outputFile, 'w')
    a.write(final_file)
    f.close()


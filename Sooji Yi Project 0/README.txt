What This Program Does
----------------------
* This program strips the white space from a given text file.
* White space includes spaces, tabs, and blank lines but NOT line returns.
* If no-comments is specified, then all comments beginning with the sequence "//" will be removed.

How to Compile/Run the Code
---------------------------
* Because this is through Python, as long as Python is installed in the computer, the code should be able to be interpreted by the command prompt/terminal.
* To execute this file, type into the Command Prompt or Terminal:
	python stripWhiteSpace.py filename.txt
	OR
	python stripWhiteSpace.py no-comments filename.txt
* Your working directory must be where the stripWhiteSpace.py is located.
* If your input file is in a different directory, instead of 'filename.txt', put the path.
	EX: python stripWhiteSpace.py no-comments /Users/pikashoes/Desktop/hello.txt
* The output file will be named filenameout.txt and will be contained in the same path as the input file ('filename' is replaceable with your file name).

What Works and Does Not Work
----------------------------
* If your input file is in a different directory from the stripWhiteSpace.py location, then you must specify that path in your command.
* The order must be preserved. The python file is first, then 'no-comments' if desired (this is optional), and the last should be your file name and/or path.
* os and sys are imported in this program. These should be available as standard Python libraries and are not specific to Max OSX.

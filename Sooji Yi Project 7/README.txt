Files
-----
* VMTranslator.py
* codewriter.py
* parser.py

How to compile/run the program
------------------------------
* The correct syntax is:
	python VMTranslator.py <filename or directory>
* The filename should end in .vm if it is the filename alone.
* You must change directories (cd) into the same directory where VMTranslator.py is located.
* If your file is located in a different directory, please put the directory even if it is for one file and not for a folder.

Important Notes BEFORE running program
--------------------------------------
* My previous project (Assembler) did not strip the white space immediately. However, I have included that within this VMTranslator. One thing to note is that when a .vm file is put through the VMTranslator using the syntax above in "How to compile/run the program", all white spaces AND comments will be stripped except for spaces and new lines (unless the line is empty).
* If you would like to keep your original, commented .vm file, PLEASE MAKE A COPY.

Comments
--------
* Because I was unable to make lecture, I had to rely heavily on the book and the uploaded worksheet. I think I will need to come in during office hours some time to go over the efficient way to generate Hack language from the commands (when I tried it without looking at the answers, I had errors). When I read the answers that you posted, I am able to understand it and can extend that for other commands, which is how I came up with the majority of the Hack instructions in this program. However, I would like to be able to do it just from my head, not from looking at the worksheet, so I will need more practice on this.
* My program passed all tests successfully.
* I had to do a lot of debugging, but I was able to figure them out after running the .asm file on the CPU emulator on "SLOW" and figuring out what I was missing.
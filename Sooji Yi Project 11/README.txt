Instructions
------------
* The correct syntax is:
	python JackCompiler.py [filename | directory]
* I checked this time by putting the folders in a different directory from the code and running this, and it successfully ran.
* It also worked for folders with only a single file.

What doesn't work
-----------------
* This program successfully compiles (and apparently translates, although not perfectly) all the programs supplied. The only error I see for some of the files is for my compileTerm function.
	* What I did:
	-------------
	> I began by opening up the .jack files and the outputted .vm files in my text editor and going through line by line in the .jack files using my code. If it declared a class variable, I'd go through my code and trace the steps. I was unable to figure out what was going wrong.
	> So I put print statements in appropriate places and tried to go through it again, except this time having a better idea of where the code might be failing. I still could not figure it out in time.
* This program compiles Pong, for instance, without any error message, but when the files are loaded into the Emulator, I get an error saying "PongGame.vm: Illegal 16-bit value". I'm not sure if it's related to the above error message, but this will thus not run on the VM emulator.
	* What I did:
	-------------
	> I followed steps similar to above, going through the files line by line. I did discover some other bugs along the way, but none of the fixes seemed to fix this particular error.
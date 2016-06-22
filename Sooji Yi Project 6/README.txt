PURPOSE OF THIS PROGRAM
-----------------------
* This is an assembler that translates Assembly language programs and generates Hack code that can be run on the CPU emulator.

COMPILING/RUNNING PROGRAM
-------------------------
* In order to successfully fun this program, the .asm file MUST be passed through the stripWhiteSpace.py file first, and all comments must be removed. The correct syntax for this is:
	python stripWhiteSpace.py no-comments filename.asm
* An output file is not generated as filename.out.
* Please check the README.txt for the Project 0 program for more detailed instructions.
* To actually run the assembler, the syntax is:
	python assembler.py filename.out
* This will generate a filename.hack file that can be run on the CPU emulator.

WHAT WORKS/DOES NOT WORK
------------------------
* Order must be preserved in the syntax.
* IMPORTANT: This assembler will not run if you do not run the stripWhiteSpace first!!
* I was unable to figure out how to integrate my stripWhiteSpace.py program into this assembler, because my stripWhiteSpace.py program is taking arguments from the command line. So it is not integrated. With more time, I think I would be able to, but since this assignment is late already and I have to begin the next one, for the sake of time, I have not integrated stripWhiteSpace.py. The assembler works as long as stripWhiteSpace is run first with no-comments.

NOTES
-----
* Sorry this is so late! I had a lot going on and, as I said on Piazza, wasn't able to finish this on time.
* I deleted my other test files but left the Pong.asm one.
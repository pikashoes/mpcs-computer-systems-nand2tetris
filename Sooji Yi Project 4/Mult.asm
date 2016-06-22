// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

	@R0
	D = M     // Take values from memory location 0 and put it in D
	@R13      // Put in temporary memory location
	M = D	 
	@R2	     
	M = 0     // Set R2 = 0
(LOOP)
    @R1       // Get second value
    D = M
    @END      // End if second value is equal to 0 so that if it starts out with 0, we can go straight to the product (0)
    D; JEQ
    @R13	  // Get first value from temporary location
    D = M
    @R2 
    M = M + D // Add first value to R2 
    @END      // End if the first value is equal to 0
    D;JEQ     // We add first and then end the first value because we want to minimize lines
    @R1       // Get the second value
    D = M    
    D = D - 1 // Decrease by 1
    M = D     // Put this decreased value in the temporary location
    @END      // End if the second value is now equal to 0
    D;JEQ
    @LOOP     // Else loop back
    0;JMP
(END)
	@END      // End
	0;JMP
	@pointer        // Screen starts at memory location pointer
	M = 0           // Set this to 0

(LOOP)
    @KBD            // Takes in keyboard input
    D = M

    @WHITE
    D;JEQ           // If no key is pressed, it will equal 0. Go to white
    @BLACK
    0;JMP           // Else go to black

(BLACK)
	@pointer        // Check if max has been reached
	D = M           // Get pointer
	                // 8192 is the max that the pointer can go to. 24575 is where KBD starts and 16384 is where SCREEN starts, so 24576 - 16384 = 8192.
	@8192           
	D = D - A

	                // If D (the value of the pointer) minus A (8192) is > 0, then it is above the max. We do not add more black because it is above the maximum. The white will decrease the memory location, allowing us to continue to add black when keyboard is pressed again.
	@LOOP
	D;JGE

    @pointer        // If max has not been reached, we blacken it
    D = M           // Get pointer
    @SCREEN         // Get the the screen
    A = A + D       // Screen address = Screen + Pointer
    M = -1          // Blacken the word at this memory location
    
    @pointer
    M = M + 1       // Increase pointer by 1
    
    @LOOP           // Go back to the beginning of the loop
    0;JMP

(WHITE)
    @pointer        // Unlike with black, since we are decreasing our pointer for when there is no KBD input, we check to see if it has reached its minimum of 16384.
    D = M
	@LOOP           // If it is less than 0, we don't decrease but instead go back to the loop   
	D;JLT

    @pointer
    D = M
    @SCREEN
    A = A + D
    M = 0           // Instead of making it black, we make it white

    @pointer
    M = M - 1       // When it is white, we decrease the position of the pointer so that it counteracts the black

    @LOOP           // Return to loop
    0;JMP
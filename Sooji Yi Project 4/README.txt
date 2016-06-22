Difficulties
------------
* Project 4:
* Mult.asm was easier to understand and execute for me than Fill.asm. I struggled with Fill.asm because I completely forgot from lecture and the book the actual memory locations/limitations of screen and keyboard.
* Once I figured that out, I originally tried to create a "Reset" function, where the pointer (which is why I initially named it pointer) could just go back to the beginning if it was filled with black.
* However, this wasn't really working for me, especially because if it wasn't filled with black and I didn't press down on the keyboard, I realized it would still go back to the beginning because it had reached the "end" of its space.
* So I re-read the book and looked at the example on Figure 4.2 and realized that if I could just increment and ALSO de-increment the pointer based on whether it was black or white, and if it reached the minimum or maximum, which we already know, to just do nothing but stay infinitely in the loop until a key was pressed or not, that would answer the question.

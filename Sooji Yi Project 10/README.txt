How To Compile and Run
-----------------------
* Correct syntax is:
	python JackAnalyzer.py [filename | directory]
* INPUT: Your original .jack files will be stripped of white space and will have all its block comments removed. If you want to preserve these comments, please make a copy of your original file.
* OUTPUT: For each file in the directory (or if it's a single file, for that file), this will output a filename.xml file that contains the syntax output of the supplied Jack file.

Comments
--------
* I unfortunately have been unable to make class due to personal reasons, and thus this assignment required careful reading of the book and lecture notes. I did try the worksheet myself, as well, which helped me understand the material better, although again, I'm not so sure how I'll fare without a worksheet, book, and lecture materials in front of me.
* Overall, I ended up spending a lot of time on this and had a lot of debugging to do. I re-used some of my VMTranslator code for the JackAnalyzer, although I added the block comment removal as well.
* The ouput files, when compared to the given files, compare successfully for Square, ExpressionlessSquare, and ArrayTest.
# Advanced Programming in C
  
This course is an introduction to systems programminng where we go beyond Java and IDEs to learn C and command line tools. We learn unix systems programming (I/O, process control, TCP/IP networking, sockets API and HTTP protocol), git, GNU Make, shell scripting and C. This course is designed to transform coders into professional programmers.

Per my Professor's Academic Integrity pledge I am not allowed to post solutions to any of my assignments here. However, I will detail the themes for each assignment and if you would like to see it send me an **email request** to mduran2429@gmail.com where I will provide you with a **url** to my **secret GitHub gist** for this course.

There were seven homework assignments:

	1. Intro to C (compiling, linking, headers, makefiles, data types, primitive operations)  
		* Prime Numbers, GCD, binary/hex/octal representation of numbers   
		
	2. Memory Management (malloc/free, pointers, arrays), command line arguments (argv/argc), errror checking (errno)
		* Seeding raw memory arrays with random numbers, sorting, then memory cleanup 
		* Taking the command line args in argv and returning them in all caps version order
		
	3. Creating Generic Library (generic linked list with associated methods), function pointers
		* wrote a generic singly linked list that could hold any data type
		* used function pointers to take command line args in argv and return them in reverse order
		
	4. Structs, C I/O
		* created our own data structure that would be binary written (read) to (from) a file
		
	5. Shell scripting, linux processes management (fork/exec and all the various process states), TCP/IP networking
		* used netcat to connect to our database remotely to perform various C I/O functions while using
		  the fork/exec paradigm
		  
	6. Sockets API (remote connection for our database), HTTP protocol (data transfer over network)
		* re-created homework 5 by using sockets API instead of netcat tool
		* created an HTTP client that would allow us to transfer data over the internet
		
	7. Three tier architecture 
		* created an HTTP server that would interface with our previously defined database to service
		  client database queries and render the results on an internet webpage

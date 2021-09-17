# C++ for C Programmers
  
This course is a survey and analysis of the C++ language from the C programmer's perspective. We focus on how C++ features are implemented and understand the subtleties to the language syntax compared to the "subset" C language. We cover essential 6 components of classes (constructor, destructor, copy assignment/constructor, and move assignment/constructor), references, operator overloading, namespaces, exceptions, OOP (polymorphism, multiple and virtual inheritence, C++ I/O stream hierarchy), generic programming (containers, iterators, STL algorithms, functors and lambda), RAII (smart pointers), templates (type deduction, variadic, metaprogramming, concepts).

Per my Professor's Academic Integrity pledge I am not allowed to post solutions to any of my assignments here. However, I will detail the themes for each assignment and if you would like to see it send me an **email request** to mduran2429@gmail.com where I will provide you with a **url** to my **secret GitHub gist** for this course.

There were four homework assignments:

	1. echocat.cpp, Makefile
		*  Introduction to c++, namespaces, string objects, and c review
		*  Makefile review
	
	2. mystring.cpp, Makefile, test1.cpp, ..., test5.cpp
		* Cpp classes (defined as an interface in .h file, implemented in .c file)
		* Learning when constructor, destructor, move (copy) assignment (construction) are called on the stack.

	3. mdb-grep.cpp, mdb.cpp, mdb.h
		* multiple inheritence, virtual functions, implicit declaration of class components
		* initializer lists, RAII, regex pattern matching
		* Converting all C style file I/O to C++ style file I/O

	4. xdb.h, exception.h, helper.h, maker.cpp, maker.h, mymake.cpp, MyMakefile
		* this is the best code in my portfolio
		* generic templates that can serialize any database struct to a file
		* User defined exceptions and exception inheritence
		* how to operate within a namespace, and advanced code organization
		* Recursive algorithm that parses a MyMakefile into rules while using shell script commands to build actual executables
		* try/catch blocks that utilize extensive error checking to ensure the software doesn't crash

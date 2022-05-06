# Cloud Computing and Big Data
  
This course focuses on the design and implementation of operating systems. Topics include process synchronization and interprocess communication, processor scheduling, memory management, virtual memory, interrupt handling, device management, I/O, and file systems. Hands-on study of Linux operating system design and kernel internals. Experience with commercial virtualization tools and open source software. The course was the first to introduce virtualization as a tool for teaching computer science, specifically operating systems.

per my professor's academic integrity pledge i am not allowed to post solutions to any of my assignments here. however, i will detail the themes for each assignment and if you would like to see it send me an **email request** to mduran2429@gmail.com where i will provide you with a **link** to my **secret github gist** for this course.

There were six homework assignments:

	1. simple bash-like shell program, assembly, bootsrap process (from BIOS loading the MBR to GRUB bootloader)
	2. building and running linux kernel, writing system calls in kernel space & testing the system call in user space 
	3. tracing process state changes (TASK_RUNNINNG, ... , EXIT_ZOMBIE, EXIT_DEAD), copying data from kernel to user space, testing the syscall
	4. kernel scheduler hacking (multicore round-robin scheduler), synchronization (low-level locking mechanisms), load balancing (leverage the multi core processor)
	5. Memory Management (paging virtual memory addresses to physical memory addresses), investigation of linux process address space
	6. implementation of psuedo file-systems (completely in RAM, not backed up to disk)
		* this assignment was not fully completed, but there is the inode_scrap.c code that
		  lays the groundwork for the ppagefs psuedo file system

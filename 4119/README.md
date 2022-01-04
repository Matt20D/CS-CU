# Computer Networks
  
This course provides an introduction to computer networks and the technical foundations of the Internet, including applications, protocols, algorithms for routing and transport/congestion control, and local area networks. The course will cover key network “layers” and how they operate together to provide services, with an emphasis on:

 * Application, transport, network, and link layers.
 * A “top-down” approach, starting from applications we all use every day in order to derive the requirements they place on the network, moving to how the layers below the applications provide these requirements.
 * How these layers manifest in the Internet, and how the Internet’s design has facilitated its tremendous growth.
 * The emerging software-defined networking (SDN) separation of the network control plane from the network data plane.

Per my Professor's Academic Integrity pledge I am not allowed to post solutions to any of my assignments here. However, I will detail the themes for each assignment and if you would like to see it send me an **email request** to mduran2429@gmail.com where I will provide you with a **link** to my **secret GitHub gist** for this course.

There were five homework assignments:

	1. Introduction to Networks (Written): protocols, various delays, routing, throughput, file transfers, packets, packet loss.
	   
	2. Columbia re-open CU Sockets Application Layer (Programming): For this project I wrote an application layer program that modeled Columbia University's re-open CU mobile app to ensure that people that are admitted to campus show no sypmtoms of covid-19. I wrote this application layer program over TCP and UDP protocols.
	   
	3. Transport Layer (Written): reliable transfer protocol, acks/naks, window sliding, RDT Finite State Machines.
	   
	4. Transport Layer TCP reliable file transfer over UDP socket API (Programming): For this project I wrote a file transfer application layer program, that built TCP reliability over UDP socket api. I created my own Packet classs which serialized and de-serialized data to be sent over the internet via a proxy program. This emulator simulated packet loss, delay, corruption and more phenomenon which arise in the transport layer internet protocols. This project was a good example of how we can implement reliability at higher internet stack levels over unreliable data transfer mediums.
	   
	5. Network Layer (Written): IP adrresses/masking, router switching, dijkstra routing proof, BGP.



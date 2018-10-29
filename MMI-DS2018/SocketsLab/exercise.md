# Chat server part 1

## Establishing a connection:
### Exercise 1:
Make a simple server that accepts a TCP connection on port 8080 from a client and replays it back.

You can test the server by doing `telnet 127.0.0.1 8080`

How can we allow more than 1 connection at a time?

### Exercise 2:
Let's create our own client, make a program that reads user inputs, and send it to the server,
the client also displays information from the client.

## Threads
Threads are spawned from a process and allows us to do simultaneous computation.
We can share resources, like memory.

### Exercise 3:
Make a program that spawns threads, give each thread an identifier and make every thread greet
the program by saying `"Hi, I'm thread <id>"`, `<id>` being the identifer for the thread.

### Exercise 4:
Modify the simple server created in Exercise 1 so that it spawns one thread to handle each incoming client,
is it the best thing we can do? How can this be more efficient? reflect on possible optimizations.

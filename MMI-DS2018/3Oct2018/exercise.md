# Chat server part 2

## Server operator:
### Exercise 1:
Spawn a thread for the server so a server operator can do the following things:
  - Numbers of users connected, executing the command `/n_users`


## Protocol
We have to define the protocol we want to communicate from, we define a Message class
so clients communicate with the server, and later with each other.

### Exercise 2:
Create a class Message with a methods `encode()`, that returns `bytes` so it can be sent
to the server, our Message class should have a header and a body,
for now let's just make the message with a body.

We are going to use google protobuf to design our protocol, go ahead and do a protocol for a Message
with the fields:
  - int32 fr, specifying who's sending the message
  - int32 to, specifying to whom the message is addressed
  - string msg, specifying the message content
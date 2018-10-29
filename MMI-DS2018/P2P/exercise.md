# Chat server part 3

## Communicating clients
Implement direct messages from client-to-client.

## What if the client is not present?
Design a system in which unsent messages are stored until the receiver is notified, change the protocol accordingly

## Merging server and client
In a p2p system, clients and servers as seen as a single entity, model your program such that messages can be broadcasted among different peers until they reach the destination
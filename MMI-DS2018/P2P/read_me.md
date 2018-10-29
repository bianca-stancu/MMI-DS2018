# P2P Assignment

## Usage
System arguments, in order:
* Ip
* Port
* Displayed name

## Commands
* **help** to display all commands
* **exit** to quit program
* **show** to show a list of all peers
* **add <ip> <port>** to add a peer to your list of peers
* **send <name>** to send a message to a peer
* **close <ip> <port>** to remove a peer and close the connection

## Methodology
* For sending messages, flooding technique is used
* Every message has a uuid and every node keeps track of the nodes they saw
* For every message, the sender waits to receive back an acknowledge message within 5 seconds (timespan for testing purposes), if not it attempts to resend it again.

## Assumptions
* Displayed names are unique

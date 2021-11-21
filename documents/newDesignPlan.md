# Design Plan

Group members **Kristian Krok**, **Laura North**, **Aksel Linros** and **Niko Häppölä**.

Norris Chat System is an instant messaging system for *Distributed Systems* -course in University of Helsinki.

## Description of the topic

In this project we will create a distributed chat system, where users can broadcast messages to every other user in the network. All users are free to join and leave at any time, and will see the messages sent in the same order as everyone else. Receiving messages happens only when user is online, and the system does not save any previous messages.
The project will be implemented with Python, Docker and possibly FastAPI or RabbitMQ as the message broker.


## Nodes

A user is a single node in the system. There are no centralized servers, so the whole network consists of user nodes. All the nodes are pluripotent, so depending on the situation they can be any of the three variations:

1) Host node. This is a special role for one user node that is needed for initializing connection of a new node. When a request to join the chat system comes, the host node will respond with information about all the nodes in the network, so that the new node can initialize communication paths. There must always be at least one host node, and the first node to start the network automatically gets assigned this role.

## Messages

*Description of messages sent and received (syntax and semantics).*



## Other comments

*How about scalability? Other things?*


# ~~Design Plan~~ Depricated!

Group members **Kristian Krok**, **Laura North**, **Aksel Linros** and **Niko Häppölä**.

Norris File System is a distributed file system implementation for *Distributed Systems* -course in University of Helsinki.

## Description of the topic

*More detailed description of topic, techniques or methods.*

- Distributed file system
- Allows saving and opening text files
- Maybe WORM-style? (Write Once, Read Many)
- Data is duplicated to at least two nodes, possible to configure?

## Nodes

*Description of different node, their roles and functionalities.*

- In practice, nodes are virtual machines
- We'll use KVM
- One node at the time is the main node
- Main node handles other nodes and data locations etc.
- If main node crashes, a new one is raised from other nodes (by some logic)

## Messages

*Description of messages sent and received (syntax and semantics).*

- Messaging over internet, basic HTTP-messaging (GET, PUT)?

## Other comments

*How about scalability? Other things?*

- Should be scalable up to x machines
- Scaling will mainly increase storage, maybe fault tolerance too?
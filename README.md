# Norris Chat System

Project work for University of Helsinki course Distributed Systems fall 2021.

***

Simple instant messaging system without dedicated server. Starting node handles message broadcasting and can (almost) be replaced should the first one disconnect.


## Documentation

Teachers are able to find more detailed description in Final Report of the Project.

- [Design plan](https://github.com/kriskrok/norris-chat-system/blob/main/documents/design_plan.md)
- [Architecture diagram](https://github.com/kriskrok/norris-chat-system/blob/main/documents/updated_architecture-diagram.svg)
- [Final report](https://github.com/kriskrok/norris-chat-system/blob/main/documents/group18_final_report.pdf)

## Use instructions

Configure three env variables before running the app: HOSTNAME, MYIP and LEADER. HOSTNAME should be the IP of the leader node, MYIP your own IP and LEADER either 'True' if you are leading chat (as in starting first) or 'False' otherwise.

For example:

```
export MYIP='192.168.124.12'
export CHATHOST='92.168.124.63'
export LEADER='False'
```

Navigate to \src\ and start the node with

```
python3 chat.py
```

You have to insert a nickname before joining the chat.
# Use instructions

Configure three env variables before running the app: HOSTNAME, MYIP and LEADER. HOSTNAME should be the IP of the leader node, MYIP your own IP and LEADER either 'True' if you are leading chat or 'False' otherwise.

For example:

```
export MYIP='192.168.124.12'
export CHATHOST='92.168.124.63'
export LEADER='False'
```

Start the node with

```
python3 chat.py
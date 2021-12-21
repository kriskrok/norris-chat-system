# Server instructions

**DEPRECATED**

Install dependencies with

```
pip install -r requirements.txt
```

Then configure two env variables: CHATHOST and MYIP. CHATHOST should be the IP of the host node, and MYIP your own.
For example if host node IP was 192.168.124.63 and my IP 192.168.124.12:

```
export MYIP='192.168.124.12'
export CHATHOST='92.168.124.63'
```

Start the node with

```
python3 main.py
```


## server.py instructions

**Follow these**

Configure three env variables: HOSTNAME, MYIP and LEADER. HOSTNAME should be the IP of the leader node, MYIP your own IP and LEADER either 'True' if you are leading chat or 'False' otherwise.

For example:

```
export MYIP='192.168.124.12'
export CHATHOST='92.168.124.63'
export LEADER='False'
```

Start the node with

```
python3 chat.py
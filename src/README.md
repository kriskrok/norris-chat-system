# Server instructions

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

Environment variable is HOSTNAME. Use otherwise instructions above.
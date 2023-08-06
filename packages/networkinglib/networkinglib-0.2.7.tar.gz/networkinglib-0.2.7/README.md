# networkinglib
Python Networking Module

## How to use



### TCP Client
#### Opening socket and connecting to server
```Python
from networkinglib import tcp
socket = tcp.connect('127.0.0.1', 7777)
if not socket: print("Could not connect!")
```

#### Sending packet
```Python
socket.send("Hello Server!")
```

#### Receiving Packets
```Python
print(socket.receive())
```

#### Closing connection
```Python
socket.close()
```



### UDP Client
#### Opening socket
```Python
from networkinglib import udp
socket = udp.open()
if not socket: print("An unexpected error occured!")
```

#### Sending packet
```Python
socket.send("Hello Server!", "127.0.0.1", 7777)
# or
socket.send("Hello Server!", "127.0.0.1:7777")
```

#### Receiving Packets
```Python
msg, source_address, source_port = socket.receive()
print('Received:\n', msg, 'From:\n', source_address + ':' + str(source_port))
```

#### Closing connection
```Python
socket.close()
```

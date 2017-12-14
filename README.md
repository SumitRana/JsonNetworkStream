# JsonNetworkStream
Python library for making network stream communication following a 'json' based communication protocol .
Library provide client-server-client based communication , with additional option of peer to peer private key based encryption ( AES - Advanced Encryption Standard ).


## Client Side Docs :

```python
import client

# Declare client object 
#  port - port address ,host - ip address of server , encryption_key - 16 bit long string 
clientObject = client.DataStreamClient(host,port=12222,encryption_key)

# register client 
clientObject.register_client(username,password,user_description)

# login client 
clientObject.login(username,password)

# register listener - listener method is passed with data 
clientObject.register_event_listener(listener=your_listener_method)

# Send Message 
clientObject.send_message(to=receiver_username,data=data_string,**optional_json_data_keys)

# logout Client 
clientObject.logout()
```

## Server Side Docs :

```python
import server 

# Declare Server Object :
# server runs on the machine in which installed , using the port address specified
serverObject = server.DataStreamServer(port=12222)

# register client
serverObject.register_user(username,password,user_description)

# kill server
serverObject.stop_server()
```

* For adding peer to peer encryption of data , a 16-characters long string is shared privately by both the clients ( as it is private key based encryption ).

#### * [Install with pip](https:#pypi.python.org/pypi/JsonNetworkStream/2.0) - pip install JsonNetworkStream
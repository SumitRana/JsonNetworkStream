# JsonNetworkStream
Python library for making network stream communication following a 'json' based communication protocol .
Library provide client-server-client based communication , with additional option of peer to peer encryption.


# Client side docs :
import client

#Declare client object \n
#port - port address ,host - ip address of server , encryption_key - 16 bit long string
clientObject = client.DataStreamClient(host,port=12222,encryption_key)

#register client \n
clientObject.register_user(username,password,description)

#login client \n
clientObject.login(username,password)

#register listener - listener method is passed with data \n
clientObject.register_event_listener(listener=your_listener_method)

#Send Message \n
clientObject.send_message(to=receiver_username,data=data_string,**optional_json_data_keys)

#logout Client \n
clientObject.logout()
Client side docs - 

message load protocol - json
{ "type": "message",
  "to_user": "(username)",
  "from_user": "(username)",
  "time": "(in ISO format)", 
  "data": "(always a json dictionary)"
  }

presence log
{ "username": "(username)",
  "password": "",
	"type": "presence",
  "is_online": "true" }



Server Side Docs - 


message load protocol - json
{ "type": "message",
  "to_user": "(username)",
  "from_user": "(username)",
  "time": "(in ISO format)", 
  "data": "(always a json dictionary)"
  }

offline dump
[{"username": [message_json ,message_json , ..]
	}, ..
]

registered users
[{ 'username': "",
	'password': "",
	'name': "",
	'presence': ""
	}, ..
]


Registration Protocol - 

{ "type": "registration",
  "username": "",
  "password": "",
  "name": ""
  }
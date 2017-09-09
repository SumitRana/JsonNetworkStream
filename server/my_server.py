import socket
import pickle
import json
import os
import threading

from secure import *


class DataStreamServer:
	s = None
	port = None
	host = None
	kill_server = False
	server_encryption_key = None

	# variables
	users = []
	online_users = [] #contains list of - tuple(stream,username)
	online_users_username = []
	offline_dump = dict()
	encdec_key = None

	def __init__(self,port=12301,encryption_key=None):
		import json
		self.encdec_key = encryption_key
		self.start_server(port)

	def initialize(self):
		with open(os.getcwd()+"/registered_users.pickle","w") as f:
			pickle.dump([],f)
		with open(os.getcwd()+"/offline_user_data.pickle","w") as f:
			pickle.dump([],f)
		return 200

	def register_user(self,username,password,name):
		d = dict()
		d['username'] = username
		d['password'] = password
		d['name'] = name
		d['presence'] = 0
		try:
			with open(os.getcwd()+"/registered_users.pickle","r") as f:
				self.users = pickle.load(f)
		except IOError:
			self.users = []
		try:
			for user in self.users:
				if user['username'] == username:
					raise ValueError("UserName Exists .")
			self.users.append(d)
			with open(os.getcwd()+"/registered_users.pickle","w") as f:
				pickle.dump(self.users,f)
		except ValueError as v:
			return 500

		try:
			with open(os.getcwd()+"/offline_user_data.pickle","r") as f:
				self.offline_dump = pickle.load(f)
		except IOError:
			self.offline_dump = dict()

		self.offline_dump[str(username)] = []
		with open(os.getcwd() + "/offline_user_data.pickle", "w") as f:
			pickle.dump(self.offline_dump,f)
		return d

	def receive(self,stream):
		thread_counter = 0
		while True:
			try:
				r = str(stream.recv(1024))
				# if self.encdec_key is not None:
				# 	r = manual_decrypt(self.encdec_key,r,"AES",self.encdec_key)
				dump = json.loads(r)
				if dump['type'] == "presence":					
					user_exist = False
					with open(os.getcwd()+"/registered_users.pickle","r") as f:
						self.users = pickle.load(f)
						for user in self.users:
							if user['username'] == dump['username']:
								user['presence'] = dump['is_online']
								user_exist = True
					

					if user_exist:
						#for saving stream class - socket class
						
						u = (stream ,dump['username'])
						
						if u not in self.online_users:
							self.online_users.append(u)
							self.online_users_username.append(str(dump['username']))
							#sending offline queue to user
							with open(os.getcwd()+"/offline_user_data.pickle","r") as f:
								self.offline_dump = pickle.load(f)

							for mes in self.offline_dump[str(dump["username"])]:
								stream.sendall(json.dumps(mes))
							self.offline_dump[str(dump["username"])] = []

							with open(os.getcwd()+"/offline_user_data.pickle","w") as f:
								pickle.dump(self.offline_dump,f)
						else:
							raise Exception("User Already logged in .")
							break
						#sending offline dump
					else:
						raise Exception("User not registered .")

				elif dump['type'] == "registration":
					self.register_user(username=dump['username'],password=dump['password'],name=dump['name'])

				elif dump['type'] == "message":
					if str(dump['to_user']) in self.online_users_username:#if 'to' is online
						for to_user_stream,username in self.online_users:
							if username == dump['to_user']:
								to_user_stream.send(json.dumps(dump))
					else:
						with open(os.getcwd()+"/offline_user_data.pickle","r") as f:
							self.offline_dump = pickle.load(f)
						try:
							self.offline_dump[dump['to_user']].append(dump)
						except Exception:
							self.offline_dump[str(dump['to_user'])] = [dump]
						with open(os.getcwd()+"/offline_user_data.pickle","w") as f:
							pickle.dump(self.offline_dump,f)
				
			except Exception as e:#can be raised to kill client listening thread
				break
		return True

	# def send(self,stream):
	# 	while True:
	# 		m = str(raw_input())
	# 		if m == "purge":
	# 			print "inside purge"
	# 			c.sendall("Server left the conversation..")
	# 			s.close()
	# 			print "Connection closed at your end."
	# 			break
	# 		stream.sendall(m+'\n')
	# 	return True

	class serverThread(threading.Thread):
		thread_stream = None
		parent_context = None

		def __init__(self,stream,context):
			threading.Thread.__init__(self)
			self.thread_stream = stream
			self.parent_context = context

		def run(self):
			self.parent_context.receive(self.thread_stream)

	def start_server(self,p):
		self.s = socket.socket()  # Create a socket object
		self.host = socket.gethostname()  # Get local machine name
		self.port = p  # Reserve a port for your service.
		print self.port
		print p
		self.s.bind(('0.0.0.0', self.port))  # Bind to the port
		self.s.listen(5)

		try:
			while self.kill_server is not True:
				d = dict()
				c, addr = self.s.accept()  # Establish connection with client.
				t1 = self.serverThread(stream=c,context=self)
				t1.daemon = True
				t1.start()
		except Exception as e:
			print "Error:" + str(e)

	def stop_server(self):
		self.kill_server = False
		self.s.close()
		return 200

	# class destructor
	def __del__(self):
		self.stop_server()
		del self.s
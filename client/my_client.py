import socket
import thread
import threading
import time
import sys
from datetime import datetime as dt
import json

from secure.encdec import *


class DataStreamClient:
	stream = None #socket

	#variables
	sending_data_queue = [] # contains list of message loads to be send

	#event listeners
	receiver = None
	kill_receiver = False
	kill_client = False

	#global variables
	encdec_key = None
	host_address = None
	port_address = None
	is_online = None
	user = None
	pas = None

	def __init__(self,host="127.0.0.1",port=12301,encryption_key=None):
		self.encdec_key = encryption_key
		self.start_client(host,port)

	def register_event_listener(self,listener_type="data-receiver",listener=None):
		if listener_type == "data-receiver":
			self.receiver = listener
		return 200

	def remove_event_listener(self,listener_type):
		if listener_type == "data-receiver":
			self.kill_receiver = True
			self.receiver = None
		return 200

	def send_presence(self):
		if self.is_online == True:
			d = dict()
			d['type'] = "presence"
			d['username'] = str(self.user)
			d['password'] = str(self.pas)
			d['is_online'] = True
			self.stream.sendall(json.dumps(d))
		return 200

	def send_message(self,to,data,**custom_data):
		core_data = { 'data': data }
		d=dict()
		d['type'] = "message"
		d['to_user'] = str(to)
		d['from_user'] = str(self.user)
		d['data'] = core_data
		d['time'] = str(dt.isoformat(dt.now()))
		d.update(custom_data)
		self.sending_data_queue.append(d)
		if self.encdec_key is not None:
			ed = manual_encrypt(self.encdec_key,str(json.dumps(core_data)),'AES',self.encdec_key)
			base64_encoded_string = base64.encodestring(ed)
			d['data'] = base64_encoded_string
			self.stream.sendall(json.dumps(d))
			# self.stream.sendall(manual_encrypt(self.encdec_key,json.dumps(d),'AES',self.encdec_key))
		else:
			self.stream.sendall(json.dumps(d))
		# self.stream.sendall(json.dumps(d))
		return 200

	def receive(self):
		while self.kill_client is False:
			if self.receiver is not None:
				try:
					r = str(self.stream.recv(1024))
					try:
						dump = json.loads(r)
						if self.encdec_key is not None:
							base64_decoded_string = base64.decodestring(dump['data'])
							decrypted_string = manual_decrypt(self.encdec_key,base64_decoded_string,'AES',self.encdec_key)
							dump["data"] = json.loads(decrypted_string)
							# dd = manual_decrypt(self.encdec_key,dump["data"],'AES',self.encdec_key)
						try:
							self.receiver(dump)
							continue
						except TypeError:
							pass
					except ValueError:
						pass
				except Exception as e:
					print str(e)
					pass
		return True

	class clientThread(threading.Thread):
		parent_context = None
		def __init__(self,context):
			threading.Thread.__init__(self)
			self.parent_context = context

		def run(self):
			self.parent_context.receive()


	def start_client(self,host,port):
		if self.stream is None:
			self.stream = socket.socket()         # Create a socket object
			self.port_address = int(port)         # Reserve a port for your service.
			self.host_address = host         # host to connect to
			self.stream.connect((self.host_address, self.port_address))
			try:
				t1 = self.clientThread(context=self)
				t1.start()
			except Exception as e:
				return 500
		else:
			return "Client Already running ."
		return 200

	def login(self,username,password):
		self.user = str(username)
		self.pas = str(password)
		self.is_online = True
		self.send_presence()
		return 200


	def register_client(self,username,password,description=""):
		d = dict()
		d['type'] = "registration"
		d['username'] = str(username)
		d['password'] = str(password)
		d['name'] = str(description)
		self.stream.sendall(json.dumps(d))
		return 200

	def stop_client():
		self.kill_client = True
		self.stream.sendall("kill Client Connection .")
		self.stream.close()
		return 200

	def logout():
		return stop_client()

	# class destructor
	def __del__(self):
		self.stop_client()
		del stream
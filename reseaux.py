import socket

class Reseaux:

	sock = 0

	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self, host, port):
		self.sock.connect((host, port))

	def quitter(self):
		self.sock.close()

	def sendChar(self, c):
		self.sock.send(c)

	def sendString(self, str):
		self.sock.send(str)

	def get(self, size):
		return self.sock.recv(size)

	def getString(self):
		res = ""
		c   = ''
		while(c != '\0'):
			c = self.sock.recv(1)
			print c
			if(c != '\0'):
				res += c
		return res

	def getInt(self):
		return ord(self.sock.recv(1))

	def getChar(self):
		return chr(ord(self.sock.recv(1)))
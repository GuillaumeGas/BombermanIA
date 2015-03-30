import sys
from reseaux import *
from ia import *

class Bomberman:
	reseau = Reseaux()
	ia = Ia(2) #1 ou alea, 2 pour evoluee (soon...)
	ID = 0
	l = 0
	c = 0
	mapp = []
	bombes = []
	mort = False

	def connect(self, host, port, pseudo):
		self.reseau.connect(host, port)
		self.reseau.sendString("LOGIN " + pseudo + "\0")

	def getSpec(self):
		print("GET SPEC")
		self.reseau.getString()
		self.ID = self.reseau.getChar()
		self.l = self.reseau.getInt()
		self.c = self.reseau.getInt()

		for i in range(self.l):
			self.mapp.append(['0']*self.c)

	def getMap(self):
		res = self.reseau.getString()
		if res == "DEAD":
			self.mort = True
		else:
			print("GET MAP")
			for i in range(self.l):
				for j in range(self.c):
					self.mapp[i][j] = self.reseau.getChar()

			nb_bombes = self.reseau.getInt()
			self.bombes = []
			for i in range(nb_bombes):
				by = self.reseau.getInt()
				bx = self.reseau.getInt()
				self.bombes.append((bx,by))

	def afficherMap(self):
		s = '+'
		for i in range(self.c):
			s += '-'
		s += '\n'
		for i in range(self.l):
			s += '|'
			for j in range(self.c):
				s += self.mapp[i][j]
			s += '|\n'
		s += '+'
		for i in range(self.c):
			s += '-'
		s += '+\n'
		print(s)

		for i in range(len(self.bombes)):
			(x, y) = self.bombes[i]
			print("bombe " + str(i) + " (" + str(x) + ", " + str(y) + ")")

	def jouerCoup(self):
		action = self.ia.jouerCoup(self.l, self.c, self.mapp, self.bombes, self.ID)
		print("Action : " + action+";")
		self.reseau.sendChar(action)

	def gameOver(self):
		return self.mort


bb = Bomberman()
bb.connect(sys.argv[2], int(sys.argv[3]), sys.argv[1])
bb.getSpec()

while(bb.gameOver() == False):
	bb.getMap()
	bb.afficherMap()
	bb.jouerCoup()

bb.reseau.quitter()


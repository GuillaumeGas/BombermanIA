from random import randint

class Etat:
	(NORMAL, FUITE) = range(2)

class Ia:

	def __init__(self, num=1):
		self.num = num
		self.etat = Etat.NORMAL
		self.liste_actions = []

	def jouerCoup(self, l, c, mapp, bombes, ID):
		if self.num == 1:
			return self.jouerCoupAlea(l, c, mapp, bombes, ID)
		else:
			return self.jouerCoupEvol(l, c, mapp, bombes, ID)

	def jouerCoupAlea(self, l, c, mapp, bombes, ID):

		(posx, posy) = self.getPosIa(l, c, mapp, ID)

		while(True):
			action = randint(0, 4)
			if action == 0 and self.caseAccessible(l, c, mapp, posx, posy-1):
				return 'N'
			if action == 1 and self.caseAccessible(l, c, mapp, posx, posy+1):
				return 'S'
			if action == 2 and self.caseAccessible(l, c, mapp, posx+1, posy):
				return 'E'
			if action == 3 and self.caseAccessible(l, c, mapp, posx-1, posy):
				return 'W'
			if action == 4:
				return 'B'

	def jouerCoupEvol(self, l, c, mapp, bombes, ID):
		
		(posx, posy) = self.getPosIa(l, c, mapp, ID)		

		if self.etat == Etat.FUITE:
			print "FUITE"
			action_prevue = self.liste_actions[len(self.liste_actions)-1]

			if action_prevue == 'N' or action_prevue == 'S':
				if self.caseAccessible(l, c, mapp, posx+1, posy):
					self.liste_actions = []
					self.liste_actions.append('E')
					self.etat = Etat.NORMAL
				elif self.caseAccessible(l, c, mapp, posx-1, posy):
					self.liste_actions = []
					self.liste_actions.append('W')
					self.etat = Etat.NORMAL
			elif action_prevue == 'E' or action_prevue == 'W':
				if self.caseAccessible(l, c, mapp, posx, posy+1):
					self.liste_actions = []
					self.liste_actions.append('S')
					self.etat = Etat.NORMAL
				elif self.caseAccessible(l, c, mapp, posx, posy-1):
					self.liste_actions = []
					self.liste_actions.append('N')
					self.etat = Etat.NORMAL

			print "Case SUD ("+str(posx%c)+","+str((posy+1)%l)+") = "+mapp[(posy+1)%l][posx%c]+";"

			if len(self.liste_actions) == 1:
				self.etat = Etat.NORMAL

		else:
			(x, y) = self.dansRayonActionBombe(l, c, mapp, bombes, posx, posy)
			if x > -1 and y > -1:
				print "BOMB A PROXIMITE"
				(action, nb) = self.determinerDirectionFuite(l, c, mapp, x, y, posx, posy)
				for i in range(nb):
					self.liste_actions.append(action)
				if nb > 1:
					self.etat = Etat.FUITE	
			elif self.ennemyProche(l, c, mapp, posx, posy, ID):
				print "ENEMY DETECTE"
				self.liste_actions.append('B')
			else:
				print "MOUVEMENT"
				self.liste_actions.append(self.mouvementAleatoire(l, c, mapp, posx, posy))

		return self.liste_actions.pop()


	def getPosIa(self, l, c, mapp, ID):
		for i in range(c):
			for j in range(l):
				if mapp[j][i] == ID:
					print "ID : ("+str(i)+","+str(j)+")"
					return (i, j)

	def caseAccessible(self, l, c, mapp, x, y):
		x %= c
		y %= l
		if(mapp[y][x] != 'X'):
			print "Case ("+str(x)+","+str(y)+") : "+mapp[y][x]+";"
			return True
		return False

	#cherche si le joueur en posx, posy est dans le rayon d'action d'une bombe. Si oui, renvoie la pos de cette bombe
	#Return : (x, y) ou (-1, -1) si pas de bombes
	def dansRayonActionBombe(self, l, c, mapp, bombes, posx, posy):
		print "Detection bombe..."

		for i in range(len(bombes)):
			(bx, by) = bombes[i]
			if (posx >= ((bx-3)%c) and posx <= ((bx+3)%c)) or (posy >= ((by-3)%l) and posy <= ((by+3)%l)):
				return (bx, by)
		return (-1, -1)

	#determine ou aller en fonction de la bombe en x, y, et du joueur en posx, posy, 
	#ainsi que le nombre de deplacement a effectuer (ligne droite)
	#Return : (action, nombre)
	def determinerDirectionFuite(self, l, c, mapp, x, y, posx, posy):
		print "Determination direction fuite... bombe("+str(x)+","+str(y)+") J("+str(posx)+","+str(posy)+")"

		if x == posx and y == posy:
			if self.caseAccessible(l, c, mapp, posx, posy-1):
				return ('N', 1)
			if self.caseAccessible(l, c, mapp, posx, posy+1):
				return ('S', 1)
			if self.caseAccessible(l, c, mapp, posx+1, posy):
				return ('E', 1)
			if self.caseAccessible(l, c, mapp, posx-1, posy):
				return ('W', 1)
		else:
			if x != posx:
				if self.caseAccessible(l, c, mapp, posx, posy+1):
					return ('S', 1)
				elif self.caseAccessible(l, c, mapp, posx, posy-1):
					return ('N', 1)
				else:
					if x < posx:
						nb = (((x-4)%c)-posx)%c
						return ('W', nb)
					if x > posx:
						nb = (((x-4)%c)-posx)%c
						return ('E', nb)
			else:
				if self.caseAccessible(l, c, mapp, posx+1, posy):
					return ('E', 1)
				elif self.caseAccessible(l, c, mapp, posx-1, posy):
					return ('W', 1)
				else:
					if y < posy:
						nb = (((y-4)%l)-posy)%l
						return ('N', nb)
					if y > posy:
						nb = (((y-4)%l)-posy)%l
						return ('S', nb)

	#determine si un enemy est proche (dans le rayon d action de notre bombe si on la pose)
	#Return : True si oui sinon False
	def ennemyProche(self, l, c, mapp, posx, posy, ID):
		print "Determination ennemy proche..."

		pos = posx
		while pos >= posx-3 and pos >= 0:
			if ord(mapp[posy][pos]) != ID and ord(mapp[posy][pos]) > 0 and ord(mapp[posy][pos]) < 9:
				return True
			pos = (pos-1)%c
		pos = posx
		while pos <= posx+3 and pos < c:
			if ord(mapp[posy][pos]) != ID and ord(mapp[posy][pos]) > 0 and ord(mapp[posy][pos]) < 9:
				return True
			pos = (pos+1)%c
		pos = posy
		while pos >= posy-3 and pos >= 0:
			if ord(mapp[pos][posx]) != ID and ord(mapp[pos][posx]) > 0 and ord(mapp[pos][posx]) < 9:
				return True
			pos = (pos-1)%l
		pos = posy
		while pos <= posy+3 and pos < l:
			if ord(mapp[pos][posx]) != ID and ord(mapp[pos][posx]) > 0 and ord(mapp[pos][posx]) < 9:
				return True
			pos = (pos+1)%l
		
		return False

	def mouvementAleatoire(self, l, c, mapp, posx, posy):
		print "Determination mouvement aleatoire..."

		while(True):
			action = randint(0, 4)
			if action == 0 and self.caseAccessible(l, c, mapp, posx, posy-1):
				return 'N'
			if action == 1 and self.caseAccessible(l, c, mapp, posx, posy+1):
				return 'S'
			if action == 2 and self.caseAccessible(l, c, mapp, posx+1, posy):
				return 'E'
			if action == 3 and self.caseAccessible(l, c, mapp, posx-1, posy):
				return 'W'
			if action == 4:
				return 'B'

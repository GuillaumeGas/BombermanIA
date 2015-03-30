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
			action_prevue = self.liste_actions[len(self.liste_actions)-1]

			if action_prevue == 'N' or action_prevue == 'S':
				if self.caseAccessible(l, c, mapp, posx+1, posy):
					self.liste_actions = []
					self.liste_actions.append('E')
					self.etat = Etat.NORMAL
				else if self.caseAccessible(l, c, mapp, posx-1, posy):
					self.liste_actions = []
					self.liste_actions.append('W')
					self.etat = Etat.NORMAL
			else if action_prevue == 'E' or action_prevue == 'W':
				if self.caseAccessible(l, c, mapp, posx, posy+1):
					self.liste_actions = []
					self.liste_actions.append('S')
					self.etat = Etat.NORMAL
				else if self.caseAccessible(l, c, mapp, posx, posy-1):
					self.liste_actions = []
					self.liste_actions.append('N')
					self.etat = Etat.NORMAL
			else:
				if len(self.liste_actions) == 1:
					self.etat = Etat.NORMAL

		else:
			(x, y) = self.dansRayonActionBombe(l, c, mapp, bombes, posx, posy)
			if x > -1 and y > -1:
				(action, nb) = self.determinerDirectionFuite(l, c, mapp, x, y, posx, posy)
				for i in range(nb):
					self.liste_actions.append(action)
				if nb > 1:
					self.etat = Etat.FUITE	
			else if self.enemyProche(l, c, mapp, posx, posy):
				self.liste_actions.append('B')
			else:
				self.liste_actions.append(self.mouvementAleatoire(l, c, mapp, posx, posy))

		return self.liste_actions.pop()


	def getPosIa(self, l, c, mapp, ID):
		for i in range(l):
			for j in range(c):
				if mapp[j][i] == ID:
					return (j, i)

	def caseAccessible(self, l, c, mapp, x, y):
		if(x >= 0 and x < c and y >= 0 and y < l):
			if(mapp[x][y] != 'X'):
				return True
		return False



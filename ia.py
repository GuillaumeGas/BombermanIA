from random import randint

class Ia:

	def __init__(self, num=1):
		self.num = num

	def jouerCoup(self, l, c, mapp, bombes, ID):
		if self.num == 1:
			return self.jouerCoupAlea(l, c, mapp, bombes, ID)
		else:
			return 'N' #tmp...

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



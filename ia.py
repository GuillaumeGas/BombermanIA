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
		action = randint(0, 4)
		if action == 0:
			return 'N'
		if action == 1:
			return 'S'
		if action == 2:
			return 'E'
		if action == 3:
			return 'W'
		if action == 4:
			return 'B'



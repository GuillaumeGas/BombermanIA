from random import Random

class Ia:

	def __init__(self, num=1):
		self.num = num

	def jouerCoup(self, l, c, mapp, bombes, ID):
		if self.num == 1:
			return self.jouerCoupAlea(l, c, mapp, bombes, ID)
		else:
			return 'N' #tmp...

	def jouerCoupAlea(self, l, c, mapp, bombes, ID):
		return 'N'



class JudgeMap:
	def __init__(self, li):
		self.li = li	# map
		self.la = []	# coordinate of attack
		self.ld = []	# coordinate of defend
		self.ls = []	# coordinate of source

		for i in range(len(li)):
			for j in range(len(li[0])):
				if li[i][j] == 'A':
					self.la.append([i,j])
				elif li[i][j] == 'D':
					self.ld.append([i,j])
				elif li[i][j] == '$':
					self.ls.append([i,j])
				elif li[i][j] == '@':
					self.ld.append([i,j])
					self.ls.append([i,j])

	def GetValue(self):
		
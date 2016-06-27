#	information:
#		1.we assume that the number of 'A' can be diffend from 'D'
#		2.'D' first
#		3.if losing 2 or more than 2 '$'s, we will lose the game


def ADCmp(var1, var2):	# sig:1 - Attack and sig:2 - Defend, of course Attack first
	if var1[0] == var2[0]:	# struct {time ,sig}
		return var2[1] - var1[1]
	else:
		return var1[0] - var2[0]
	

class JudgeMap:
	def __init__(self, li):

		
		# The information of Map
		
		self.li = li
		self.xSiz = len(li[0])
		self.ySiz = len(li)

		self.la = []	# coordinate of attack
		self.ld = []	# coordinate of defend

		self.ls = []	# coordinate of source
		self.dis_a = {}
		self.dis_d = {}

	def GetInformation(self):
		for i in range(len(self.li)):
			for j in range(len(self.li[0])):	
				if self.li[i][j] == 'A':
					self.la.append([i,j])
				elif self.li[i][j] == 'D':
					self.ld.append([i,j])
				elif self.li[i][j] == '$':
					self.ls.append([i,j])
				elif self.li[i][j] == '@':
					self.ld.append([i,j])
					self.ls.append([i,j])

		for i in range(len(self.ls)):
			self.GetDis(i)

	def GetDis(self, id):
		dx = [0, 0, 1, -1]
		dy = [1, -1, 0, 0]
		vis = [([-1] * len(self.li[0])) for i in range(len(self.li))]
		vis[self.ls[id][0]][self.ls[id][1]] = 0
		now = [self.ls[id][0],self.ls[id][1]]
		que = [[self.ls[id][0],self.ls[id][1]]]
		while(len(que) != 0):
			now = que[0]
			for i in range(4):
				nexx = now[0] + dx[i]
				nexy = now[1] + dy[i]
				if nexx >= 0 and nexx < self.ySiz and nexy >= 0 and nexy < self.xSiz and self.li[nexx][nexy] != 'x' and vis[nexx][nexy] == -1:
					nex = [nexx, nexy]
					vis[nexx][nexy] = vis[now[0]][now[1]] + 1
					que.append(nex)
			del que[0]
		self.dis_a[id] = []
		self.dis_d[id] = []
		for i in range(len(self.la)):
			self.dis_a[id].append(vis[self.la[i][0]][self.la[i][1]])
		for i in range(len(self.ld)):
			self.dis_d[id].append(vis[self.ld[i][0]][self.ld[i][1]])

	'''
	def AttackCount(self):
		Attack_success = 0
		LenofSource = len(self.ls)
		LenofAttack = len(self.la)
		LenofDefend = len(self.ld)
		for AttackWay in range(LenofSource ** LenofAttack):
			try_success = LenofSource
			for DefendWay in range(LenofSource ** LenofDefend):
				#print '------------', AttackWay, DefendWay
				Now = [([]) for i in range(len(self.ls))]		# list of struct {time, sig} sig 1-attack 2-defend
				TmpAttackWay = AttackWay
				for i in range(LenofAttack):
					AimSource = TmpAttackWay % LenofSource
					TmpAttackWay /= LenofSource
					Now[AimSource].append([self.dis_a[AimSource][i], 1])
				TmpDefendWay = DefendWay
				for i in range(LenofDefend):
					AimSource = TmpDefendWay % LenofSource
					TmpDefendWay /= LenofSource
					Now[AimSource].append([self.dis_d[AimSource][i], 2])
				for i in range(len(Now)):
					Now[i].sort(cmp = ADCmp)
					#print i, '=', Now[i]
				#print '-----------'
				Can_Attack = 0
				for i in range(len(Now)):
					cnt = 0
					for j in range(len(Now[i])):
						if Now[i][j][1] == 1: cnt -= 1
						else: cnt += 1
						if cnt < 0:
							Can_Attack += 1
							break
				try_success = min(try_success, Can_Attack)
			Attack_success = max(Attack_success, try_success)
		return Attack_success
	'''

	def DefendCount(self):
		LenofSource = len(self.ls)
		LenofAttack = len(self.la)
		LenofDefend = len(self.ld)
		Defend_success = LenofSource
		for AttackWay in range(LenofSource ** LenofAttack):
			try_success = 0
			for DefendWay in range(LenofSource ** LenofDefend):
				#print '------------', AttackWay, DefendWay
				Now = [([]) for i in range(len(self.ls))]		# list of struct {time, sig} sig 1-attack 2-defend
				TmpAttackWay = AttackWay
				for i in range(LenofAttack):
					AimSource = TmpAttackWay % LenofSource
					TmpAttackWay /= LenofSource
					Now[AimSource].append([self.dis_a[AimSource][i], 1])
				TmpDefendWay = DefendWay
				for i in range(LenofDefend):
					AimSource = TmpDefendWay % LenofSource
					TmpDefendWay /= LenofSource
					Now[AimSource].append([self.dis_d[AimSource][i], 2])
				for i in range(len(Now)):
					Now[i].sort(cmp = ADCmp)
					#print i, '=', Now[i]
				#print '-----------'
				Can_Defend = 0
				for i in range(len(Now)):
					cnt = 0
					for j in range(len(Now[i])):
						if Now[i][j][1] == 1: cnt -= 1
						else: cnt += 1
						if cnt < 0: break
					if cnt >= 0:
						Can_Defend += 1
				try_success = max(try_success, Can_Defend)
			Defend_success = min(Defend_success, try_success)
		return Defend_success


# Reference:
#	sometime we may use one 'D' protect more than one source,now we can just use 'Attack_success' to judge
#	for example:
#		.....
#		..A..
#		..D..
#		.$..$
#		...$.
#
#	but for some instance:
#		.....
#		.A...
#		.$$..
#		..D..
#		.....
#	it seems that it is not as useful as before, we can add parameter 'Defend_success' to judge
#
#	so,both 'Attack_success' and 'Defend_success' are necessery.And the way get them is similar
#


	def GetValue(self):
		self.GetInformation()

		#for l in self.li:
		#	print l
		#print self.dis_a
		#print self.dis_d

		Defend_success = self.DefendCount()

		#print 'Defend_success = ', Defend_success

		if Defend_success >= 3:
			return 1.0
		else:
			return -1.0


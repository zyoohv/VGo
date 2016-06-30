from Judge import JudgeMap
import copy, math, sys, random
import threading


NumofThread = 15

Lock = threading.Lock()

class Node():
	def __init__(self, li, deep):
		self.L = 0		# Lose
		self.W = 0		# Win
						# Q = W / N 
		self.d = deep 	# deep of the node, 'root' is 1

		self.li = li	# map
		self.xSiz = len(li[0])
		self.ySiz = len(li)
		self.son = []	# son

		self.NumofSource = 0
		self.sig = {}	# the local of defend/attack
		self.cnt = 0	# the number of defends/attack
		if self.d % 2:
			for i in range(len(li)):
				for j in range(len(li[0])):
					if li[i][j] == 'D' or li[i][j] == '@':
						self.sig[self.cnt] = [j, i]
						self.cnt += 1
					if li[i][j] == '$' or li[i][j] == '@':
						self.NumofSource += 1
		else:
			for i in range(len(li)):
				for j in range(len(li[0])):
					if li[i][j] == 'A':
						self.sig[self.cnt] = [j, i]
						self.cnt += 1
					if li[i][j] == '$' or li[i][j] == '@':
						self.NumofSource += 1
		'''
			O-------sig[][0]----->xSiz
			|
			|
			|
			|
		sig[][1]
			|
			|
			|
			|
			v
			ySiz
		'''

	def UnfoldSon(self, Son_id):
		dx = [0, 0, 0, 1, -1]
		dy = [0, 1, -1, 0, 0]
		for i in range(5 ** self.son[Son_id].cnt):
			div = i
			nexl = copy.deepcopy(self.son[Son_id].li)
			move_success = 0	# sign if move successfully
			for j in range(self.son[Son_id].cnt):	# chose the Son_id='j' to move
				nexx = self.son[Son_id].sig[j][0] + dx[div % 5]
				nexy = self.son[Son_id].sig[j][1] + dy[div % 5]
				div /= 5
				if nexx >= 0 and nexx < self.xSiz and nexy >= 0 and nexy < self.ySiz and nexl[nexy][nexx] !='x' and nexl[nexy][nexx] != 'A':
					if nexl[nexy][nexx] == '.':
						nexl[nexy][nexx] = 'A'
					elif nexl[nexy][nexx] == 'D':
						nexl[nexy][nexx] = '.'
					elif nexl[nexy][nexx] == '$':	# 2new defending in source
						nexl[nexy][nexx] = '.'
					elif nexl[nexy][nexx] == '@':
						nexl[nexy][nexx] = '$'
					move_success += 1
					nexl[self.son[Son_id].sig[j][1]][self.son[Son_id].sig[j][0]] = '.'
				elif nexx == self.son[Son_id].sig[j][0] and nexy == self.son[Son_id].sig[j][1]:	# don't move it
					move_success += 1
			if move_success == self.son[Son_id].cnt:
				self.son[Son_id].son.append(Node(nexl, self.d + 2))


	def Unfold(self):		# unfold the node
		dx = [0, 0, 0, 1, -1]
		dy = [0, 1, -1, 0, 0]
		SearchList = range(5 ** self.cnt)
		random.shuffle(SearchList)
		for i in SearchList:		# hei hei...    :), yeah, maybe I'm serious...
			div = i
			nexl = copy.deepcopy(self.li)
			move_success = 0	# sign if move successfully
			for j in range(self.cnt):	# chose the id='j' to move
				nexx = self.sig[j][0] + dx[div % 5]
				nexy = self.sig[j][1] + dy[div % 5]
				div /= 5
				now_las = '$' if nexl[self.sig[j][1]][self.sig[j][0]] == '@' else '.'
				if nexx >= 0 and nexx < self.xSiz and nexy >= 0 and nexy < self.ySiz and nexl[nexy][nexx] !='x' and nexl[nexy][nexx] != 'D' and nexl[nexy][nexx] != '@':
					if nexl[nexy][nexx] == '.':
						nexl[nexy][nexx] = 'D'
					elif nexl[nexy][nexx] == 'A':
						nexl[nexy][nexx] = '.'
					elif nexl[nexy][nexx] == '$':	# 2new defending in source
						nexl[nexy][nexx] = '@'
					move_success += 1
					nexl[self.sig[j][1]][self.sig[j][0]] = now_las
				elif nexx == self.sig[j][0] and nexy == self.sig[j][1]:	# don't move it
					move_success += 1
			if move_success == self.cnt:
				self.son.append(Node(nexl, self.d + 1))
		for i in range(len(self.son)):
			self.UnfoldSon(i)


def ProgressBar(p):
	sys.stdout.write('[' + '#' * p + '.' * (50 - p) + ']' + str(p * 2) + '%\r')
	sys.stdout.flush()


WorkId = 0
root = 0
BreakSearch = 0

class Worker(threading.Thread):
	def __init__(self, name):
		threading.Thread.__init__(self)
		self.name = 'Thread-' + str(name)
		self.Nowid = 0
		#print self.name, 'WorkId =', WorkId

	def run(self):
		global root
		global WorkId
		global BreakSearch
		while True:
			if WorkId == len(root.son) or BreakSearch == 1: 
				break
			if Lock.acquire():
				ProgressBar(50 * (WorkId + 1) / len(root.son))
				self.Nowid = WorkId
				WorkId += 1
				Lock.release()
			#else:
			#	print 'waiting...' 
			#	continue
			Min_Defend = root.NumofSource
			for cas in root.son[self.Nowid].son:
				var = JudgeMap(cas.li)
				val = var.GetValue()
				Min_Defend = min(Min_Defend, val)
				if val >= 3:
					root.son[self.Nowid].W += 1
					root.W += 1.0
				else:
					root.son[self.Nowid].L += 1
					root.L += 1.0
			if Min_Defend == root.NumofSource:	# it is a perfect choice !
				root.son[self.Nowid].L = -1
			if root.son[self.Nowid].L == -1 and Lock.acquire():
				ProgressBar(50)
				BreakSearch = 1
				Lock.release()

def PrintTree(now):
	fout = open('debug.txt', 'w')
	fout.writelines('--------------deep : ' + str(now.d) + '\n')
	for i in now.li:
		fout.writelines(str(i) + '\n')
	fout.writelines('parameter- L: ' + str(now.L) + ' W: ' + str(now.W) + '\n\n')

	for i in range(len(now.son)):
		fout.writelines('----------id : ' + str(i) + '\n')
		for j in now.son[i].li:
			fout.writelines(str(j) + '\n')
		fout.writelines('parameter- L: ' + str(now.son[i].L) + ' W: ' + str(now.son[i].W) + '\n')
		fout.writelines('Num of sons : ' + str(len(now.son[i].son)) + '\n')
	fout.close()


def Search(Mps):
	global root
	global WorkId
	global NumofThread
	global BreakSearch
	root = Node(Mps, 1)
	root.Unfold()

	WorkId = 0
	BreakSearch = 0

	ThreadList = []
	for i in range(NumofThread):
		NewThread = Worker(i)
		ThreadList.append(NewThread)

	for i in range(NumofThread):
		ThreadList[i].start()

	for i in range(NumofThread):
		ThreadList[i].join()

	print ''
	li = []
	for i in range(len(root.son)):
		Wp = root.son[i].W
		Lp = root.son[i].L
		if Wp == 0 and Lp == 0: continue	# we know nothing about it
		li.append([1.0 * Wp / (1.0 + Lp + Wp), i])
	li.sort(key = lambda x:x[0], reverse = True)

	# debug
	#PrintTree(root)

	return  root.son[li[0][1]].li


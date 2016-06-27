from setting import L, N_thr, C_puct, P
from Judge import JudgeMap
import subprocess
import copy
import math
import sys


class Node():
	def __init__(self, li, deep):
		self.P = P 	# the talent of the node, we can use someway to make it better !
		self.N = 1.0
		self.W = 0.0
		#self.Q = 0		# Q = W / N 
		self.d = deep	# the deep of the node
		self.li = li	# map
		self.xSiz = len(li[0])
		self.ySiz = len(li)
		self.son = []	# son
		self.sig = {}	# the local of defend/attack
		self.cnt = 0	# the number of defends/attack

		if self.d % 2:
			for i in range(len(li)):
				for j in range(len(li[0])):
					if li[i][j] == 'D' or li[i][j] == '@':
						self.sig[self.cnt] = [j, i]
						self.cnt += 1
		else:
			for i in range(len(li)):
				for j in range(len(li[0])):
					if li[i][j] == 'A':
						self.sig[self.cnt] = [j, i]
						self.cnt += 1
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

	def UnfoldSon(self, id):
		dx = [0, 0, 0, 1, -1]
		dy = [0, 1, -1, 0, 0]
		for i in range(5 ** self.son[id].cnt):
			div = i
			nexl = copy.deepcopy(self.son[id].li)
			move_success = 0	# sign if move successfully
			for j in range(self.son[id].cnt):	# chose the id='j' to move
				nexx = self.son[id].sig[j][0] + dx[div % 5]
				nexy = self.son[id].sig[j][1] + dy[div % 5]
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
					nexl[self.son[id].sig[j][1]][self.son[id].sig[j][0]] = '.'
				elif nexx == self.son[id].sig[j][0] and nexy == self.son[id].sig[j][1]:	# don't move it
					move_success += 1
			if move_success == self.son[id].cnt:
				self.son[id].son.append(Node(nexl, self.d + 2))


	def Unfold(self):		# unfold the node
		if self.d >= L: return
		dx = [0, 0, 0, 1, -1]
		dy = [0, 1, -1, 0, 0]
		for i in range(5 ** self.cnt):
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
		for id in range(len(self.son)):
			self.UnfoldSon(id)



	def ChoseChild(self):	# chose the best child according formula : a = { Q + u }
		N = 0.0
		for son in self.son:
			N += son.N
		li = []
		for i in range(len(self.son)):
			li.append([self.son[i].W / self.son[i].N + C_puct * self.son[i].P * math.sqrt(N) / (1.0 + self.son[i].N), i])
		if self.d % 2:
			li.sort(key = lambda x:x[0], reverse = True)
		else:
			li.sort(key = lambda x:x[0])
		return li[0][1]


			


class SearchTree():
	def __init__(self, li):
		self.root = Node(li, 1)		# note : the deep of root is 1, but not 0
		self.root.Unfold()

	def Get_Nex(self, T):
		las = 0
		for i in range(T):
			now = int(100 * i / T)
			if now > las:
				las = now
				sys.stdout.write('[')
				for j in range(now):
					sys.stdout.write('#')
				for j in range(100 - now):
					sys.stdout.write('.')
				sys.stdout.write(']' + str(now) + '%\r')
				sys.stdout.flush()
			self.Searching(self.root)
		print ''
		li = []
		for i in range(len(self.root.son)):
			Wp = self.root.son[i].W
			Np = self.root.son[i].N
			li.append([(Np + Wp) / (2.0 * Np), i])
		li.sort(key = lambda x:x[0], reverse = True)
		return  self.root.son[li[0][1]].li

	def Searching(self, now):
		now.N += 1.0
		if len(now.son) == 0:
			var = JudgeMap(now.li)
			Res = var.GetValue()
			#print 'Res = ', Res
			now.W += Res
			if now.N >= N_thr:
				now.Unfold()
			return Res
		nex = now.son[now.ChoseChild()]
		Res = self.Searching(nex)
		now.W += Res
		return Res

	def PrintTree(self, now):
		fout = open('debug.txt', 'w')
		fout.writelines('--------------deep : ' + str(now.d) + '\n')
		for i in now.li:
			fout.writelines(str(i) + '\n')
		fout.writelines('parameter- N: ' + str(now.N) + ' W: ' + str(now.W) + '\n\n')

		for i in range(len(now.son)):
			fout.writelines('----------id : ' + str(i) + '\n')
			for j in now.son[i].li:
				fout.writelines(str(j) + '\n')
			fout.writelines('parameter- N: ' + str(now.son[i].N) + ' W: ' + str(now.son[i].W) + '\n')
			fout.writelines('Num of sons : ' + str(len(now.son[i].son)) + '\n')
		fout.close()

'''
def main():
	li = [
	list('...$.'),
	list('..A..'),
	list('D$...'),
	list('....$'),
	list('$....')
	]
	cal = SearchTree(li)
	for i in cal.Get_Nex(500):
		print i
	cal.PrintTree(cal.root)


if __name__ == '__main__':
	main()
'''
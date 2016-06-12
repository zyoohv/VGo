from setting import L, N_thr, C_puct, P
import subprocess
import copy
import math


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
		self.son = []	# struct : [ 'son', id ]
		self.sig = {}	# the local of defend

		self.cnt = 0	# the number of defends
		for i in range(len(li)):
			for j in range(len(li[0])):
				if li[i][j] == 'D':
					self.sig[self.cnt] = [j, i]
					self.cnt += 1
		'''
		O---------j------------>xSiz
		|
		|
		|
		|
		i
		|
		|
		|
		|
		v
		ySiz
		'''

	def Unfold(self):		# unfold the node
		if self.d >= L:
			return
		dx = [0, 0, 0, 1, -1]
		dy = [0, 1, -1, 0, 0]
		for i in range(5 ** self.cnt):
			div = i
			nexl = copy.deepcopy(self.li)
			move_success = 0
			for j in range(self.cnt):
				nexx = self.sig[j][0] + dx[div % 5]
				nexy = self.sig[j][1] + dy[div % 5]
				div /= 5
				if nexx >= 0 and nexx < self.xSiz and nexy >= 0 and nexy < self.ySiz and nexl[nexy][nexx] !='x' and nexl[nexy][nexx] != '$' and nexl[nexy][nexx] != 'D':
					move_success += 1
					if nexl[nexy][nexx] == '.':
						nexl[nexy][nexx] = 'D'
						nexl[self.sig[j][1]][self.sig[j][0]] = '.'
					elif nexl[nexy][nexx] == 'A':
						nexl[nexy][nexx] = '.'
						nexl[self.sig[j][1]][self.sig[j][0]] = '.'
				elif nexx == self.sig[j][0] and nexy == self.sig[j][1]:
					move_success += 1
			if move_success == self.cnt:
				self.son.append([Node(nexl, self.d + 1), i])



	def ChoseChild(self):	# chose the best child according formula : a = { Q + u }
		N = 0.0
		for son in self.son:
			N += son[0].N
		li = []
		for i in range(len(self.son)):
			li.append([self.son[i][0].W / self.son[i][0].N + C_puct * self.son[i][0].P * math.sqrt(N) / (1.0 + self.son[i][0].N), i])
		li.sort(key = lambda x:x[0], reverse = True)
		#print li[0][1]
		return li[0][1]


			


class SearchTree():
	def __init__(self, li):
		self.root = Node(li, 1)
		self.root.Unfold()

	def Get_Nex(self, T):
		for i in range(T):
			self.Searching(self.root)
		li = []
		for i in range(len(self.root.son)):
			li.append([(self.root.son[i][0].W + 0.7) / self.root.son[i][0].N, i])
		li.sort(key = lambda x:x[0], reverse = True)
		return  self.root.son[li[0][1]][0].li

	def Searching(self, now):
		now.N += 1.0
		if len(now.son) == 0:
			parameter = 'bin\Judge.exe'
			for i in range(now.ySiz):
				parameter += ' '
				for j in range(now.xSiz):
					parameter += now.li[i][j]
			p = subprocess.Popen(str(parameter), shell = True)
			Res = p.wait()
			#print 'Res = ', Res
			now.W += Res
			if now.N >= N_thr:
				now.Unfold()
			return Res
		nex = now.son[now.ChoseChild()][0]
		now.W += self.Searching(nex)

	def PrintTree(self, now):
		fout = open('print.txt', 'w')
		fout.writelines('--------------deep : ' + str(now.d) + '\n')
		for i in range(now.cnt):
			fout.writelines(str(now.sig[i][0]) + ' ' + str(now.sig[i][1]) + '\n')
		fout.writelines('\n')
		for i in now.li:
			fout.writelines(str(i) + '\n')
		fout.writelines('parameter- N: ' + str(now.N) + ' W: ' + str(now.W) + '\n\n')
		for i in now.son:
			fout.writelines('----------id : ' + str(i[1]) + '\n')
			for j in i[0].li:
				fout.writelines(str(j) + '\n')
			fout.writelines('parameter- N: ' + str(i[0].N) + ' W: ' + str(i[0].W) + '\n')
		fout.close()

'''
def main():
	li = [
	list('...$.'),
	list('A.A.A'),
	list('D$...'),
	list('...D$'),
	list('$.D..')
	]
	cal = SearchTree(li)
	#cal.PrintTree(cal.root)
	for i in cal.Get_Nex(1000):
		print i


if __name__ == '__main__':
	main()
'''
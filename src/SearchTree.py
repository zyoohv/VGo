from setting import L, N_thr, C_puct, P
import subprocess
import copy


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

		cnt = 0
		for i in range(len(li)):
			for j in range(len(li[0])):
				if li[i][j] == 'D':
					self.sig[cnt] = [j, i]
					cnt += 1

	def Unfold(self):		# unfold the node
		if self.d >= L:
			return
		dx = [0, 0, 0, 1, -1]
		dy = [0, 1, -1, 0, 0]
		son_id = 0
		for i in range(125):
			div = i
			nexl = copy.deepcopy(self.li)
			move_success = 1
			for j in range(3):
				nexx = self.sig[j][0] + dx[div % 5]
				nexy = self.sig[j][1] + dy[div % 5]
				div /= 5
				if nexx >= 0 and nexx < self.xSiz and nexy >= 0 and nexy < self.ySiz and self.li[nexy][nexx] !='x' and self.li[nexy][nexx] != '$':
					move_success += 1
					if nexl[nexy][nexx] == '.':
						nexl[nexy][nexx] = 'D'
						nexl[self.sig[j][1]][self.sig[j][0]] = '.'
					elif nexl[nexy][nexx] == 'A':
						nexl[nexy][nexx] = '.'
						nexl[self.sig[j][1]][self.sig[j][0]] = '.'
			if move_success == 3:
				self.son.append([Node(nexl, self.d + 1), son_id])
				son_id += 1



	def ChoseChild(self):	# chose the best child according formula : a = { Q + u }
		N = 0.0
		for son in self.son:
			N += son[0].N
		li = []
		for i in range(len(self.son)):
			li.append([self.son[i][0].W / self.son[i][0].N + C_puct * self.son[i][0].P * N / (1.0 + self.son[i][0].N), i])
		li.sort(key = lambda x:x[0], reverse = True)
		return li[0][1]


			


class SearchTree():
	def __init__(self, li):
		self.root = Node(li, 1)
		self.root.Unfold()

	def Get_Nex(self, T):
		for i in range(T):
			self.Searching(self.root)
		return  self.root.son[self.root.ChoseChild()][0].li

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
		nex = now.son[now.ChoseChild()]
		now.W += self.Searching(nex[0])

	def PrintTree(self, now):
		print '--------------deep : ',now.d
		for i in now.li:
			print i
		print 'parameter- N:', now.N, 'W', now.W
		for i in now.son:
			self.PrintTree(i[0])

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
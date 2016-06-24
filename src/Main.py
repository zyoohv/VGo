import sys
import time
import pygame
from pygame.locals import *
from setting import Mps, xSiz, ySiz
from SearchTree import SearchTree, Node

dic1 = {	# normal display
'.' : 'pic/none.png',
'x' : 'pic/ban.png',
'$' : 'pic/sor.png',
'A' : 'pic/enmy.png',
'D' : 'pic/defend.png',
'@' : 'pic/dsor.png'
}

dic2 = {	# get red display
'.' : 'pic/attack.png',
'$' : 'pic/ar_sor.png',
'A' : 'pic/red_enmy.png',
'D' : 'pic/red_defend.png',
'@' : 'pic/red_dsor.png'
}

dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]

locked = {}

def cor(x, y):
	return x * 50, y * 50

def main():
	flag = 0
	lasx = 0
	lasy = 0
	NumofEnmy = 3
	NumofTurn = 1
	pygame.init()
	global Mps
	for i in range(len(Mps)):
		Mps[i] = list(Mps[i])

	screen = pygame.display.set_mode((xSiz * 50, ySiz * 50), 0, 32)

	for i in range(len(Mps)):
		for j in range(len(Mps[0])):
			block = pygame.image.load(dic1[Mps[i][j]]).convert()
			screen.blit(block, cor(j, i))

	pygame.display.update()

	while True:
		for event in pygame.event.get():
			if event == QUIT:
				exit()
			elif event.type == MOUSEBUTTONDOWN:
				localtion_keys = list(event.pos)
				localtion_keys[0] = localtion_keys[0] / 50 * 50
				localtion_keys[1] = localtion_keys[1] / 50 * 50
				if flag == 0:	# chose one to move
					if Mps[localtion_keys[1] / 50][localtion_keys[0] / 50] == 'A' and (localtion_keys[0] / 50, localtion_keys[1] / 50) not in locked:
						# making the enmy and enmy's rounding get red
						block = pygame.image.load('pic/red_enmy.png').convert()
						screen.blit(block, localtion_keys)
						for i in range(4):
							nexx = localtion_keys[0] / 50 + dx[i]
							nexy = localtion_keys[1] / 50 + dy[i]
							if nexx >= 0 and nexx < xSiz and nexy >= 0 and nexy < ySiz and Mps[nexy][nexx] != 'x':
								block = pygame.image.load(dic2[Mps[nexy][nexx]]).convert()
								screen.blit(block, [nexx * 50, nexy * 50])
						flag = 1
						lasx = localtion_keys[0] / 50
						lasy = localtion_keys[1] / 50
				elif flag == 1:	# chose the coordinate to move
					for i in range(4):	# back to normal arrounding the enmy
						nexx = lasx + dx[i]
						nexy = lasy + dy[i]
						if nexx >= 0 and nexx < xSiz and nexy >= 0 and nexy < ySiz:
							block = pygame.image.load(dic1[Mps[nexy][nexx]]).convert()
							screen.blit(block, [nexx * 50, nexy * 50])	
					if localtion_keys[0] / 50 == lasx and localtion_keys[1] / 50 == lasy:	# don't move
						block = pygame.image.load('pic/enmy.png').convert()
						screen.blit(block, localtion_keys)
						locked[(localtion_keys[0] / 50, localtion_keys[1] / 50)] = 1	# lock it until next turn
						flag = 0
						continue
					move_success = 0
					if Mps[localtion_keys[1] / 50][localtion_keys[0] / 50] != 'x' and Mps[localtion_keys[1] / 50][localtion_keys[0] / 50] != 'A':
						# move to a new coordinate and check if can move
						for i in range(4):
							nexx = localtion_keys[0] / 50 + dx[i]
							nexy = localtion_keys[1] / 50 + dy[i]
							if nexx == lasx and nexy == lasy:
								if Mps[localtion_keys[1] / 50][localtion_keys[0] / 50] == '.':	# normal move
									#print nexx, nexy, localtion_keys
									block = pygame.image.load('pic/none.png')	#'A' -> '.'
									screen.blit(block, [lasx * 50, lasy * 50])
									Mps[lasy][lasx] = '.'
									block = pygame.image.load('pic/enmy.png')	#'.' -> 'A'
									screen.blit(block, localtion_keys)
									Mps[localtion_keys[1] / 50][localtion_keys[0] / 50] = 'A'
									locked[(localtion_keys[0] / 50, localtion_keys[1] / 50)] = 1
								elif Mps[localtion_keys[1] / 50][localtion_keys[0] / 50] == '$':	# destory a source
									block = pygame.image.load('pic/none.png')
									screen.blit(block, [lasx * 50, lasy * 50])
									Mps[lasy][lasx] = '.'
									block = pygame.image.load('pic/enmy.png')
									screen.blit(block, localtion_keys)
									Mps[localtion_keys[1] / 50][localtion_keys[0] / 50] = 'A'
									locked[(localtion_keys[0] / 50, localtion_keys[1] / 50)] = 1
								elif Mps[localtion_keys[1] / 50][localtion_keys[0] / 50] == 'D':	# attack
									block = pygame.image.load('pic/none.png')
									screen.blit(block, [lasx * 50, lasy * 50])
									Mps[lasy][lasx] = '.'
									block = pygame.image.load('pic/none.png')
									screen.blit(block, localtion_keys)
									Mps[localtion_keys[1] / 50][localtion_keys[0] / 50] = '.'
									NumofEnmy -= 1
								elif Mps[localtion_keys[1] / 50][localtion_keys[0] / 50] == '@':	# attack enmy in source
									block = pygame.image.load('pic/none.png')
									screen.blit(block, [lasx * 50, lasy * 50])
									Mps[lasy][lasx] = '.'
									block = pygame.image.load('pic/sor.png')
									screen.blit(block, localtion_keys)
									Mps[localtion_keys[1] / 50][localtion_keys[0] / 50] = '$'
									NumofEnmy -= 1
								move_success = 1
					if move_success == 0:	# return the begining states if unsuccessful move
						block = pygame.image.load('pic/enmy.png')
						screen.blit(block, [lasx * 50, lasy * 50])
					flag = 0	# chose next enmy to move
		pygame.display.update()
		if len(locked) == NumofEnmy:	# finished move
			if NumofEnmy == 0:
				print 'Game over !'
				break
			print 'computer turn(' + str(NumofTurn) + ')...',
			NumofTurn += 1
			locked.clear()

			#	using mcts searching way
			var = SearchTree(Mps)
			Mps = var.Get_Nex(500)

			#	debug output
			var.PrintTree(var.root)


			# recheck the number of enmys and redraw the map
			NumofEnmy = 0
			for i in range(len(Mps)):
				for j in range(len(Mps[0])):
					block = pygame.image.load(dic1[Mps[i][j]]).convert()
					screen.blit(block, cor(j, i))
					if Mps[i][j] == 'A':
						NumofEnmy += 1
			Wp = var.root.W
			Np = var.root.N
			print 'rate of wining: ',(Np + Wp) / (2.0 * Np) * 100.0, '%'
			print 'your turn...'

		pygame.display.update()
					

if __name__ == '__main__':
	main()
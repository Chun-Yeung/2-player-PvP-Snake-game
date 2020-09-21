import math
import random
import pygame
import Tkinter as tk
import tkMessageBox
import player

def drawGrid(w, rows, surface):
	sizeBtw = w // rows
	x = 0
	y = 0
	for i in range(rows):
		x = x + sizeBtw
		y = y + sizeBtw

		pygame.draw.line(surface, (0, 0, 0), (x,0), (x, w))
		pygame.draw.line(surface, (0, 0, 0), (0,y), (w, y))


def redrawWin(surface):
	global rows, width, s1, s2, food
	surface.fill((0, 0, 0))
	s1.draw(surface)
	s2.draw(surface)
	food.draw(surface)
	drawGrid(width, rows, surface)
	pygame.display.update()


def randomFood(rows, item):
	
	positions = item.body

	while True:
		x = random.randrange(rows)
		y = random.randrange(rows)
		if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0:
			continue
		else:
			break

	return (x, y)


def message_box(subject, content):
	root = tk.Tk()
	root.attributes("-topmost", True)
	root.withdraw()
	tkMessageBox.showinfo(subject, content)
	try:
		root.destroy()
	except:
		pass


def main():
	global width, rows, s1, s2, food
	width = 500
	height = 500
	rows = 20
	win = pygame.display.set_mode((width, height))
	s1 = player.snake(color = (0, 255, 0), pos = (5, 10), dirnx = 1, dirny = 0, player = 1)

	s2 = player.snake(color = (255, 255, 0), pos = (15, 10), dirnx = 1, dirny = 0, player = 2)

	food = player.cube(randomFood(rows, s1), 1, 0, color = (255, 255, 255))
	flag = True


	clock = pygame.time.Clock()


	while flag:
		pygame.time.delay(50)
		clock.tick(10)
		s1.move()
		s2.move()

		if s1.body[0].pos == food.pos:
			s1.addCube()
			food = player.cube(randomFood(rows, s1), 1, 0, color = (255, 255, 255))

		for x in range(len(s1.body)):
			if s1.body[x].pos in list(map(lambda z:z.pos, s1.body[x+1:])) or s1.body[x].pos in list(map(lambda z:z.pos, s2.body[x+1:])):
				#result = "Score: " + str(len(s.body))
				message_box('Player1 Lost!!!', "Player1 Lost!!!")
				s1.reset((5, 10), 1, 0)
				s2.reset((15, 10), -1, 0)
				break

		if s2.body[0].pos == food.pos:
			s2.addCube()
			food = player.cube(randomFood(rows, s2), 1, 0, color = (255, 255, 255))

		for x in range(len(s2.body)):
			if s2.body[x].pos in list(map(lambda z:z.pos, s2.body[x+1:])) or s2.body[x].pos in list(map(lambda z:z.pos, s1.body[x+1:])):
				#result = "Score: " + str(len(s.body))
				message_box('Player2 Lost!!!', "Player2 Lost!!!")
				s1.reset((5, 10), 1, 0)
				s2.reset((15, 10), -1, 0)
				break

		redrawWin(win)

	pass

main()

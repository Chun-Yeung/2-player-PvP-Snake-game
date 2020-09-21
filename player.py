import math
import pygame

class cube(object):
	rows = 20
	w = 500

	def __init__(self, start, dirnx, dirny, color):
		self.pos = start
		self.dirnx = 0
		self.dirny = 0
		self.color = color

	def move(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

	def draw(self, surface, eyes = False):
		dis = self.w // self.rows
		i = self.pos[0]
		j = self.pos[1]

		pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))

		if eyes:
			centre = dis//2
			radius = 3
			circleMiddle = (i*dis + centre - radius, j*dis + 8)
			circleMiddle2 = (i*dis + dis - radius*2, j*dis + 8)
			pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
			pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

class snake(object):

	body = []
	turns = {}
	def __init__(self, color, pos, dirnx, dirny, player):
		self.head = cube(pos, dirnx, dirny, color)
		self.body.append(self.head)
		self.color = color
		self.dirnx = dirnx
		self.dirny = dirny
		self.player = player


	def setColor(self, color):
		self.color = color


	def move(self):

		move_translate = {
    		pygame.K_a: (-1, 0),
    		pygame.K_d: (1, 0),
    		pygame.K_w: (0, -1),
    		pygame.K_s: (0, 1),
		}

		move_translate2 = {
    		pygame.K_LEFT: (-1, 0),
    		pygame.K_RIGHT: (1, 0),
    		pygame.K_UP: (0, -1),
    		pygame.K_DOWN: (0, 1)
		}

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)

			if event.type == pygame.KEYDOWN:
				if self.player == 1:
					if event.key in move_translate:
						self.dirnx, self.dirny = move_translate[event.key]
						self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
				else:
					if event.key in move_translate2:
						self.dirnx, self.dirny = move_translate2[event.key]
						self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]


		for i,c in enumerate(self.body):
			p = c.pos[:]
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0], turn[1])
				if i == len(self.body)-1:
					self.turns.pop(p)
			else:
				##wormhole wall
				if c.dirnx == -1 and c.pos[0] <= 0:
					c.pos = (c.rows-1, c.pos[1])
				elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
					c.pos = (0, c.pos[1])
				elif c.dirny == 1 and c.pos[1] >= c.rows-1:
					c.pos = (c.pos[0], 0)
				elif c.dirny == -1 and c.pos[1] <= 0:
					c.pos = (c.pos[0], c.rows-1)
				else:
					c.move(c.dirnx, c.dirny)

	def reset(self, pos, dirnx, dirny):
		self.head = cube(pos, dirnx, dirny, color = self.color)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dirnx = dirnx
		self.dirny = dirny



	def addCube(self):
		tail = self.body[-1]
		dx, dy = tail.dirnx, tail.dirny

		if dx == 1 and dy == 0:
			self.body.append(cube((tail.pos[0]-1, tail.pos[1]), dx, dy, self.color))
		elif dx == -1 and dy == 0:
			self.body.append(cube((tail.pos[0]+1, tail.pos[1]), dx, dy, self.color))
		elif dx == 0 and dy == 1:
			self.body.append(cube((tail.pos[0], tail.pos[1]-1), dx, dy, self.color))
		elif dx == 0 and dy == -1:
			self.body.append(cube((tail.pos[0], tail.pos[1]+1), dx, dy, self.color))

		self.body[-1].dirnx = dx
		self.body[-1].dirny = dy

	def draw(self, surface):
		for i, c in enumerate(self.body):
			if i ==0:
				c.draw(surface, True)
			else:
				c.draw(surface)


"""class snake2(snake):

	body = []
	turns = {}

	'''def __init__(self, color, pos):
					snake.__init__(self, color, pos)
					self.color = color
					self.head = cube(pos, dirnx = -1, dirny = 0, color = (255, 255, 0))
					self.dirnx = -1
					self.dirny = 0'''


	def __init__(self, color, pos):
				self.color = color
				self.head = cube(pos, dirnx = -1, dirny = 0, color = (255, 255, 0))
				self.body.append(self.head)
				self.dirnx = -1
				self.dirny = 0

	def move(self):

		move_translate = {
    		pygame.K_LEFT: (-1, 0),
    		pygame.K_RIGHT: (1, 0),
    		pygame.K_UP: (0, -1),
    		pygame.K_DOWN: (0, 1)
		}

		for event in pygame.event.get():
			
			if event.type == pygame.KEYDOWN:
				self.dirnx, self.dirny == move_translate[event.key]
				self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

			'''keys = pygame.key.get_pressed()
									
												for key in keys:
													if keys[pygame.K_LEFT]:
														self.dirnx = -1
														self.dirny = 0
														self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
									
													elif keys[pygame.K_RIGHT]:
														self.dirnx = 1
														self.dirny = 0
														self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
									
													elif keys[pygame.K_UP]:
														self.dirnx = 0
														self.dirny = -1
														self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
									
													elif keys[pygame.K_DOWN]:
														self.dirnx = 0
														self.dirny = 1
														self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]'''

		for i,c in enumerate(self.body):
			p = c.pos[:]
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0], turn[1])
				if i == len(self.body)-1:
					self.turns.pop(p)
			else:
				##wormhole wall
				if c.dirnx == -1 and c.pos[0] <= 0:
					c.pos = (c.rows-1, c.pos[1])
				elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
					c.pos = (0, c.pos[1])
				elif c.dirny == 1 and c.pos[1] >= c.rows-1:
					c.pos = (c.pos[0], 0)
				elif c.dirny == -1 and c.pos[1] <= 0:
					c.pos = (c.pos[0], c.rows-1)
				else:
					c.move(c.dirnx, c.dirny)

	def reset(self, pos):
		self.head = cube(pos, dirnx = -1, dirny = 0, color = (255, 255, 0))
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dirnx = -1
		self.dirny = 0
"""
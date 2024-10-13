import pygame
import numpy as np
from itertools import pairwise
from lib import utils as utl
from lib import rmath
from lib import color
from lib import shape


def interpolate(A, B, t):
	return (1 - t) * A + t * B

def eta(distance):
	if distance < 0.0001:
		return 9999
	else:
		return 1 / distance


class Ant:
	texture = None
	
	def __init__(self, total_cities):
		if Ant.texture is None:
			Ant.texture = utl.image('./assets/image/green-ant.png', (18, 22))

		self.current_city = 0
		self.visited = []
		self.all_cities = set(range(total_cities))
		self.completed_tour = False

		self.apha = 0.8
		self.beta = 4

		self.position = (0, 0)
		self.velocity = 1
		self.deltaV = 0.05
		self.state = 0 # 0 = rest state, 1 = reached
		self.move = False
		self.angle = 0

		self.paths = []
		if total_cities > 50:
			self.alpha_for_path = 5
		elif total_cities > 30:
			self.alpha_for_path = 10
		else:
			self.alpha_for_path = 20



		

	def find_next_city(self, dist_mat, ferrom_mat):
		available = list(self.all_cities - set(self.visited))

		# print('availables - ')
		# print(available)

		if len(available) == 0:
			if self.visited[0] == self.visited[-1]:
				# self.completed_tour = True
				return
			return self.visited[0]

		if len(available) == 1:
			return available.pop()

		weights = np.empty_like(available, dtype=np.float64)

		for i, nxt in enumerate(available):
			weights[i] = (ferrom_mat[self.current_city, nxt] ** self.apha) * \
						 (eta(dist_mat[self.current_city, nxt]) ** self.beta)

		weights /= weights.sum()

		

		next_city = np.random.choice(available, p=weights)
		return int(next_city)



	def go(self, positoin_array, nxt):
		if nxt != self.current_city:
			self.move = True
			self.angle = rmath.heading(positoin_array[nxt]-self.position)
			self.deltaV = self.velocity/np.linalg.norm(positoin_array[nxt]-positoin_array[self.current_city])
		
		if not self.move:
			return

		self.position = interpolate(positoin_array[self.current_city], positoin_array[nxt], self.state)
		self.state += self.deltaV

		self.paths.append(self.position)

		if self.state > 1:
			self.visited.append(nxt)
			self.state = 0
			self.move = False
			self.current_city = nxt




	def drawPath(self, screen):


		for i in range(len(self.paths)-1):
			# pygame.draw.aaline(screen(), color.WHITE, self.paths[i], self.paths[i+1])
			shape.aaline(screen(), (255, 255, 255, self.alpha_for_path), self.paths[i], self.paths[i+1], 1)




	def show(self, screen):
		screen.render(Ant.texture, self.angle, *self.position, 'c')









class AntPopulation:
	def __init__(self, total_ant, total_cities):
		self.ants = []
		self.total_cities = total_cities
		self.total_ants = total_ant
		self.go_to = []

		self.velocity = 20
		self.evaporation = 0.7
		self.alpha = 0.8
		self.beta = 2

	def __iter__(self):
		return iter(self.ants)

	def set_velocity(self, value):
		for ant_unit in self.ants:
			self.velocity = value
			ant_unit.velocity = value

	def randomize(self, positoin_array):
		self.ants = []
		self.go_to = []

		for i in range(self.total_ants):
			a = Ant(self.total_cities)
			start_city = int(np.random.randint(0, self.total_cities))
			a.position = positoin_array[start_city].astype(np.float64)
			a.current_city = start_city
			a.visited = [start_city]
			a.velocity = self.velocity


			self.ants.append(a)
			self.go_to.append(start_city)

	def build_visited_matrix(self):
		visited_matrix = np.zeros((self.total_cities, self.total_cities))
		# print('visited list')
		for ant_unit in self:
			# print(ant_unit.visited)
			for a, b in pairwise(ant_unit.visited):
				visited_matrix[a, b] += 1
				visited_matrix[b, a] += 1

		return visited_matrix

	def update_pheromone(self, dist_mat, pheromone_matrix):
		visited_matrix = self.build_visited_matrix()

		for i in range(self.total_cities):
			for j in range(self.total_cities):
				total_pheromone = visited_matrix[i, j] * eta(dist_mat[i, j])
				total_pheromone += (1 - self.evaporation) * pheromone_matrix[i, j]

				pheromone_matrix[i, j] = total_pheromone

























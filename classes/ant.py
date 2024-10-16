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
	if distance < 0.00001:
		return 99999
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
		self.distance_visited = 0

		self.apha = 0.8
		self.beta = 4
		self.r0 = 0.2

		self.position = (0, 0)
		self.velocity = 1
		self.deltaV = 0.05
		self.state = 0 # 0 = rest state, 1 = reached
		self.move = False
		self.angle = 0

		if total_cities > 50:
			self.alpha_for_path = 5
		elif total_cities > 30:
			self.alpha_for_path = 10
		else:
			self.alpha_for_path = 20


	def last_city(self):
		return self.visited[-1]


		

	def find_next_city(self, dist_mat, ferrom_mat, exploitation=False):
		available = list(self.all_cities - set(self.visited))

		# print('availables - ')
		# print(available)

		if len(available) == 0:
			if self.visited[0] == self.visited[-1]:
				# self.completed_tour = True
				return
			return self.visited[0]

		if len(available) == 1:
			return available[0]

		weights = np.empty_like(available, dtype=np.float64)

		for i, nxt in enumerate(available):
			weights[i] = (ferrom_mat[self.current_city, nxt] ** self.apha) * \
						 (eta(dist_mat[self.current_city, nxt]) ** self.beta)



		if exploitation and np.random.rand() < self.r0:
			idx = np.argmax(weights)
			return available[idx]


		weights /= weights.sum()
		
		try:
			next_city = np.random.choice(available, p=weights)
		except ValueError:
			weights = np.ones(weights.size) / weights.size
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


		if self.state > 1:
			self.visited.append(nxt)
			self.state = 0
			self.move = False
			self.current_city = nxt


	def drawPath(self, screen, cities):

		for a, b in pairwise(self.visited):
			shape.aaline(screen(), (255, 255, 255, self.alpha_for_path), cities[a], cities[b], 1)
		shape.aaline(screen(), (255, 255, 255, self.alpha_for_path), cities[self.visited[-1]], self.position, 1)



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
		self.elitism_factor = 1
		self.global_factor = 0.6
		self.initial_pheromone = 0.2

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

		for ant_unit in self:

			for a, b in pairwise(ant_unit.visited):
				visited_matrix[a, b] += 1
				visited_matrix[b, a] += 1

		return visited_matrix


	def update_pheromone(self, dist_mat, pheromone_matrix, top_ants_list, min_distance):
		visited_matrix = np.zeros((self.total_cities, self.total_cities))
		elit_ants = len(top_ants_list)
		elit_path_matrix = np.zeros((self.total_cities, self.total_cities), dtype=np.bool_)

		top_ants_list = sorted(top_ants_list)


		if elit_ants > 1:
			for i in top_ants_list:
				print(self.ants[i].visited)
			print()

		j = 0
		for i, ant_unit in enumerate(self):
			for a, b in pairwise(ant_unit.visited):
				visited_matrix[a, b] += 1
				visited_matrix[b, a] += 1

				if j < elit_ants and i == j:
					elit_path_matrix[a, b] = 1
					elit_path_matrix[b, a] = 1
			
			if i == j:
				j += 1

		min_distance **= 1/2
		for i in range(self.total_cities):
			for j in range(self.total_cities):
				# Evaporate pheromone
				pheromone_matrix[i, j] *= (1 - self.evaporation)

				# Add new pheromone based on path frequency
				pheromone_matrix[i, j] += visited_matrix[i, j] * eta(dist_mat[i, j])

				# Elitism
				pheromone_matrix[i, j] += self.elitism_factor * elit_ants * elit_path_matrix[i, j] / min_distance


	def update_pheromone2(self, dist_mat, pheromone_matrix, global_best_path, min_distance):
		visited_matrix = np.zeros((self.total_cities, self.total_cities))
		best_path_matrix = np.zeros((self.total_cities, self.total_cities), dtype=np.bool_)


		for a, b in pairwise(global_best_path):
			best_path_matrix[a, b] = 1
			best_path_matrix[b, a] = 1

		for ant_unit in self.ants:
			for a, b in pairwise(ant_unit.visited):
				visited_matrix[a, b] += 1
				visited_matrix[b, a] += 1

		# min_distance **= (1/2)

		for i in range(self.total_cities):
			for j in range(self.total_cities):
				# Evaporate pheromone on all edges
				pheromone_matrix[i, j] *= (1 - self.evaporation)

				# Add pheromone based on how many times the edge was visited
				# pheromone_matrix[i, j] += visited_matrix[i, j] * eta(dist_mat[i, j])

				# Elitism update: Apply extra pheromone on the global best path
				pheromone_matrix[i, j] += self.elitism_factor * best_path_matrix[i, j] * eta(min_distance) #* visited_matrix[i, j]


	def update_pheromone3(self, pheromone_matrix, global_best_path, min_distance):
		delta_pheromone = np.zeros(pheromone_matrix.shape)


		for a, b in pairwise(global_best_path):
			delta_pheromone[a, b] = self.elitism_factor * eta(min_distance)
			delta_pheromone[b, a] = self.elitism_factor * eta(min_distance)

		for ant_unit in self.ants:
			for a, b in pairwise(ant_unit.visited):
				delta_pheromone[a, b] += eta(ant_unit.distance_visited)
				delta_pheromone[b, a] += eta(ant_unit.distance_visited)

		pheromone_matrix *= (1 - self.evaporation)
		pheromone_matrix += delta_pheromone

	def update_pheromone3(self, pheromone_matrix, global_best_path, min_distance):
		delta_pheromone = np.zeros(pheromone_matrix.shape)

		# for global best path
		for a, b in pairwise(global_best_path):
			delta_pheromone[a, b] = self.elitism_factor * eta(min_distance)
			delta_pheromone[b, a] = self.elitism_factor * eta(min_distance)

		for ant_unit in self.ants:
			for a, b in pairwise(ant_unit.visited):
				delta_pheromone[a, b] += eta(ant_unit.distance_visited)
				delta_pheromone[b, a] += eta(ant_unit.distance_visited)


		pheromone_matrix *= (1 - self.evaporation)
		pheromone_matrix += delta_pheromone




	def update_pheromone_global(self, pheromone_matrix, top_ants_list, min_distance):
		delta_pheromone = np.zeros(pheromone_matrix.shape)

		for i in top_ants_list:
			for a, b in pairwise(self.ants[i].visited):
				delta_pheromone[a, b] += eta(min_distance)
				delta_pheromone[b, a] += eta(min_distance)

		min_distance **= 1/2

		pheromone_matrix *= (1 - self.global_factor)
		pheromone_matrix += self.global_factor * delta_pheromone


	def update_pheromone_local(self, pheromone_matrix, a, b):
		pheromone_matrix[a, b] *= (1 - self.evaporation)
		pheromone_matrix[a, b] += self.evaporation * self.initial_pheromone



def draw_heatmap(screen, matrix, vmin=None, vmax=None, color_map=None):
    """
    Draws a heatmap on the given surface based on the provided matrix.

    Parameters:
    - surface: The Pygame surface to draw on.
    - matrix: 2D NumPy array representing the data for the heatmap.
    - cell_size: Size of each cell in pixels.
    - color_map: Function to map normalized values to colors. If None, uses a default blue-red gradient.
    """
    # Normalize the matrix to the range 0-255

    screen.background((255, 255, 255))

    cell_size = screen.w / matrix.shape[0]

    if vmin is None:
    	vmin = matrix.min()

    if vmax is None:
    	vmax = matrix.max()

    norm_matrix = (matrix - vmin) / (vmax - vmin)

    # Default color mapping function if none provided
    if color_map is None:
    	color_map = lambda value: utl.lerp_color(value, color.LIGHT_PINK, color.BLUE)

    # Draw the heatmap
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            color_value = norm_matrix[i, j]
            color_rgb = color_map(color_value)
            pygame.draw.rect(screen.surface, color_rgb, (j * cell_size, i * cell_size, cell_size, cell_size))
            # pygame.draw.rect(screen.surface, (0, 0, 0), (j * cell_size, i * cell_size, cell_size, cell_size), 2)

















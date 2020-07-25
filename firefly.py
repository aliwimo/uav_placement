import math
import random
import numpy as np
from decimal import Decimal
from config_file import POP_SIZE, DIM_SIZE, ALPHA, BETA0, GAMMA, UB, LB, BUILDING, Users_Locations

class Firefly:
    def __init__(self, location):
        self.location = location.copy()
        self.fitness = self.update_fitness()

    def update_fitness(self):
        total_sum = 0
        for index in range(Users_Locations.shape[0]):
            total_sum += self.calc_fitness(Users_Locations[index])
        return total_sum
    
    def calc_fitness(self, user):
        dotProduct = 1
        up = 0
        dp = 0
        d2D = math.sqrt(self.location[0]**2)
        d3D = 0

        for i in range(DIM_SIZE):
            d3D += (user[i] - self.location[i])**2
            dotProduct += user[i] * self.location[i]
            up += user[i]**2
            dp += self.location[i]**2
        
        d3D = math.sqrt(d3D)
        mag_mul = math.sqrt(up) * math.sqrt(dp)

        result = (20.0 * math.log10(d3D) + 20.0 * ( 0.301 ) + 32.4) + (14.0 + 15.0 * math.pow(1.0 - dotProduct/mag_mul, 2.0) ) + (0.5 * d2D)
        return result

    def calc_distance(self, other):
        dist = 0
        for index in range(DIM_SIZE):
            dist += (self.location[index] - other.location[index])**2
        return math.sqrt(dist)
    
    def light_intensity(self, distance):
        return self.fitness * math.exp(-GAMMA * (distance ** 1))

    def attractiveness(self, distance):
        return BETA0 * math.exp(-GAMMA * (distance ** 2))

    def update_location(self, other, distance):
        for index in range(DIM_SIZE):
            epsilon = random.random() - 0.5
            # alpha = ALPHA - (random.uniform(-ALPHA, ALPHA))
            alpha = ALPHA
            rand = alpha * epsilon
            self.location[index] += self.attractiveness(distance) * (other.location[index] - self.location[index]) + rand

    def move_randomly(self):
        for index in range(DIM_SIZE):
            epsilon = random.random() - 0.5
            alpha = ALPHA - (random.uniform(0, ALPHA))
            rand = alpha * epsilon
            self.location[index] += rand

    def check_bounds(self):
        for index in range(DIM_SIZE):
            if self.location[index] > UB:
                self.location[index] = UB
            if self.location[index] < LB:
                self.location[index] = LB

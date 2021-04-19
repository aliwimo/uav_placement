import numpy as np
from random import choice, random
import time

# start timer
start_time = time.time()

# set initial parameters' values
population_size = 50
dimension_size = 3
donors_number = 1
receivers_number = 1
maximum_evaluations = 2500
bound = 200

# other dependent parameters, no need to change
current_evaluation = population_size
x_upper_bound = bound
x_lower_bound = -bound
y_upper_bound = bound
y_lower_bound = -bound
z_upper_bound = bound
z_lower_bound = 0

BUILDING = [20, 50, 200]     #b1
# BUILDING = [20, 50, 250]     #b2
# BUILDING = [20, 50, 300]     #b3
# BUILDING = [10, 50, 250]     #b4
# BUILDING = [30, 50, 250]     #b5
# BUILDING = [50, 50, 250]     #b6

# users location data file path

BUILDING        = [20, 50, 200]     #b1
user_data = f"users/UserLocations_{BUILDING[0]}_{BUILDING[1]}_{BUILDING[2]}.dat"
Users_Locations = np.loadtxt(user_data)     #u2

# ========================================================= #
#                       Functions                           #
# ========================================================= #

# generating the initial drones
def generate_drones():
    population = np.zeros((population_size, dimension_size))
    i = 0
    while i < population_size:
        new_drone = generate_drone()
        if not drone_is_inside(new_drone):
            population[i, :] = new_drone
            i += 1
    return population

# generating just one drone
def generate_drone():
    drone = np.zeros(dimension_size)
    drone[0] = x_lower_bound + random() * (x_upper_bound - x_lower_bound)
    drone[1] = y_lower_bound + random() * (y_upper_bound - y_lower_bound)
    drone[2] = z_lower_bound + random() * (z_upper_bound - z_lower_bound)
    return drone

# calculating fitness of all drones in population
def calculate_fitnesses(drones):
    fitnesses = np.zeros(population_size)
    for i in range(population_size):
        fitnesses[i] = fitness(drones[i])
    return fitnesses

# calculation fitness for one individual
def fitness(drone):
    total_sum = 0
    for index in range(Users_Locations.shape[0]):
        total_sum += fitness_per_user(Users_Locations[index], drone)
    return total_sum

# calculating signal strength for one user in the building
def fitness_per_user(user, drone):
    dotProduct = 1
    up = 0
    dp = 0
    d2D = np.sqrt(drone[0]**2)
    d3D = 0

    for i in range(dimension_size):
        d3D += (user[i] - drone[i])**2
        dotProduct += user[i] * drone[i]
        up += user[i]**2
        dp += drone[i]**2
    
    d3D = np.sqrt(d3D)
    mag_mul = np.sqrt(up) * np.sqrt(dp)

    result = (20.0 * np.log10(d3D) + 20.0 * ( 0.301 ) + 32.4) + (14.0 + 15.0 * pow(1.0 - dotProduct/mag_mul, 2.0) ) + (0.5 * d2D)
    return result

# perform infection between two individuals
def perform_infection(x_k, x_m):
    j = np.random.randint(0, dimension_size)
    x_k[j] += np.random.uniform(-1.0, 1.0) * (x_k[j] - x_m[j])
    return check_bounds(x_k)

# check if exceeded bounds
def check_bounds(drone):
    # check drone's x location
    if drone[0] > x_upper_bound: drone[0] = x_upper_bound
    elif drone[0] < x_lower_bound: drone[0] = x_lower_bound
    # check drone's y location
    if drone[1] > y_upper_bound: drone[1] = y_upper_bound
    elif drone[1] < y_lower_bound: drone[1] = y_lower_bound
    # check drone's z location
    if drone[2] > z_upper_bound: drone[2] = z_upper_bound
    elif drone[2] < z_lower_bound: drone[2] = z_lower_bound
    while drone_is_inside(drone):
        drone = generate_drone()
    return drone

# get lists of indexes of doreceivers_numbers and recievers
def get_donors_and_receivers_indexes(fitnesses):
    donors = []
    receivers = []
    sorted_indexes = np.argsort(fitnesses)
    for i in range(donors_number):
        donors.append(sorted_indexes[i])
    for i in range(receivers_number):
        receivers.append(sorted_indexes[-1 - i])
    return donors, receivers

# performing plasma tranfer from donor to receiver indvidual
def perform_plasma_transfer(receiver, donor):
    for j in range(dimension_size):
        receiver[j] += np.random.uniform(-1.0, 1.0) * (receiver[j] - donor[j])
    return check_bounds(receiver)

# updating donor's parameters
def update_donor(donor):
    for j in range(dimension_size):
        donor[j] += np.random.uniform(-1.0, 1.0) * donor[j]
    return check_bounds(donor)

# compare individual's fitness with global fitness value
def compare_with_best_fitness(x):
    global best_fitness
    x_fitness = fitness(x)
    if x_fitness < best_fitness:
        best_fitness = x_fitness
        # best_index = fitnesses.index(min(fitnesses))
        best_index = np.where(fitnesses == best_fitness)
        print(f"Best: {best_fitness} \t - location: {population[best_index]}")


# check if the drone is inside the building or not
def drone_is_inside(drone):
    x_in = False
    y_in = False
    z_in = False
    if 0 <= drone[0] <= BUILDING[0]: x_in = True
    if 0 <= drone[1] <= BUILDING[1]: y_in = True
    if 0 <= drone[2] <= BUILDING[2]: z_in = True
    return (x_in and y_in and z_in)

# ========================================================= #
#                      Start of IPA                         #
# ========================================================= #

# generating initial population
population = generate_drones()

# calculating fitness of population
fitnesses = calculate_fitnesses(population)

# finding best individual fitness
best_fitness = min(fitnesses)

# print("==> Population: ")
# print(population)
# print("==> Fitnesses: ")
# print(fitnesses)

# for i in range(population_size):
#     print(f"Location: {population[i, :]} \t- Fitness: {fitnesses[i]} \t- is inside: {drone_is_inside(population[i])}")


print(f"Initial best fitness value: {best_fitness}")
print(f"Number of parameters: {dimension_size}")
print(f"Population size: {population_size}")

while current_evaluation < maximum_evaluations:

    # start of infection phase
    for index in range(population_size):
        if current_evaluation < maximum_evaluations:
            current_evaluation += 1
            random_index = np.random.randint(0, population_size)
            while random_index == index:
                random_index = np.random.randint(0, population_size)
            current_individual = population[index].copy()
            random_individual = population[random_index].copy()
            infected_individual = perform_infection(current_individual, random_individual)
            fitness_of_infected = fitness(infected_individual)
            if fitness_of_infected < fitnesses[index]:
                population[index] = infected_individual.copy()
                fitnesses[index] = fitness_of_infected
                compare_with_best_fitness(infected_individual)
        else:
            break # if exceeded maximum evaluation number
    
    # start of plasma transfering phase
    # generating dose_control and treatment_control vectors
    dose_control = np.ones(receivers_number, int)
    treatment_control = np.ones(receivers_number, int)

    # get indexes of both of donors and receivers
    donors_indexes, receivers_indexes = get_donors_and_receivers_indexes(fitnesses)

    for i in range(receivers_number):
        receiver_index = receivers_indexes[i]
        random_donor_index = donors_indexes[int(np.random.randint(0, donors_number))]
        current_receiver = population[receiver_index]
        random_donor = population[random_donor_index]
        while treatment_control[i] == 1:
            if current_evaluation < maximum_evaluations:
                current_evaluation += 1
                treated_individual = perform_plasma_transfer(current_receiver, random_donor)
                treated_fitness = fitness(treated_individual)
                if dose_control[i] == 1:
                    if treated_fitness < fitnesses[random_donor_index]:
                        dose_control[i] += 1
                        population[receiver_index] = treated_individual.copy()
                        fitnesses[receiver_index] = treated_fitness
                    else:
                        population[receiver_index] = random_donor.copy()
                        fitnesses[receiver_index] = fitnesses[random_donor_index]
                        treatment_control[i] = 0
                else:
                    if treated_fitness < fitnesses[receiver_index]:
                        population[receiver_index] = treated_individual.copy()
                        fitnesses[receiver_index] = treated_fitness
                    else:
                        treatment_control[i] = 0
                compare_with_best_fitness(population[receiver_index])
            else:
                break # if exceeded maximum evaluation number


    # start of donors updating phase
    for i in range(donors_number):
        if current_evaluation < maximum_evaluations:
            current_evaluation += 1
            donor_index = donors_indexes[i]
            if (current_evaluation / maximum_evaluations) > random():
                population[donor_index] = update_donor(population[donor_index])
            else:
                population[donor_index] = generate_drone()
            fitnesses[donor_index] = fitness(population[donor_index])
            compare_with_best_fitness(population[donor_index])
        else:
            break # if exceeded maximum evaluation number

# print elapsed time
end_time = time.time()
print(f"Elapsed time: {(end_time - start_time):.2f} seconds")

# print best fitness value in scientific notation
print(f"Best fitness value: {best_fitness:.6e}")

print(fitnesses)


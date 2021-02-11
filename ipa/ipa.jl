using Distributions
using DelimitedFiles
using Printf
using Dates

# start timer
start_time = Dates.now()

# set initial parameters' values
population_size = 10
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
Users_Locations = readdlm("users/UserLocations_20_50_200.dat")

# ========================================================= #
#                       Functions                           #
# ========================================================= #

# generating the initial population
function generate_drones()
    population = zeros(population_size, dimension_size)
    i = 1
    while i <= population_size
        new_drone = generate_drone()
        if !drone_is_inside(new_drone)
            population[i, :] = new_drone
            i += 1
        end
    end
    return population
end

# generating just one individual
function generate_drone()
    drone = zeros(1, dimension_size)
    drone[1, 1] = x_lower_bound + rand() * (x_upper_bound - x_lower_bound)
    drone[1, 2] = y_lower_bound + rand() * (y_upper_bound - y_lower_bound)
    drone[1, 3] = z_lower_bound + rand() * (z_upper_bound - z_lower_bound)
    return drone
end

# calculating fitness of all individuals in population
function calculate_fitnesses(drones)
    fitnesses = zeros(population_size)
    for i = 1:population_size
        fitnesses[i] = fitness(drones[i, :])
    end
    return fitnesses
end

# calculation fitness for one individual
function fitness(drone)
    total_sum = 0
    for index = 1:(size(Users_Locations)[1])
        total_sum += fitness_per_user(Users_Locations[index, :], drone)
    end
    return total_sum
end

# calculating signal strength for one user in the building
function fitness_per_user(user, drone)
    dotProduct = 1
    up = 0
    dp = 0
    d2D = sqrt(drone[1] ^ 2)
    d3D = 0

    for i = 1:dimension_size
        d3D += (user[i] - drone[i]) ^ 2
        dotProduct += user[i] * drone[i]
        up += user[i] ^ 2
        dp += drone[i] ^ 2
    end
    
    d3D = sqrt(d3D)
    mag_mul = sqrt(up) * sqrt(dp)

    result = (20.0 * log10(d3D) + 20.0 * ( 0.301 ) + 32.4) + (14.0 + 15.0 * ((1.0 - dotProduct/mag_mul) ^ 2) ) + (0.5 * d2D)
    return result
end

# perform infection between two individuals
function perform_infection(x_k, x_m)
    j = rand(1:dimension_size)
    x = copy(x_k)
    x[j] = x_k[j] + (rand(Uniform(-1.0, 1.0)) * (x_k[j] - x_m[j]))
    return check_bounds(x)
end

# check if exceeded bounds
function check_bounds(drone)
    # check drone's x location
    if drone[1] > x_upper_bound
        drone[1] = x_upper_bound
    elseif drone[1] < x_lower_bound
        drone[1] = x_lower_bound
    end
    # check drone's y location
    if drone[2] > y_upper_bound
        drone[2] = y_upper_bound
    elseif drone[2] < y_lower_bound
        drone[2] = y_lower_bound
    end
    # check drone's z location
    if drone[3] > z_upper_bound
        drone[3] = z_upper_bound
    elseif drone[3] < z_lower_bound
        drone[3] = z_lower_bound
    end
    while drone_is_inside(drone)
        drone = generate_drone()
    end
    return drone
end

# get lists of indexes of doreceivers_numbers and recievers
function get_donors_and_receivers_indexes(fitnesses)
    donors = zeros(Int64, donors_number)
    receivers = zeros(Int64, receivers_number)
    sorted_indexes = sortperm(fitnesses)
    for i = 1:donors_number
        donors[i] = sorted_indexes[i]
    end
    reverse!(sorted_indexes)
    for i = 1:receivers_number
        receivers[i] = sorted_indexes[i]
    end
    return donors, receivers
end

# performing plasma tranfer from donor to receiver indvidual
function perform_plasma_transfer(receiver, donor)
    for j = 1:dimension_size
        receiver[j] += rand(Uniform(-1, 1)) * (receiver[j] - donor[j])
    end
    return check_bounds(receiver)
end

# updating donor's parameters
function update_donor(donor)
    for j = 1:dimension_size
        donor[j] += rand(Uniform(-1, 1)) * donor[j]
    end
    return check_bounds(donor)
end

# compare individual's fitness with global fitness value
function compare_with_best_fitness(x)
    if fitness(x) < best_fitness
        global best_fitness = fitness(x)
        best_index = argmin(fitnesses)
        best = population[best_index, :]
        println("Best: $best_fitness \t - location: $best")
    end
end

# check if the drone is inside the building or not
function drone_is_inside(drone)
    x_in = false
    y_in = false
    z_in = false
    if 0 <= drone[1] <= BUILDING[1] 
        x_in = true
    end
    if 0 <= drone[2] <= BUILDING[2] 
        y_in = true
    end
    if 0 <= drone[3] <= BUILDING[3] 
        z_in = true
    end
    return (x_in && y_in && z_in)
end

# ========================================================= #
#                      Start of IPA                         #
# ========================================================= #

# generating initial population
population = generate_drones()

println(population)

# calculating fitness of population
fitnesses = calculate_fitnesses(population)

# finding best individual fitness
best_fitness = minimum(fitnesses)

# print initial best fitness value and other statistics
println("Initial best fitness value: $best_fitness")
println("Number of parameters: $dimension_size")
println("Population size: $population_size")

while current_evaluation < maximum_evaluations

    # start of infection phase
    for index = 1:population_size
        if current_evaluation < maximum_evaluations
            global current_evaluation += 1
            random_index = rand(1:population_size)
            while random_index == index
                random_index = rand(1:population_size)
            end
            current_individual = population[index, :]
            random_individual = population[random_index, :]
            infected_individual = perform_infection(current_individual, random_individual)
            fitness_of_infected = fitness(infected_individual)
            if fitness_of_infected < fitnesses[index]
                population[index, :] = copy(infected_individual)
                fitnesses[index] = fitness_of_infected
                compare_with_best_fitness(infected_individual)
            end
        else
            break # if exceeded maximum evaluation number
        end
    end

    # start of plasma transfering phase
    # generating dose_control and treatment_control vectors
    dose_control = ones(Int64, receivers_number)
    treatment_control = ones(Int64, receivers_number)

    # get indexes of both of donors and receivers
    donors_indexes, receivers_indexes = get_donors_and_receivers_indexes(fitnesses)
    
    for i = 1:receivers_number
        receiver_index = receivers_indexes[i]
        random_donor_index = donors_indexes[Int(rand(1:donors_number))]
        current_receiver = population[receiver_index, :]
        random_donor = population[random_donor_index, :]
        while treatment_control[i] == 1
            if current_evaluation < maximum_evaluations
                global current_evaluation += 1
                treated_individual = perform_plasma_transfer(current_receiver, random_donor)
                treated_fitness = fitness(treated_individual)
                if dose_control[i] == 1
                    if treated_fitness < fitnesses[random_donor_index]
                        dose_control[i] += 1
                        population[receiver_index, :] = copy(treated_individual)
                        fitnesses[receiver_index] = treated_fitness
                    else
                        population[receiver_index, :] = copy(random_donor)
                        fitnesses[receiver_index] = fitnesses[random_donor_index]
                        treatment_control[i] = 0
                    end
                else
                    if treated_fitness < fitnesses[receiver_index]
                        population[receiver_index, :] = copy(treated_individual)
                        fitnesses[receiver_index] = treated_fitness
                    else
                        treatment_control[i] = 0
                    end
                end
                compare_with_best_fitness(population[receiver_index, :])
            else
                break # if exceeded maximum evaluation number
            end
        end
    end

    # start of donors updating phase
    for i = 1:donors_number
        if current_evaluation < maximum_evaluations
            global current_evaluation += 1
            donor_index = donors_indexes[i]
            if (current_evaluation / maximum_evaluations) > rand()
                population[donor_index, :] = update_donor(population[donor_index, :])
            else
                population[donor_index, :] = generate_drone()
            end
            fitnesses[donor_index] = fitness(population[donor_index, :])
            compare_with_best_fitness(population[donor_index, :])
        else
            break # if exceeded maximum evaluation number
        end
    end
end

# print elapsed time
end_time = Dates.now()
total_time = (Dates.value(end_time) - Dates.value(start_time)) / 1000
@printf("Elapsed time: %.2f seconds\n", total_time)

# print best fitness value in scientific notation
@printf("Best fitness value: %.6e\n", best_fitness)

println(fitnesses)
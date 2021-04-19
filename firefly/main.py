import random
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
from firefly import Firefly
from config_file import POP_SIZE, MAX_GEN, DIM_SIZE, UB, LB, BUILDING, Location_Array, Firefly_List, O_Firefly_List, Fitnesses, Best


# check if the drone is inside the building or not
def drone_is_inside(drone):
    x_in = False
    y_in = False
    z_in = False
    if drone.location[0] <= 0 and drone.location[0] >= BUILDING[0]:
        x_in = True
    if drone.location[1] >= 0 and drone.location[1] <= BUILDING[1]:
        y_in = True
    if drone.location[2] >= 0 and drone.location[2] <= BUILDING[2]:
        z_in = True
    return (x_in and y_in and z_in)


def generate_fireflies():
    i = 0
    while i < POP_SIZE:
        new_firefly = create_firefly()
        if not drone_is_inside(new_firefly):
            Firefly_List[i] = new_firefly
            O_Firefly_List[i] = new_firefly
            i += 1
    for i in range(POP_SIZE):
        Fitnesses[i] = Firefly_List[i].fitness


def create_firefly():
    for index in range(DIM_SIZE):
        Location_Array[index] = random.uniform(LB, UB)
    return Firefly(Location_Array)


def rank_fireflies(): #Global Minimum
    best_firefly = min(Fitnesses)
    min_index = Fitnesses.index(best_firefly)
    loc = Firefly_List[min_index].location
    print("Best_value: {} - Location {}  {}  {}".format(best_firefly, loc[0], loc[1], loc[2]))
    Best.append(best_firefly)


def plot():
    plt.style.use('seaborn-whitegrid')
    ax = plt.axes(projection="3d")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    B = BUILDING
    x_lines = [None, None, None, None]
    y_lines = [None, None, None, None]
    z_lines = [None, None, None, None]
    x_lines[0], = ax.plot3D(np.linspace(0, B[0], B[0]), [0] * B[0], [0] * B[0], 'b-')
    x_lines[1], = ax.plot3D(np.linspace(0, B[0], B[0]), [0] * B[0], [B[2]] * B[0], 'b-')
    x_lines[2], = ax.plot3D(np.linspace(0, B[0], B[0]), [B[1]] * B[0], [0] * B[0], 'b-')
    x_lines[3], = ax.plot3D(np.linspace(0, B[0], B[0]), [B[1]] * B[0], [B[2]] * B[0], 'b-')

    y_lines[0], = ax.plot3D([0] * B[1], np.linspace(0, B[1], B[1]), [0] * B[1], 'b-')
    y_lines[1], = ax.plot3D([B[0]] * B[1], np.linspace(0, B[1], B[1]), [0] * B[1], 'b-')
    y_lines[2], = ax.plot3D([0] * B[1], np.linspace(0, B[1], B[1]), [B[2]] * B[1], 'b-')
    y_lines[3], = ax.plot3D([B[0]] * B[1], np.linspace(0, B[1], B[1]), [B[2]] * B[1], 'b-')

    z_lines[0], = ax.plot3D([0] * B[2], [0] * B[2], np.linspace(0, B[2], B[2]), 'b-')
    z_lines[1], = ax.plot3D([B[0]] * B[2], [0] * B[2], np.linspace(0, B[2], B[2]), 'b-')
    z_lines[2], = ax.plot3D([0] * B[2], [B[1]] * B[2], np.linspace(0, B[2], B[2]), 'b-')
    z_lines[3], = ax.plot3D([B[0]] * B[2], [B[1]] * B[2], np.linspace(0, B[2], B[2]), 'b-')

    for i in range(POP_SIZE):
        l = Firefly_List[i].location
        if drone_is_inside(Firefly_List[i]):
            ax.scatter(l[0], l[1], l[2], c='g', marker='o')
        else:
            ax.scatter(l[0], l[1], l[2], c='r', marker='x')
    
    for i in range(POP_SIZE):
        l = O_Firefly_List[i].location
        ax.scatter(l[0], l[1], l[2], c='b', marker='.')
            
    plt.draw()  
    plt.show()



def main():

    generate_fireflies()
    orginal = Fitnesses.copy()
    print('Searching ...')
    for _ in range(MAX_GEN):
        
        for i in range(POP_SIZE):
            moved = True
            for j in range(POP_SIZE):
                distance = Firefly_List[i].calc_distance(Firefly_List[j])
                if Firefly_List[i].fitness > Firefly_List[j].fitness:
                    new_firefly = Firefly(Firefly_List[i].location)
                    new_firefly.update_location(Firefly_List[j], distance)
                    while drone_is_inside(new_firefly):
                        new_firefly = Firefly(Firefly_List[i].location)
                        new_firefly.update_location(Firefly_List[j], distance)
                    new_firefly.fitness = new_firefly.update_fitness()
                    moved = True
                    if new_firefly.fitness < Firefly_List[i].fitness and not drone_is_inside(new_firefly):
                        Firefly_List[i] = new_firefly
                        Fitnesses[i] = new_firefly.fitness
            if not moved:
                new_firefly = Firefly(Firefly_List[i].location)
                new_firefly.move_randomly()
                while drone_is_inside(new_firefly):
                    new_firefly = Firefly(Firefly_List[i].location)
                    new_firefly.move_randomly()
                new_firefly.fitness = new_firefly.update_fitness()
                if new_firefly.fitness < Firefly_List[i].fitness and not drone_is_inside(new_firefly):
                    Firefly_List[i] = new_firefly
                    Fitnesses[i] = new_firefly.fitness
            Firefly_List[i].check_bounds()
            Firefly_List[i].fitness = Firefly_List[i].update_fitness()


    # for index in range(POP_SIZE):
    #     print(">>>  FF[{}]: {} >>>  {}".format(index, Firefly_List[index].fitness, orginal[index]))

    rank_fireflies()
    plot()

if __name__ == "__main__":
    main()
    

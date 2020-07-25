import numpy as np

POP_SIZE        = 50
MAX_GEN         = 1
DIM_SIZE        = 3
ALPHA           = 1.0
BETA0           = 0.5
GAMMA           = 1.0
BOUND           = 1000
UB              = BOUND
LB              = -BOUND
BUILDING        = [20, 50, 200]     #b1
# BUILDING        = [20, 50, 250]     #b2
# BUILDING        = [20, 50, 300]     #b3
# BUILDING        = [10, 50, 250]     #b4
# BUILDING        = [30, 50, 250]     #b5
# BUILDING        = [50, 50, 250]     #b6


Location_Array  = [0] * DIM_SIZE
Firefly_List    = [0] * POP_SIZE
O_Firefly_List  = [0] * POP_SIZE
Fitnesses       = [0] * POP_SIZE
Best            = []
Users_Locations = np.loadtxt( 'users/UserLocations_20_50_200.dat' )     #u1
# Users_Locations = np.loadtxt( 'users/UserLocations_20_50_250.dat' )     #u2
# Users_Locations = np.loadtxt( 'users/UserLocations_20_50_300.dat' )     #u3
# Users_Locations = np.loadtxt( 'users/UserLocations_10_50_250.dat' )     #u4
# Users_Locations = np.loadtxt( 'users/UserLocations_30_50_250.dat' )     #u5
# Users_Locations = np.loadtxt( 'users/UserLocations_50_50_250.dat' )     #u6


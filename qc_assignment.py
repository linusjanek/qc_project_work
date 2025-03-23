from helper import rnd_points
from brute_force import brute_force
from quantum import quantum

points = rnd_points(4)

#print(brute_force(points))
print(quantum(points))
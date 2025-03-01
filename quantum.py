import numpy as np
from helper import cost_function
from helper import angle_to_bloch, rnd_points, QuantumState

class BlochSphere:
    def __init__(self, azel):
        # Matrix representation of the Bloch Sphere via indices <P_ij>
        # see equation (4) in paper
        self.P = np.ndarray((len(azel), len(azel)), dtype=QuantumState)
        n = len(azel)
        print(self.P)
        for i in range(n):
            for j in range(n):
                print(i,j)
                print(self.P[i][j])
                print(angle_to_bloch(i*2*np.pi/n, cost_function(azel[i], azel[j])))
                self.P[i][j] = angle_to_bloch(i*2*np.pi/n, cost_function(azel[i], azel[j]))

def cost_matrix(azel: list[list[int]]):
    m = np.zeros(shape=(len(azel), len(azel)))
    for i in range(1, len(azel)):
        for j in range(i):
            cost = cost_function(azel[i], azel[j])
            m[i, j] = cost
            m[j, i] = cost
    return m

def epsilon_matrix(azel: list[list[int]]) -> np.ndarray:
    m = np.ones(shape=(len(azel), len(azel)))
    for i in range(1, len(azel)):
        for j in range(i):
            cost = cost_function(azel[i], azel[j])
            m[i, j] = cost
            m[j, i] = cost
    return m

def quantum(azels):
    return (0,0)

blochsphere = BlochSphere(rnd_points(5))
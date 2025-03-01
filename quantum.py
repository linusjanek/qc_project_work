import numpy as np
from helper import cost_function

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
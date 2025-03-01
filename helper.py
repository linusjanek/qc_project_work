import numpy as np
import random
# EVERYTHING IN RADIANS
AzEl = (float, float)
VectorFloat = (float, float, float)
QuantumState = (complex, complex)

# return the rotation angle
def cost_function(start_azel: AzEl, end_azel: AzEl) -> float:
    return np.arccos(np.sin(start_azel[1]) * np.sin(end_azel[1]) + np.cos(start_azel[1]) * np.cos(end_azel[1]) * np.cos(end_azel[0] - start_azel[0]))

def vector_from_azel(azel: AzEl) -> VectorFloat:
    return [np.sin(azel[0]) * np.cos(azel[1]), np.cos(azel[0]) * np.cos(azel[1]), np.sin(azel[1])]

def rnd_points(n: int) -> list[AzEl]:
    return [[random.uniform(0, 2*np.pi), random.uniform(0, np.pi)] for i in range(n)]

def route_cost(route: list[AzEl]) -> float:
    total_cost = 0
    n = len(route)
    for i in range(n):
        current_azel = route[i]
        next_azel = route[(i + 1) % n] # Wrap around to the start of the route
        total_cost += cost_function(current_azel, next_azel)
    return total_cost

def angle_to_bloch(phi: float, theta: float) -> QuantumState:
    zero_factor = np.cos(theta/2)
    one_factor = np.exp(1j * phi/2) * np.sin(theta/2)
    return (zero_factor, one_factor)
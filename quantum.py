import numpy as np
from helper import cost_function
import sympy as sp
from dwave.samplers import SimulatedAnnealingSampler

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

# Returns list of indices of shortest route
def quantum(azel: list[list[int]]) -> list[int]:
    # costs is a square symmetrical n by n matrix, the diagonal is all zeros
    costs = cost_matrix(azel)
    # Get dimension
    n = costs.shape[0]
    # The QUBO will contain n*(n-1) individual variables (the diagonal is always zero)
    variables = [f"p{i}_{j}" for i in range(n) for j in range(n)]
    for i in range(n):
        variables.remove(f"p{i}_{i}")
    # We need a dict that maps all coefficients, initialize it with all zeros
    coeff = {}
    for i, v_i in enumerate(variables):
        for v_j in variables[i:]:
            coeff[(v_i, v_j)] = 0
    # For this to work, we will built an equation with sympy and afterwards extract the coefficients
    qubo_equation = 0
    # Imprint the first constraint: The sum of each row must be equal to 1
    term = 0
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            term += sp.symbols(f"p{i}_{j}")
        qubo_equation += (term-1)**2
        term = 0
    # Imprint the second constraint: The sum of each column must be equal to 1
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            term += sp.symbols(f"p{j}_{i}")
        qubo_equation += (term-1)**2
        term = 0
    # Finally, the target: the sum of the paths shall be minimal
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            qubo_equation += costs[i,j] * sp.symbols(f"p{i}_{j}")
    # Expand the equation and extract all coefficients
    qubo_equation = sp.expand(qubo_equation)
    qubo_dict = qubo_equation.as_coefficients_dict()
    for key in qubo_dict:
        oldkey = key
        key = str(key)
        if key == "1":
            continue
        if key.endswith("**2"):
            key = key[:-3]
        key2 = key
        index = key.find("*")
        if index != -1:
            key2 = key[index+1:]
            key = key[0:index]
        coeff[(key, key2)] += qubo_dict[oldkey]

    # Now, send the QUBO to DWave
    sampler = SimulatedAnnealingSampler()
    sampleset = sampler.sample_qubo(coeff, num_reads=50000).aggregate().to_pandas_dataframe()
    print(sampleset)
    return (0,0)
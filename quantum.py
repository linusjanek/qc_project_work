import numpy as np
from helper import cost_function, route_cost
import sympy as sp
from sympy import lambdify
from scipy.optimize import basinhopping
from dwave.samplers import SimulatedAnnealingSampler
import pandas as pd

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

def verify_constraints(series: pd.Series) -> bool:
    # Get dimensions
    n = series.shape[0] - 2
    n = int((1 + np.sqrt(1 + 4*n))/2)
    # Verify that each city was just visited once
    for i in range(n):
        sum_row = 0
        sum_col = 0
        for j in range(n):
            if i == j:
                continue
            sum_row += series.loc[f"p{i}_{j}"]
            sum_col += series.loc[f"p{j}_{i}"]
        if sum_row != 1 or sum_col != 1:
            return False
    # Verify that the entire route is connected
    route = []
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if int(series.loc[f"p{i}_{j}"]) == 1:
                route.append(f"p{i}_{j}")
                break
    indeces = []
    route_i = 0
    while True:
        mark = route[route_i].find("_")
        this_i = int(route[route_i][1:mark])
        next_i = int(route[route_i][mark+1:])
        indeces.append(this_i)
        if next_i in indeces:
            break
        for i, r in enumerate(route):
            if r.startswith(f"p{next_i}_"):
                route_i = i
                break
    if len(indeces) == n:
        return indeces
    return False

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
    # Imprint the third constraint: Route must visit all cities (no subsycles can be build). (Only implemented for subsycle of 2)
    for i in range(n-1):
        for j in range(i+1,n):
            term = sp.symbols(f"p{i}_{j}")
            term *=sp.symbols(f"p{j}_{i}")
            qubo_equation += term
            term = 0
    # Finally, the target: the sum of the paths shall be minimal
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            qubo_equation += costs[i,j] * sp.symbols(f"p{i}_{j}")
    # Expand the equation and extract all coefficients
    #print(qubo_equation)
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
    sampleset["valid"] = False
    for i in range(sampleset.shape[0]):
        sampleset["valid"].iloc[i] = (verify_constraints(sampleset.iloc[i]) != False)
    while True:
        min = sampleset[sampleset["energy"] == sampleset["energy"].min()]
        v = verify_constraints(min.iloc[0])
        if v != False:
            route = [azel[v_i] for v_i in v]
            return route, route_cost(route)
        sampleset.drop(min.index[0], inplace=True)

def qubo_linus(azel: list[list[int]], function = False):
    # costs is a square symmetrical n by n matrix, the diagonal is all zeros
    costs = cost_matrix(azel)
    # Get dimension
    n = costs.shape[0]

    variables = [f"p{v}_{j}" for v in range(n) for j in range(n)]

    # We need a dict that maps all coefficients, initialize it with all zeros
    coeff = {}
    for i, v_i in enumerate(variables):
        coeff[(v_i, v_i)] = 0
        for v_j in variables[i:]:
            coeff[(v_i, v_j)] = 0

    # Helper term to make life easier
    term = 0

    # To initialize the QUBO according to [...], we define the Hamiltonian H = H_A + H_B
    # Starting with H_A
    hamiltonian_A = 0

    # Every vertex must be visited exactly once
    for v in range(n):
        for j in range(n):
            term += sp.symbols(f"p{v}_{j}")
        hamiltonian_A += (1-term)**2
        term = 0

    # jth node in the cycle for each j
    for j in range(n):
        for v in range(n):
            term += sp.symbols(f"p{v}_{j}")
        hamiltonian_A += (1-term)**2
        term = 0

    # Penalty term for edges not in E meaning self loops
    # for v in range(n):
    #     for j in range(n):
    #         if j == n-1:
    #             hamiltonian_A += sp.symbols(f"p{v}_{j}") * sp.symbols(f"p{v}_{0}")
    #         else:
    #             hamiltonian_A += sp.symbols(f"p{v}_{j}") * sp.symbols(f"p{v}_{j+1}")
    
    hamiltonian_B = 0

    # Route cost
    for u in range(n):
        for v in range(n):
            if u != v:
                for j in range(n):
                    if j == n-1:
                        term += sp.symbols(f"p{u}_{j}") * sp.symbols(f"p{v}_{0}")
                    else:
                        term += sp.symbols(f"p{u}_{j}") * sp.symbols(f"p{v}_{j+1}")
                hamiltonian_B += costs[u,v] * term
                term = 0

    A = max(costs.flatten())
    B = 1
    qubo_equation = A * hamiltonian_A + B * hamiltonian_B

    if function:
        return qubo_equation

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
        if (key, key2) in coeff:
            coeff[(key, key2)] += qubo_dict[oldkey]
        else:
            coeff[(key2, key)] += qubo_dict[oldkey]

    return coeff

def verify_constraints_linus(series: pd.Series) -> bool:
    # Get dimensions
    n = series.shape[0] - 2
    n = int((1 + np.sqrt(1 + 4*n))/2)
    # Verify that each city was just visited once
    for v in range(n):
        sum_row = 0
        sum_col = 0
        for j in range(n):
            # if i == j:
                # continue
            sum_row += series.loc[f"p{v}_{j}"]
            sum_col += series.loc[f"p{v}_{j}"]
        if sum_row != 1 or sum_col != 1:
            return False
    # Create list of edges from list of vertices
    route = []
    for j in range(n):
        for v in range(n):
            if int(series.loc[f"p{v}_{j}"]) == 1:
                if j == 0:
                    prev_vertex = v
                    init_vertex = v
                else:
                    route.append(f"p{prev_vertex}_{v}")
                    prev_vertex = v
                    if j == n-1:
                        route.append(f"p{v}_{init_vertex}")
                break
    indeces = []
    route_i = 0
    while True:
        mark = route[route_i].find("_")
        this_i = int(route[route_i][1:mark])
        next_i = int(route[route_i][mark+1:])
        indeces.append(this_i)
        if next_i in indeces:
            break
        for i, r in enumerate(route):
            if r.startswith(f"p{next_i}_"):
                route_i = i
                break
    if len(indeces) == n:
        return indeces
    return False

def quantum_linus(azel: list[list[int]]) -> list[int]:
    coeff = qubo_linus(azel)
    sampler = SimulatedAnnealingSampler()
    sampleset = sampler.sample_qubo(coeff, num_reads=50000).aggregate().to_pandas_dataframe()
    min = sampleset[sampleset["energy"] == sampleset["energy"].min()]
    v = verify_constraints_linus(min.iloc[0])
    if v != False:
        route = [azel[v_i] for v_i in v]
        return route, route_cost(route)
    return False

#TODO this doesn't work for some reason
def basin_hopping_tsp(azel: list[list[int]]) -> list[int]:
    function = qubo_linus(azel, function=True)
    # Convert to lambda function
    f = lambdify([*function.free_symbols], function, 'numpy')
    # Create x0 with all zeros
    print(function.free_symbols)
    x0 = np.zeros(len(function.free_symbols))
    print(f(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))
    minimizer_kwargs = {"method": "BFGS"}
    ret = basinhopping(function, x0, minimizer_kwargs=minimizer_kwargs,niter=200)

    # the global minimum is:
    ret.x, ret.fun
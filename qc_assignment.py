from helper import rnd_points, generate_subgroup_indices
from brute_force import brute_force
from quantum import quantum, quantum_linus, basin_hopping_tsp
import json
from datetime import datetime
from time import time  # Import time module for runtime measurement

# Get the current timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# Define the output file path
file_path = f'./out/data_{timestamp}.json'

'''
input_data = {}
with open(f"Brute_Force/out/output{4}_{2}.json") as input_file:
    input_data = json.load(input_file)
print(input_data)
points = input_data[0]["points"]
cb = input_data[0]["cost"]
subgroup_indices = generate_subgroup_indices(4, 2)

correct = True
num_iterations = 20000
while correct:
    rq, cq = quantum_linus(points, subgroup_indices=subgroup_indices, num_reads=num_iterations)
    if abs(cb-cq) < 0.0001:
        print(f"Correct! cb == {round(cb, 4)}, cq == {round(cq, 4)}")
        num_iterations = int(num_iterations * 0.5) + 1
    else:
        print(f"Failed at {num_iterations} iterations! cb == {round(cb, 4)}, cq == {round(cq, 4)}")
        correct = False
num_iterations = num_iterations * 2'
'''
better_qt_solution_counter = 0
for num_iterations in [100]:
    iterator_path = f'./out/num_iterations_subgroups_{num_iterations}.json'
    iterator_data = []
    for targets in range(6, 7):
        for subgroup_size in range(2, 7):
        # for subgroup_size in range(2, 5):
            # Load targets from C++ JSON output
            input_data = {}
            if subgroup_size == 0:
                with open(f"Brute_Force/out/output{targets}.json") as input_file:
                    input_data = json.load(input_file)
            else:
                with open(f"Brute_Force/out/output{targets}_{subgroup_size}.json") as input_file:
                    input_data = json.load(input_file)

            print(input_data)
            correct = 0
            total_runtime = 0
            n_points = int(len(input_data))
            for i in range(n_points):
                #points = rnd_points(targets)
                #rb, cb = brute_force(points)
                #points = input_data[i]["points"]
                points = input_data[i]["points"]
                cb = input_data[i]["cost"]
                
                subgroup_indices = generate_subgroup_indices(targets, subgroup_size)

                start_time = time()  # Start the timer
                rq, cq = quantum_linus(points, subgroup_indices=subgroup_indices, num_reads=num_iterations)
                end_time = time()  # End the timer

                runtime = end_time - start_time  # Calculate runtime
                total_runtime += runtime  # Accumulate runtime

                print(f"Runtime: {runtime:.4f} seconds")  # Print runtime
                print(rq)
                str = f"Attempt {i+1}/{n_points}: cb == {round(cb, 4)}, cq == {round(cq, 4)} -> "
                if abs(cb-cq) < 0.0001:
                    correct += 1
                    str += "correct!"
                else:
                    str += "failed!"
                    if cq < cb:
                        str += " BETTER QUANTUM SOLUTION"
                        better_qt_solution_counter += 1
                print(str)

                # Write points, rq and cq to json file
                new_data = dict()
                new_data['id'] = f'{targets}.{i}'
                new_data['points'] = points
                new_data['rq'] = rq
                new_data['cq'] = cq

                # Add runtime to json
                new_data['runtime'] = runtime
                try:
                    # Read the existing JSON data
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                except FileNotFoundError:
                    # If the file doesn't exist, start with an empty list
                    data = []

                # Append the new data
                data.append(new_data)

                # Write the updated data back to the file
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
            print(f"Total: {correct}/{len(input_data)} were correct!")

            new_data = dict()
            new_data['id'] = f'{targets}.{subgroup_size}'
            new_data['num_iterations'] = num_iterations
            new_data['correct'] = correct
            new_data['total'] = n_points
            new_data['average_runtime'] = total_runtime/n_points

            iterator_data.append(new_data)   
            with open(iterator_path, 'w') as file:
                json.dump(iterator_data, file, indent=4)

print(f"Quantum annealing found {better_qt_solution_counter} better solutions than brute force.")
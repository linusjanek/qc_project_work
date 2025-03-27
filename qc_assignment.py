from helper import rnd_points
from brute_force import brute_force
from quantum import quantum, quantum_linus
import json
from datetime import datetime

total_attempts = 3
correct = 0
targets = 3

# Get the current timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# Define the file path
file_path = f'./out/data_{timestamp}.json'

for i in range(total_attempts):
    points = rnd_points(targets)
    rb, cb = brute_force(points)
    rq, cq = quantum_linus(points)
    str = f"Attempt {i+1}/{total_attempts}: cb == {round(cb, 4)}, cq == {round(cq, 4)} -> "
    if abs(cb-cq) < 0.0001:
        correct += 1
        str += "correct!"
    else:
        str += "failed!"
    print(str)

    # Write points, rq and cq to json file
    new_data = dict()
    new_data['id'] = i
    new_data['points'] = points
    new_data['rq'] = rq
    new_data['cq'] = cq
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
    print(f"Total: {correct}/{total_attempts} were correct!")
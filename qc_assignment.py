import json
import time
from helper import rnd_points, deterministic_points
from brute_force import brute_force
#from quantum import quantum, quantum_linus

total_attempts = 10
correct = 0
targets = 5
for targets in range(4,13):
    points = deterministic_points(targets)
    
    start_time = time.time()
    rb, cb = brute_force(points)
    elapsed_time = time.time() - start_time  # Calculate elapsed time
    
    # Prepare data to save
    data = {
        "targets": targets,
        "points": points,
        "route": rb,
        "cost": cb,
        "time_taken": elapsed_time  # Add elapsed time to the data
    }
    # Save to a JSON file
    filename = f"iteration_targets_{targets}.json"
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)
    
#for i in range(total_attempts):
#    points = deterministic_points(targets)
#    rb, cb = brute_force(points)
#    rq, cq = quantum_linus(points) # type: ignore
#    str = f"Attempt {i+1}/{total_attempts}: cb == {round(cb, 4)}, cq == {round(cq, 4)} -> "
#    if abs(cb-cq) < 0.0001:
#        correct += 1
#        str += "correct!"
#    else:
#        str += "failed!"
#    print(str)
#print(f"Total: {correct}/{total_attempts} were correct!")
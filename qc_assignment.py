from helper import rnd_points
from brute_force import brute_force
from quantum import quantum, quantum_linus

total_attempts = 10
correct = 0
targets = 4
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
print(f"Total: {correct}/{total_attempts} were correct!")
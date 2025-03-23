from helper import rnd_points
from brute_force import brute_force
from quantum import quantum

total_attempts = 10
correct = 0
targets = 6
for i in range(total_attempts):
    points = rnd_points(targets)
    rb, cb = brute_force(points)
    rq, cq = quantum(points)
    str = f"Attempt {i+1}/{total_attempts}: rb: {rb}, cb == {round(cb, 4)}, rq: {rq}, cq == {round(cq, 4)} -> "
    if abs(cb-cq) < 0.001:
        correct += 1
        str += "correct!"
    else:
        str += "failed!"
    print(str)
    #exit(0)
print(f"Total: {correct}/{total_attempts} were correct!")
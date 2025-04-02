# File to plot the results of the simulations
import json
import matplotlib.pyplot as plt
import numpy as np

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth
'''
# Plot the error rate dependent on the ammount of iterations and amount of vertices
for num_iterations in [20, 40, 80, 100, 150, 200, 1000]:
    iterator_path = f'./out/num_iterations_{num_iterations}.json'
    with open(iterator_path) as input_file:
        # Load the JSON data into a Python dictionary
        input_data = json.load(input_file)
        # Extract the data for plotting
        x = []
        y = []
        for i in range(len(input_data)):
            x.append(input_data[i]["id"])
            y.append(input_data[i]["correct"]/input_data[i]["total"])
        # plot the data
        plt.plot(x, y, label=f'{num_iterations} iterations')
        plt.xlabel('Number of vertices')
        plt.ylabel('Accuracy')
        plt.title('Accuracy vs number of vertices, sample size n=50')
        plt.legend()
        plt.grid()
        # Save the plot to a file
plt.savefig(f'./out/num_iterations_{num_iterations}.png')
# Clear the current figure to avoid overlap
plt.clf()

# Same plot, error rate dependent on the ammount of qubo parameters
for num_iterations in [20, 40, 80, 100, 150, 200, 1000]:
    iterator_path = f'./out/num_iterations_{num_iterations}.json'
    with open(iterator_path) as input_file:
        # Load the JSON data into a Python dictionary
        input_data = json.load(input_file)
        # Extract the data for plotting
        x = []
        y = []
        for i in range(len(input_data)):
            x_i = int(input_data[i]["id"].split(".")[0])
            x_i = x_i**2
            x.append(x_i)
            y.append(input_data[i]["correct"]/input_data[i]["total"])
        # plot the data
        plt.plot(x, y, label=f'{num_iterations} iterations')
        plt.xlabel('Number of qubo parameters')
        plt.ylabel('Accuracy')
        plt.title('Accuracy vs number of vertices, sample size n=50')
        plt.legend()
        plt.grid()
        # Save the plot to a file
plt.savefig(f'./out/qubo_params_iteration.png')
# Clear the current figure to avoid overlap
plt.clf()

# Plot that interpolates the amount of iteration needed for an accuracy of 0.95
for num_iterations in [20, 40, 80, 100, 150, 200, 1000]:
    iterator_path = f'./out/num_iterations_{num_iterations}.json'
    with open(iterator_path) as input_file:
        # Load the JSON data into a Python dictionary
        input_data = json.load(input_file)
        # Extract the data for plotting
        x = []
        y = []
        for i in range(len(input_data)):
            x.append(int(input_data[i]["id"].split(".")[0]))
            y.append(input_data[i]["correct"]/input_data[i]["total"])
        # plot the data
        print(np.interp(0.95,y,x))
        plt.plot(smooth(y, 2),x)
plt.show()

# Plot of runtime dependent on number of iterations
for num_iterations in [20, 40, 80, 100, 150, 200, 1000]:
    iterator_path = f'./out/num_iterations_{num_iterations}.json'
    with open(iterator_path) as input_file:
        # Load the JSON data into a Python dictionary
        input_data = json.load(input_file)
        # Extract the data for plotting
        x = []
        y = []
        for i in range(len(input_data)):
            x.append(input_data[i]["id"])
            y.append(input_data[i]["average_runtime"])
        # plot the data
        plt.plot(x, y, label=f'{num_iterations} iterations')
        plt.xlabel('Number of vertices')
        plt.ylabel('Average Runtime (s)')
        plt.title('Runtime vs number of vertices, sample size n=50')
        plt.legend()
        plt.grid()
plt.savefig(f'./out/runtime_iterations.png')

# Plot runtime compared to brute forced solution
iterator_path = f'./out/num_iterations_rt_10000.json'
with open(iterator_path) as input_file:
    # Load the JSON data into a Python dictionary
    input_data = json.load(input_file)
    # Extract the data for plotting
    x = []
    y = []
    for i in range(len(input_data)):
        x.append(int(input_data[i]["id"].split(".")[0]))
        y.append(input_data[i]["average_runtime"])
    # plot the data
    plt.plot(x, y, label=f'Simulated annealing')

x = []
y = []
for targets in range(4,12):
    with open(f"Brute_Force/out/output{targets}.json") as input_file:
        input_data = json.load(input_file)
        # Extract the data for plotting
        x.append(targets)
        y_i = []
        for i in range(len(input_data)):
            y_i.append(input_data[i]["time"])
        y.append(np.mean(y_i))

plt.plot(x, y, label=f'Brute force')
# set y axis to log scale
plt.yscale('log')
plt.xscale('linear')
plt.xlabel('Number of vertices')
plt.ylabel('Average Runtime (s)')
plt.title('Simulated annealing vs. Brute force runtime, 10000 iterations')
plt.legend()
plt.grid()
plt.savefig(f'./out/runtime_vs_brute.png')
'''

# Plot normalized runtime dependent on number of subgroups for annealing and brute force
iterator_path = f'./out/num_iterations_subgroups_100.json'
with open(iterator_path) as input_file:
    # Load the JSON data into a Python dictionary
    input_data = json.load(input_file)
    # Extract the data for plotting
    x = []
    y = []
    for i in range(len(input_data)):
        x.append(int(input_data[i]["id"].split(".")[1]))
        y.append(input_data[i]["average_runtime"])
    y = y / np.max(y)  # Normalize the y values
    # plot the data
    plt.plot(x, y, label=f'Simulated annealing')

x = []
y = []
for subgroups in range(2,7):
    with open(f"Brute_Force/out/output6_{subgroups}.json") as input_file:
        input_data = json.load(input_file)
        # Extract the data for plotting
        x.append(subgroups)
        y_i = []
        for i in range(len(input_data)):
            y_i.append(input_data[i]["time"])
        y.append(np.mean(y_i))
y = y / np.max(y)  # Normalize the y values

plt.plot(x, y, label=f'Brute force')
# set y axis to log scale
plt.yscale('log')
plt.xscale('linear')
plt.xlabel('Number of vertices')
plt.ylabel('Average normalized runtime')
plt.title('Simulated annealing vs. Brute force runtime, 10000 iterations')
plt.legend()
plt.grid()
plt.savefig(f'./out/runtime_vs_brute.png')

plt.savefig(f'./out/runtime_subgroups.png')
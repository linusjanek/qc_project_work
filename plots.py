# File to plot the results of the simulations
import json
import matplotlib.pyplot as plt

# Plot the error rate dependent on the ammount of iterations and amount of vertices
for num_iterations in [20, 40, 80, 100, 150, 200, 1000]:
    iterator_path = f'./out/num_iterations_{num_iterations}.json'
    with open(iterator_path) as input_file:
        # Load the JSON data into a Python dictionary
        input_data = json.load(input_file)
        print(input_data)
        # Extract the data for plotting
        x = []
        y = []
        for i in range(len(input_data)):
            x.append(input_data[i]["id"])
            y.append(input_data[i]["correct"]/input_data[i]["total"])
        # plot the data
        plt.plot(x, y, label=f'{num_iterations} iterations')
        plt.xlabel('Number of vertices')
        plt.ylabel('Error rate')
        plt.title('Error rate vs number of vertices')
        plt.legend()
        plt.grid()
        # Save the plot to a file
plt.savefig(f'./out/num_iterations_{num_iterations}.png')

# Plot of runtime dependent on number of iterations
for num_iterations in [20, 40, 80, 100, 150, 200, 1000, 10000]:
    iterator_path = f'./out/num_iterations_{num_iterations}.json'
    with open(iterator_path) as input_file:
        # Load the JSON data into a Python dictionary
        input_data = json.load(input_file)
        print(input_data)
        # Extract the data for plotting
        x = []
        y = []
        for i in range(len(input_data)):
            x.append(input_data[i]["id"])
            y.append(input_data[i]["runtime"])
        # plot the data
        plt.plot(x, y, label=f'{num_iterations} iterations')
        plt.xlabel('Number of vertices')
        plt.ylabel('Runtime (s)')
        plt.title('Runtime vs number of vertices')
        plt.legend()
        plt.grid() 
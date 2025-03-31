import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Example adjacency matrix (symmetric for an undirected graph)

data = {
    "0": [0,0,0,0,1,0],
    "1": [0,0,1,0,0,0],
    "2": [0,0,0,1,0,0],
    "3": [0,1,0,0,0,0],
    "4": [0,0,0,0,0,1],
    "5": [1,0,0,0,1,0]
}

# Convert to DataFrame
df = pd.DataFrame(data, index=["0", "1", "2", "3", "4", "5"])

# read wrong_min_energy_sampleset.csv
# df = pd.read_csv("wrong_min_energy_sampleset.csv")

# Extract only the first row of data
# df = df.iloc[0:1, 1:]
# Extract only the columns that start with a #
# df = df.loc[:, df.columns.str.startswith("")]


# Create a NetworkX graph
G = nx.from_pandas_adjacency(df)

# Draw the graph
plt.figure(figsize=(5, 5))
nx.draw(G, with_labels=True, node_color="lightblue", edge_color="gray", node_size=100, font_size=15)
plt.show()
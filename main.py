import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Example adjacency matrix (symmetric for an undirected graph)
data = {
    "A": [0, 1, 0, 1],
    "B": [1, 0, 1, 1],
    "C": [0, 1, 0, 1],
    "D": [1, 1, 1, 0]
}

# Convert to DataFrame
df = pd.DataFrame(data, index=["A", "B", "C", "D"])

# Create a NetworkX graph
G = nx.from_pandas_adjacency(df)

# Draw the graph
plt.figure(figsize=(5, 5))
nx.draw(G, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2000, font_size=15)
plt.show()
from model import *
from viewer import *
import networkx as nx

# Using the model

# run simulation
m = Model(30, False)            # initialize with 30 nodes
m.set_evolution(m.gauss())      # set weights to move according to a gaussian (default parameters (0, 0.1))
m.evolve(100)                   # evolve 100 steps

# getting results
t = 30                          # for some time t

print("\nMATRIX\n")             # adjacency matrix (numpy array)
print(m.matrix_at(t))
print("\nWEIGHTS\n")            # weights (all edges)
print(m.weights_at(t).edges())  # (returns networkx graph)
print("\nEDGES\n")
print(m.edges_at(t).edges())    # edges (fixed edges only)
                                # (returns networkx graph)


# More plotting, logging, visualization functions

V = Viewer()
V.load(m.log)
#V.weight_printout().edge_printout()


# wrap a function that errors for disconnected graphs
def shortest_path_wrapper(G):
    try:
        return nx.average_shortest_path_length(G)
    except nx.NetworkXError:
        return 0

# plot some networkx functions
V.plot([
    (nx.number_connected_components, "Connected components"),
    (nx.average_clustering, "Average clustering"),
    (shortest_path_wrapper, "Average shortest path")
    ])

# play some nice animations
V.animate((0,30),V.anim_both)       # plot of the graph over degree histogram
V.animate((31,100),V.anim_adj)        # adjacency heatmap


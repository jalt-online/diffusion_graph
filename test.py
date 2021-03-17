from model import *
from viewer import *
import networkx as nx

# run simulation
m = Model(30, False)            # initialize with 30 nodes
m.set_evolution(m.gauss())      # set weights to move according to a gaussian (default parameters (0, 0.1))
m.evolve(100)                   # evolve 100 steps

# view the record
V = Viewer()
V.load(m.log)
V.weight_printout().edge_printout()


# wrap a function that errors for disconnected graphs
def shortest_path_wrapper(G):
    try:
        return nx.average_shortest_path_length(G)
    except nx.NetworkXError:
        return 0

# plot some networkx functions
V.plot([
    nx.number_connected_components, 
    nx.average_clustering, 
    shortest_path_wrapper
    ])

# play some nice animations
V.animate((0,30),V.anim_both)       # plot of the graph over degree histogram
V.animate((31,100),V.anim_adj)        # adjacency heatmap

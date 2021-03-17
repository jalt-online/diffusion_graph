from model import *
from viewer import *
import networkx as nx

# run simulation
m = Model(30, False)
m.set_evolution(m.gauss())
m.evolve(100)

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


# some nice animations
V.animate((0,20),V.anim_both)
V.animate((0,20),V.anim_degree)
V.animate((0,20),V.anim_adj)

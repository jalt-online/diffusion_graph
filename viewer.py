import collections
import numpy as np
import networkx as nx
from model import *

from matplotlib.pyplot import figure, subplots, axis, pause, plot, xlim, ylim, show, close, Circle, errorbar, title, figtext, legend
from matplotlib.collections import LineCollection

import matplotlib.pyplot as plt

class Viewer():
    def __init__(self, log=None, debug=False):
        self.debug = debug
        self.graphs = []
        self.animate_current = self.anim_degree
        if log is not None: self.load(log)

    def load(self,log):
        self.log = log
        self.graphs = [nx.from_numpy_array(np.where(matrix==1,1,0)) for (matrix, t) in self.log]
        return self

    def show(self,matrix):
        # print network for single graph
        print(matrix)
        return self




    def weight_printout(self, interval=None):
        # print out all current edges
        if interval is None:
            for (matrix, t) in self.log:
                print("Weights at t = " + str(t))
                self.show(matrix)
        else:
            (t0, t1) = interval
            for (matrix, t) in [(matrix, t) for (matrix, t) in self.log if t >= t0 and t <= t1]:
                print("Weights at t = " + str(t))
                self.show(matrix)

        return self




    def edge_printout(self, interval=None):
        # print out only edges that have been fixed
        if interval is None:
            for (matrix, t) in self.log:
                print("Edges at t = " + str(t))
                self.show(np.where(matrix == 1, 1, 0))
        else:
            (t0, t1) = interval
            for (matrix, t) in [(matrix, t) for (matrix, t) in self.log if t >= t0 and t <= t1]:
                print("Edges at t = " + str(t))
                self.show(np.where(matrix == 1, 1, 0))
        
        return self




    def degree_sequence(self, G):
        degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
        degreeCount = collections.Counter(degree_sequence)
        deg, cnt = zip(*degreeCount.items())
        return (deg, cnt)




    def animate(self, interval=None, new_animation=False, rate=0.3, technique="default"):
        if new_animation: self.animate_current = new_animation

        print("Animating")
        show()
        self.fig, self.ax = plt.subplots()
        (t0, t1) = interval if interval is not None else (0, len(self.log))

        for (matrix, t) in [(matrix,t) for (matrix, t) in self.log if t >= t0 and t <= t1]:
            self.animate_current(interval, rate, technique, matrix, t)
            pause(rate)
            self.ax.clear()
            self.fig.clear()

        close(self.fig)
        return self




    def anim_degree(self,interval,rate,technique,matrix,t):
        G = self.graphs[t]
        deg, cnt = self.degree_sequence(G)
        plt.bar(deg, cnt, width=0.80, color=(0.3,0.3,0.8,0.5))

        plt.title("Degree histogram")
        plt.ylabel("Count")
        plt.xlabel("Degree")
        self.ax.set_xticks([d + 0.4 for d in deg])
        self.ax.set_xticklabels(deg)




    def animate_graph(self, interval, rate, technique,matrix,t):
        G = self.graphs[t]
        deg, cnt = self.degree_sequence(G)
        if technique == "default":
            nx.draw(G, node_color="black", node_size=10)
        elif technique == "Circular":
            nx.draw_circular(G, node_color="black", node_size=10)
        elif technique == "Spectral":
            nx.draw_spectral(G, node_color="black", node_size=10)
        elif technique == "Spring":
            nx.draw_spring(G, node_color="black", node_size=10)
        elif technique == "Shell":
            nx.draw_shell(G, node_color="black", node_size=10)




    def anim_both(self, interval, rate, technique,matrix,t):
        # ripping off a nice example from the networkx documentation...
        G = self.graphs[t]
        deg, cnt = self.degree_sequence(G)
        plt.bar(deg, cnt, width=0.80, color=(0.3,0.3,0.8,0.5))

        plt.title("Degree Histogram")
        plt.ylabel("Count")
        plt.xlabel("Degree")
        self.ax.set_xticks([d + 0.4 for d in deg])
        self.ax.set_xticklabels(deg)

        plt.axes([0.2, 0.2, 0.6, 0.6])
        pos = nx.spring_layout(G)
        plt.axis("off")
        nx.draw_networkx_nodes(G, pos, node_size=20, alpha =0.4, node_color="black")
        nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color="black")




    def anim_adj(self, interval, rate, technique, matrix, t):
        plt.imshow(matrix, cmap="hot", interpolation="nearest")



    def plot(self, functions, interval=None):
        # functions should be networkx functions of G
        series = [[] for f in functions] 
        (t0, t1) = interval if interval is not None else (0, len(self.log))
        for t in [t for (matrix, t) in self.log if t >= t0 and t <= t1]:
            for i in range(len(functions)):
                fi = functions[i][0]
                series[i] += [fi(self.graphs[t])]
        
        for i in range(len(functions)):
            plt.plot(series[i], label=functions[i][1])
            plt.legend()
        show()

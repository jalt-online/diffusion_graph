import numpy as np

class Model():
    def __init__(self, n, debug = False):
        self.debug = debug
        self.dim = n
        self.matrix = np.random.rand(n,n).astype(np.double)   # initial random square matrix
        self.mask = np.ones((n,n))        # set entries to 0 to lock matrix entry
        self.zeros = np.zeros((n,n))      # handy
        self.evolution = self.rand(0.1)   # default evolution function: (0.5-rand) * 0.1
        self.log = []                       # log of changes
        self.clock = 0                  # step counter

        self.log += [(np.copy(self.matrix), self.clock)]

    def reset(self):
        self.matrix = np.random.rand(self.dim,self.dim)
        self.clock = 0
        self.log = []
        self.log += [(np.copy(self.matrix), self.clock)]
        return self

    def set_evolution(self, fn):
        self.evolution = fn
        return self

    # default evolution
    def rand(self, s=0.1): # random with scalar s
        def calc(): return (0.5 - np.random.rand(self.dim,self.dim).astype(np.double)) * s
        return calc

    def gauss(self,s=0.1):
        def calc(): return np.random.normal(0.,s, (self.dim,self.dim)).astype(np.double)
        return calc

    def evolve(self, n=10):
        for i in range(n): self.step()
        return self

    def current(self):
        return np.where(self.matrix == 1., 1., 0.)

    def step(self):

        adjustment = self.evolution()   # compute adjustment
        adjustment *= self.mask         # mask off locked values
        self.matrix += adjustment       # adjust
        
        # adjust mask
        lock = np.where((self.matrix < 0.) + (self.matrix > 1.), 1.,0.)
        self.mask -= lock

        # cap values
        self.matrix = np.where(self.matrix >= 1., 1., self.matrix) 
        self.matrix = np.where(self.matrix <= 0., 0., self.matrix) 

        if self.debug: 
            print()
            print(self.matrix)
            print(self.current())

        self.clock += 1
        entry = (self.matrix, self.clock)
        
        self.log += [(np.copy(self.matrix), self.clock)]

        #for (matrix, t) in self.log:
            #if not np.all(matrix>=0): print("NEGATIVES")
            #if not np.all(matrix<=1): print("TOO BIGS")
        return self


